"""
URL ルーティング設定。
ルート('/') は myapp のホームへ接続します。
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # ルート('/') を myapp のホーム画面へ
    path('', include('myapp.urls')),
]

# 開発環境でメディアを配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
