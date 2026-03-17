# Docker 運用ガイド

## 目的
このプロジェクトの Docker 関連設定を、以下の前提で統一しています。

- `150.19.10.214` と `oc-stamp.cc.it-hiroshima.ac.jp` は名前解決済み
- SSL 証明書は取得済み（Let's Encrypt）
- Django アプリ本体コードは変更しない

## 構成概要

### 開発
- ファイル: `docker-compose.yml`
- 構成: `app` のみ
- DB: SQLite（コンテナ内）
- 公開: `http://localhost:8000`

### 本番
- ファイル: `docker-compose.prod.yml`
- 構成: `app` + `db(PostgreSQL)` + `reverse_proxy(Apache)`
- 公開:
  - `http://150.19.10.214` -> `https://oc-stamp.cc.it-hiroshima.ac.jp` へリダイレクト
  - `https://oc-stamp.cc.it-hiroshima.ac.jp` でアプリ提供

## 主要ファイル

- `Dockerfile`
  - マルチステージビルド
  - 依存パッケージを builder で解決して runtime を軽量化
  - 非 root ユーザーで実行
- `mysite/entrypoint.prod.sh`
  - DB ポート到達待機
  - `migrate` -> `collectstatic` -> `gunicorn` 起動
- `apache/app.conf`
  - `*:80` は HTTPS へ 301 リダイレクト
  - `*:443` は Django へリバースプロキシ
  - `/static/` `/media/` は Apache が直接配信
- `.env` / `.env.example`
  - Django / DB / Gunicorn / 証明書パスを一元管理

## セットアップ手順

### 1. 環境変数を作成

```powershell
cd c:\my_project\stanp_rally\DjangoTutorial
Copy-Item .env.example .env
```

`.env` で最低限以下を更新してください。

- `SECRET_KEY`
- `DB_PASSWORD`
- `LETSENCRYPT_LIVE_DIR`

### 2. 開発環境の起動

```powershell
docker compose up -d --build
docker compose logs -f app
```

### 3. 本番構成の起動

```powershell
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f app
docker compose -f docker-compose.prod.yml logs -f reverse_proxy
```

## 運用コマンド

```powershell
# 本番構成の停止
docker compose -f docker-compose.prod.yml down

# 本番構成の再起動
docker compose -f docker-compose.prod.yml restart

# DB を含めて全削除（注意: データ消去）
docker compose -f docker-compose.prod.yml down -v

# マイグレーション手動実行
docker compose -f docker-compose.prod.yml exec app python manage.py migrate

# 管理ユーザー作成
docker compose -f docker-compose.prod.yml exec app python manage.py createsuperuser
```

## トラブルシューティング

### HTTPS で接続できない
- `docker compose -f docker-compose.prod.yml logs reverse_proxy` を確認
- `.env` の `LETSENCRYPT_LIVE_DIR` が実在するか確認
- `fullchain.pem` / `privkey.pem` のパスが正しいか確認

### 502 / 503 / 504 が返る
- `docker compose -f docker-compose.prod.yml logs app` を確認
- `docker compose -f docker-compose.prod.yml logs db` を確認
- DB 接続情報（`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`）を再確認

### DB が起動後にアプリが失敗する
- `entrypoint.prod.sh` は DB ポート待機を実施するため、DB 側の認証エラーを疑う
- `docker compose -f docker-compose.prod.yml exec app env` で環境変数を確認

## セキュリティチェック

- `DEBUG=False`
- `SECRET_KEY` を強固な値に変更
- `DB_PASSWORD` を強固な値に変更
- `ALLOWED_HOSTS` に公開ドメイン/IPのみを設定
- 証明書の自動更新（`certbot renew`）をサーバー側で有効化
