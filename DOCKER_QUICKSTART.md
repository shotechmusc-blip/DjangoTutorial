# Docker クイックスタート

## 必須
- Docker Desktop for Windows
- 証明書取得済み（Let's Encrypt）
	- `/etc/letsencrypt/live/oc-stamp.cc.it-hiroshima.ac.jp/fullchain.pem`
	- `/etc/letsencrypt/live/oc-stamp.cc.it-hiroshima.ac.jp/privkey.pem`

## 開発環境（ローカル）

```powershell
# 1. プロジェクトへ移動
cd c:\my_project\stanp_rally\DjangoTutorial

# 2. 起動（ビルド込み）
docker compose up -d --build

# 3. アプリログ確認
docker compose logs -f app

# 4. アクセス
# http://localhost:8000
```

## 本番相当環境（HTTPS + Apache + PostgreSQL）

```powershell
# 1. 環境変数テンプレートをコピー
Copy-Item .env.example .env

# 2. .env を編集
# SECRET_KEY / DB_PASSWORD / LETSENCRYPT_LIVE_DIR を本番値に変更

# 3. 本番構成を起動
docker compose -f docker-compose.prod.yml up -d --build

# 4. 状態確認
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f app
docker compose -f docker-compose.prod.yml logs -f reverse_proxy
```

## アクセス確認
- `http://150.19.10.214` は `https://oc-stamp.cc.it-hiroshima.ac.jp` にリダイレクト
- `https://oc-stamp.cc.it-hiroshima.ac.jp` でアプリ表示

## よく使うコマンド

```powershell
# 停止
docker compose down
docker compose -f docker-compose.prod.yml down

# DB含め完全削除（注意: データ消去）
docker compose -f docker-compose.prod.yml down -v

# マイグレーションを手動実行
docker compose -f docker-compose.prod.yml exec app python manage.py migrate

# 管理ユーザー作成
docker compose -f docker-compose.prod.yml exec app python manage.py createsuperuser
```

## 詳細
詳細は `DOCKER_GUIDE.md` を参照してください。
