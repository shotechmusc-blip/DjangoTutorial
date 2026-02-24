from django.contrib import admin
from .models import StampRally, Floor, Spot, Stamp, Event,SSOUser

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
