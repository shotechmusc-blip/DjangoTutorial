"""
mysite の設定ファイル。

開発用の基本設定です。必要に応じて調整してください。
詳しくは Django のドキュメントを参照してください。
"""

from pathlib import Path

# パス設定: `BASE_DIR / 'subdir'` のように使用します。
BASE_DIR = Path(__file__).resolve().parent.parent


# 開発向けの簡易設定（本番には不向き）
# 本番のチェックリスト: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# セキュリティ: 本番では SECRET_KEY を安全に管理してください。
SECRET_KEY = 'django-insecure-85$^3&)w#-9dw$(07#fb==v(8i9g4sghhjee9m)xqn=nju=8zw'

# 本番では DEBUG を無効にしてください。
DEBUG = True

ALLOWED_HOSTS = []


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

# メディア（アップロード画像）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
