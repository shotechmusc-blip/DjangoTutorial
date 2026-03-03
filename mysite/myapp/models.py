from django.db import models


class StampRally(models.Model):
	"""スタンプラリー本体（名称・説明）"""
	title = models.CharField(max_length=100)             # ラリー名
	description = models.TextField(blank=True)           # 説明（任意）
	created_at = models.DateTimeField(auto_now_add=True) # 作成日時
	updated_at = models.DateTimeField(auto_now=True)     # 更新日時

	def __str__(self):
		return self.title


class Floor(models.Model):
	"""建物のフロア（1F〜5F）"""
	name = models.CharField(max_length=20)               # 表示名（例: 1F）
	order = models.PositiveIntegerField(default=1)       # 並び順（1が最上）
	floor_image = models.ImageField(upload_to='floor_images/', null=True, blank=True)

	class Meta:
		ordering = ["order"]

	def __str__(self):
		return self.name


class Spot(models.Model):
	"""各会場スポット（パスワードで押印）"""
	rally = models.ForeignKey(StampRally, related_name="spots", on_delete=models.CASCADE)  # 所属ラリー
	floor = models.ForeignKey(Floor, related_name="spots", on_delete=models.SET_NULL, null=True, blank=True)  # 所属フロア
	name = models.CharField(max_length=100)              # スポット名
	passcode = models.CharField(max_length=32)           # 紙に記載のパスワード
	order = models.PositiveIntegerField(default=0)       # 表示順
	icon = models.ImageField(upload_to='spot_icons/', null=True, blank=True)  # スタンプ用アイコン画像（任意）

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.name}"


class Stamp(models.Model):
	"""押印記録（暫定の訪問者IDで管理）"""
	spot = models.ForeignKey(Spot, on_delete=models.CASCADE)     # 押したスポット
	visitor_id = models.CharField(max_length=64)                 # 訪問者ID（セッション等で生成）
	created_at = models.DateTimeField(auto_now_add=True)         # 押印日時

	class Meta:
		unique_together = ("spot", "visitor_id")               # 同一訪問者の同一スポット重複禁止

	def __str__(self):
		return f"{self.visitor_id} - {self.spot.name}"


class Event(models.Model):
	"""スポットに紐付くイベント情報"""
	spot = models.ForeignKey(Spot, related_name="events", on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	start_at = models.DateTimeField(null=True, blank=True)
	end_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["start_at", "id"]

	def __str__(self):
		return f"{self.title} (@{self.spot.name})"
	
class SSOUser(models.Model):
	external_id = models.CharField(max_length=255,unique=True)
	created_at  = models.DateTimeField(auto_now_add=True)

	#人間に見せるための表現を決めているだけ。なぜならオブジェクトで表示したらわけわからない文字になるから
	def __str__(self):
		return self.external_id

class Character(models.Model):
	"""
	擬人化キャラクター（スタンプに割り当てられる）
	
	設計理由：
	- Spot（スタンプ）との1:1関連付けで、スタンプ押下時の画像解放機能を実現
	- 画像（本物とシルエット）をDB管理し、admin画面で簡単に追加・編集可能
	- order フィールドで表示順序を制御し、複数キャラクターを柔軟に管理
	- 説明文を DB に保持することで、テンプレートのハードコード化を回避
	"""
	spot = models.OneToOneField(Spot, on_delete=models.CASCADE, related_name='character')  # スタンプへの1:1関連付け
	name = models.CharField(max_length=100)              # キャラクター名
	image = models.ImageField(upload_to='characters/')   # 本物の画像
	silhouette_image = models.ImageField(upload_to='characters/silhouettes/')  # シルエット画像
	description = models.TextField(blank=True)           # キャラクターの説明
	order = models.PositiveIntegerField(default=0)       # 表示順序（低い順に表示）
	created_at = models.DateTimeField(auto_now_add=True) # 作成日時
	updated_at = models.DateTimeField(auto_now=True)     # 更新日時

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.name} (#{self.spot.id})"	
