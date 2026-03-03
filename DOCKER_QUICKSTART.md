# Docker クイックスタート

## 📦 必須
- Docker Desktop for Windows（https://www.docker.com/products/docker-desktop）

## 🚀 開発環境の即実行（5分）

```powershell
# 1. プロジェクトフォルダに移動
cd c:\my_project\stanp_rally\DjangoTutorial

# 2. Docker イメージをビルド（初回のみ約3-5分）
docker-compose build

# 3. コンテナを起動
docker-compose up -d

# 4. 起動ログを確認
docker-compose logs -f app

# 5. ブラウザで確認
# http://localhost:8000

# 6. 管理画面でユーザー作成
docker-compose exec app python manage.py createsuperuser
# http://localhost:8000/admin
```

## 📝 日常的なコマンド

```powershell
# ログを表示
docker-compose logs --tail 100 app

# コンテナ内でコマンド実行
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py shell

# コンテナを一時停止
docker-compose stop

# 再開
docker-compose start

# 完全に削除（データがリセット）
docker-compose down -v

# イメージを再ビルド（コード編集後）
docker-compose build --no-cache
docker-compose up -d
```

## 📊 トラブル対応

| 問題 | 解決策 |
|------|--------|
| ポート 8000 が使用中 | 別のターミナルで `docker-compose down`：または `docker-compose.yml` の `ports:` を変更 |
| マイグレーション失敗 | `docker-compose exec app python manage.py migrate --verbosity 2` でエラーを確認 |
| コードが反映されない | `docker-compose build --no-cache && docker-compose up -d` で再ビルド |
| 権限エラー | `docker-compose down -v` で完全リセット |

## 🔐 本番環境へのデプロイ

```powershell
# 1. 環境変数の設定
Copy-Item .env.example .env
# .env を編集して本番情報を入力

# 2. 本番イメージのビルド
docker-compose -f docker-compose.prod.yml build

# 3. 起動
docker-compose -f docker-compose.prod.yml up -d

# 4. ログ監視
docker-compose -f docker-compose.prod.yml logs -f
```

## 📚 詳細ガイド
👉 [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) を参照
