# マルチステージビルド: 本番環境に最適化された小さいイメージ生成

# ステージ1: ビルド
FROM python:3.12-slim as builder

WORKDIR /build

# システム依存関係をインストール（Pillow等の複雑なパッケージのため）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ステージ2: ランタイム
FROM python:3.12-slim

# メタデータ
LABEL maintainer="Django App"
LABEL description="Django application running with Gunicorn"

# 環境変数設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# ビルドステージからインストール済みパッケージをコピー
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# アプリケーションコードをコピー
COPY mysite/ /app/

# 非rootユーザーを作成（セキュリティベストプラクティス）
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Static filesの収集ディレクトリを作成（権限確認）
RUN mkdir -p /app/staticfiles

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# アプリケーション起動
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "mysite.wsgi:application"]
