from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    # ホーム
    path('', views.home, name='home'),
    # マップ（フロア一覧→詳細）
    path('map/', views.map_index, name='map_index'),
    path('map/<int:floor_id>/', views.floor_detail, name='floor_detail'),
    # スタンプカード
    path('card/', views.card, name='card'),
    # スポット詳細（押印）
    path('spot/<int:spot_id>/', views.spot_detail, name='spot_detail'),
    # 擬人化キャラクター
    path('characters/', views.characters, name='characters'),
    path("sso/login",views.sso_login,name="sso_login"),
]
