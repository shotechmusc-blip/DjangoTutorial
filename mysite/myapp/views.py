from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import models
import uuid
from .models import StampRally, Floor, Spot, Stamp, Event, SSOUser, Character

def home(request):
	"""
	ホーム画面を表示します。
	ヘッダーとボディの要素（アイコン、進捗バー、区切り、ボタン）を読み込みます。
	"""
	return render(request, 'myapp/home.html')


def _get_visitor_id(request):
	#ユーザのリクエスト内にあるsession["visitor_id"]を取得
	vid = request.session.get('visitor_id')
	#もし辞書に存在しなければ、
	if not vid:
		#作成
		vid = uuid.uuid4().hex
		#作成したものをsession辞書に登録
		request.session['visitor_id'] = vid
	return vid


def map_index(request):
	"""マップ画面：フロアの一覧（1F〜5F）を表示します。"""
	floors = Floor.objects.order_by('order')
	return render(request, 'myapp/map_index.html', {
		'floors': floors,
		'back_url': reverse('home'),
	})


def floor_detail(request, floor_id: int):
	"""フロア詳細：平面図画像（後で実画像に差し替え）を表示します。"""
	floor = get_object_or_404(Floor, id=floor_id)
	return render(request, 'myapp/floor_detail.html', {
		'floor': floor,
		'back_url': reverse('map_index'),
	})


def card(request):
	"""
	スタンプカード画面：カード（上部）＋スポット一覧（下部）＋進捗%表示。
	"""
	_get_visitor_id(request)

	rally = StampRally.objects.first()
	spots = Spot.objects.select_related('floor').order_by('floor__order', 'order', 'id')
	total = spots.count()
	vid = request.session['visitor_id']
	stamped_qs = Stamp.objects.filter(visitor_id=vid).select_related('spot').order_by('created_at', 'id')
	stamped_count = stamped_qs.count()
	# 進捗はカードのスロット数（4個）を分母にする
	base_slots = 4  # 4個の2×2グリッド配置で固定
	denom = base_slots
	progress = int((min(stamped_count, denom) / denom) * 100) if denom else 0

	# 直前押印の簡易アニメーション用フラグ
	last_stamped_id = request.GET.get('stamped')

	# スロット（表示用）：スポットが0でも固定グリッドの空丸を表示
	slot_count = denom
	slots = []
	# 押印順にカード穴を埋め、残りは空欄にする
	for i in range(slot_count):
		if i < stamped_count:
			st = stamped_qs[i]
			s = st.spot
			slots.append({
				'spot_id': s.id,
				'name': s.name,
				'icon_url': (s.icon.url if s.icon else None),
				'filled': True,
			})
		else:
			slots.append({
				'spot_id': None,
				'name': '',
				'icon_url': None,
				'filled': False,
			})

	# すべてのスタンプが埋まったかを判定
	is_all_stamped = stamped_count >= denom

	return render(request, 'myapp/card.html', {
		'rally': rally,
		'spots': spots,
		'slots': slots,
		'progress': progress,
		'last_stamped_id': last_stamped_id,
		'is_all_stamped': is_all_stamped,
		'back_url': reverse('home'),
	})


def spot_detail(request, spot_id: int):
	"""
	スポット詳細：QR（後で追加）／パスワード入力で押印、イベント詳細ボタンを表示。
	POSTで正しいパスワードが送信されたら押印してカードへ戻します。
	"""
	_get_visitor_id(request)
	spot = get_object_or_404(Spot, id=spot_id)
	# 紐付くイベント一覧
	events = Event.objects.filter(spot=spot).order_by('start_at', 'id')

	message = None
	if request.method == 'POST':
		input_code = request.POST.get('passcode', '').strip()
		if input_code and input_code == spot.passcode:
			Stamp.objects.get_or_create(spot=spot, visitor_id=request.session['visitor_id'])
			# カード画面へ戻り、直前押印スポットをクエリで渡す（簡易アニメーション用）
			return redirect(f"{reverse('card')}?stamped={spot.id}")
		else:
			message = 'パスコードが違います。紙に記載のコードを入力してください。'

	return render(request, 'myapp/spot_detail.html', {
		'spot': spot,
		'message': message,
		'events': events,
		'back_url': reverse('card'),
	})

def characters(request):
	"""
	擬人化キャラクター画面：DB登録されたキャラクターを表示します。
	スタンプ押下でシルエット画像から本物の画像に置き換え、説明を表示します。
	
	設計：
	- Character モデルから全キャラクターを取得（order順）
	- テンプレートで動的に描画し、admin画面での管理を容易に
	- 訪問者IDごとのスタンプ状態をJSで管理（後後バックエンド連携可能）
	"""
	_get_visitor_id(request)
	
	# DBからキャラクターを取得（order順）
	characters = Character.objects.select_related('spot').order_by('order', 'id')
	
	# 訪問者の押印済みスタンプを取得（集合化して高速判定）
	vid = request.session['visitor_id']
	stamped_spots = set(
		Stamp.objects.filter(visitor_id=vid).values_list('spot_id', flat=True)
	)
	
	# キャラクターデータにスタンプ押下情報をマージ
	character_data = []
	for char in characters:
		character_data.append({
			'id': char.id,
			'name': char.name,
			'description': char.description,
			'image_url': char.image.url if char.image else None,
			'silhouette_url': char.silhouette_image.url if char.silhouette_image else None,
			'stamp_id': char.spot.id,
			'is_stamped': char.spot.id in stamped_spots,
		})
	
	return render(request, 'myapp/characters.html', {
		'characters': character_data,
		'back_url': reverse('home'),
	})


def sso_login(request):
	#中本先輩のサイトからこちらにアクセスしてくるとき?id=xxxからIDを取得する
	external_id = request.GET.get("id")

	# 正しくIDが取得できれば以下の処理を実行する
	if external_id:

		sso_user,created = SSOUser.objects.get_or_create(external_id=external_id)
		#訪問者IDをsession辞書に保存
		request.session["visitor_id"] = str(sso_user.id)
		return redirect(reverse("card")) #カード画面へリダイレクト

	return redirect(reverse("home"))