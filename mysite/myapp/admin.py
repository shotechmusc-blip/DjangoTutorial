from django.contrib import admin
from .models import StampRally, Floor, Spot, Stamp, Event, SSOUser, Character

"""管理画面にモデルを登録（データ確認用）"""

admin.site.register(StampRally)

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
	list_display = ("name", "order", "has_image")
	list_editable = ("order",)

	def has_image(self, obj):
		return bool(obj.floor_image)
	has_image.boolean = True
	has_image.short_description = "画像あり"


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
	list_display = ("name", "floor", "order", "has_icon")
	list_filter = ("floor",)
	search_fields = ("name",)

	def has_icon(self, obj):
		return bool(obj.icon)
	has_icon.boolean = True
	has_icon.short_description = "画像あり"


admin.site.register(Stamp)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ("title", "spot", "start_at", "end_at")
	list_filter = ("spot",)
	search_fields = ("title", "description")

@admin.register(SSOUser)
class SSoUserAdmin(admin.ModelAdmin):
	list_display = ["external_id","created_at"]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	"""
	擬人化キャラクター管理画面
	
	UI設計理由：
	- list_display: 一覧画面で essentials（名前・スタンプ・順序・説明プレビュー）を表示
	- readonly_fields: created_at, updated_at はユーザに編集させない
	- fieldsets: 関連フィールドをグループ化し、フォームの可読性を向上
	- image_preview, silhouette_preview: 画像アップロード前の確認機能
	"""
	list_display = ("name", "spot", "order", "has_images", "description_preview")
	list_filter = ("order", "created_at")
	search_fields = ("name", "description")
	list_editable = ("order",)
	readonly_fields = ("created_at", "updated_at", "image_preview", "silhouette_preview")

	fieldsets = (
		("基本情報", {
			"fields": ("spot", "name", "order"),
		}),
		("画像管理", {
			"fields": ("image", "image_preview", "silhouette_image", "silhouette_preview"),
			"description": "本物の画像とシルエット画像をアップロードしてください。",
		}),
		("説明", {
			"fields": ("description",),
		}),
		("メタデータ", {
			"fields": ("created_at", "updated_at"),
			"classes": ("collapse",),
		}),
	)

	def has_images(self, obj):
		"""画像の有無を表示"""
		return bool(obj.image and obj.silhouette_image)
	has_images.boolean = True
	has_images.short_description = "画像完備"

	def description_preview(self, obj):
		"""説明文をプレビュー（最初の50文字）"""
		if obj.description:
			return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
		return "（説明なし）"
	description_preview.short_description = "説明プレビュー"

	def image_preview(self, obj):
		"""本物の画像を管理画面で表示"""
		if obj.image:
			return f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px;" />'
		return "（未設定）"
	image_preview.allow_tags = True
	image_preview.short_description = "本物の画像プレビュー"

	def silhouette_preview(self, obj):
		"""シルエット画像を管理画面で表示"""
		if obj.silhouette_image:
			return f'<img src="{obj.silhouette_image.url}" style="max-width: 200px; max-height: 200px;" />'
		return "（未設定）"
	silhouette_preview.allow_tags = True
	silhouette_preview.short_description = "シルエット画像プレビュー"
