"""
mysite の設定ファイル。

開発用の基本設定です。必要に応じて調整してください。
詳しくは Django のドキュメントを参照してください。

Docker 対応: 環境変数から設定を読み込み
"""

import os
from pathlib import Path

# パス設定: `BASE_DIR / 'subdir'` のように使用します。
BASE_DIR = Path(__file__).resolve().parent.parent


# 開発向けの簡易設定（本番には不向き）
# 本番のチェックリスト: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# セキュリティ: 本番では SECRET_KEY を安全に管理してください。
# Docker: .env ファイルまたは環境変数から読み込み
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-85$^3&)w#-9dw$(07#fb==v(8i9g4sghhjee9m)xqn=nju=8zw'
)

# 本番では DEBUG を無効にしてください。
# Docker: 環境変数 DEBUG=False で無効化
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS を環境変数から読み込み（カンマ区切り）
# 例: ALLOWED_HOSTS=localhost,127.0.0.1,app
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,app'
).split(',')


# アプリケーション設定

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # myapp: ホーム画面などアプリ本体のコードを格納
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# データベース設定
# 詳細: https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# Docker: PostgreSQL との互換性を保つために環境変数対応

db_engine = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')

if 'postgresql' in db_engine:
    # PostgreSQL（本番推奨）
    DATABASES = {
        'default': {
            'ENGINE': db_engine,
            'NAME': os.environ.get('DB_NAME', 'mydatabase'),
            'USER': os.environ.get('DB_USER', 'myuser'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'mypassword'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # SQLite（開発用）
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# パスワード検証
# 詳細: https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 国際化設定
# 詳細: https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# 静的ファイル（CSS/JS/画像）
# 詳細: https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
# Docker 本番: collectstatic の出力先を指定
STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR / 'staticfiles')

# メディア（アップロード画像）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
