"""Rebuild Phase 1.2 from hand-curated, sense-restricted seeds.

No learner texts are generated. Rank is a stable identifier order, not corpus frequency.
"""
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'config/languages/ko/k1'

# lemma | sense | central Japanese gloss; optional POS override
CORE = {
'reference': ('pronoun', 'communication', '''
나|i_informal|私（普通形）
저|i_humble|私（謙譲）
너|you_informal|あなた（親しい相手）
우리|we|私たち
여기|here|ここ
거기|there_near_listener|そこ
저기|there_over_there|あそこ
이것|this_thing|これ
그것|that_thing|それ
저것|that_thing_over_there|あれ
누구|who|誰
뭐|what_colloquial|何（口語）
무엇|what|何
어디|where|どこ
언제|when|いつ|adverb
왜|why|なぜ|adverb
어떻게|how|どのように|adverb
어느|which|どの|determiner
같이|together|一緒に|adverb
모두|all_together|みんなで・全部|adverb
'''),
'people': ('noun', 'family', '''
사람|person|人
친구|friend|友達
가족|family|家族
아버지|father|父
어머니|mother|母
아들|son|息子
딸|daughter|娘
형|older_brother_male|兄（男性から）
오빠|older_brother_female|兄（女性から）
누나|older_sister_male|姉（男性から）
언니|older_sister_female|姉（女性から）
동생|younger_sibling|弟・妹
남자|man|男性
여자|woman|女性
아이|child|子ども
학생|student|学生
선생님|teacher|先生
손님|guest_customer|客
이름|name|名前
나라|country|国
한국|korea|韓国
'''),
'places': ('noun', 'place', '''
집|home|家
학교|school|学校
회사|company|会社
가게|shop|店
식당|restaurant|食堂・飲食店
카페|cafe|カフェ
병원|hospital|病院
은행|bank|銀行
시장|market|市場
공원|park|公園
도서관|library|図書館
화장실|restroom|トイレ
방|room|部屋
교실|classroom|教室
길|road|道
거리|street|通り
역|station|駅
밖|outside|外
안|inside|中
앞|front|前
뒤|back|後ろ
옆|side|横
위|above|上
아래|below|下
곳|place|場所
도시|city|都市
'''),
'time': ('noun', 'time', '''
오늘|today|今日
어제|yesterday|昨日
내일|tomorrow|明日
지금|now|今|adverb
아침|morning|朝
점심|lunch|昼食
저녁|evening|夕方・晩
밤|night|夜
시간|time|時間（時刻・時間の長さ）
시|clock_hour|時（時刻の単位）|counter
분|minute|分（時間の単位）|counter
주|week_unit|週（単位）|counter
월|calendar_month|月（暦の月）|counter
년|year_unit|年（単位）|counter
날|day|日
하루|one_day|一日
주말|weekend|週末
월요일|monday|月曜日
화요일|tuesday|火曜日
수요일|wednesday|水曜日
목요일|thursday|木曜日
금요일|friday|金曜日
토요일|saturday|土曜日
일요일|sunday|日曜日
봄|spring|春
여름|summer|夏
가을|autumn|秋
겨울|winter|冬
처음|first_time|初め
마지막|last|最後
때|time_occasion|時
매일|every_day|毎日|adverb
일찍|early|早く|adverb
'''),
'daily_objects': ('noun', 'object', '''
책|book|本
공책|notebook|ノート
종이|paper|紙
사진|photo|写真
전화|telephone|電話
휴대폰|mobile_phone|携帯電話
컴퓨터|computer|コンピューター
텔레비전|television|テレビ
문|door|扉
창문|window|窓
의자|chair|椅子
책상|desk|机
침대|bed|ベッド
가방|bag|かばん
옷|clothes|服
신발|shoes|靴
우산|umbrella|傘
돈|money|お金
물|water|水
밥|cooked_rice_meal|ご飯（炊いた米・日常の食事）
빵|bread|パン
과일|fruit|果物
사과|apple|リンゴ
고기|meat|肉
채소|vegetable|野菜
커피|coffee|コーヒー
차|tea|お茶
우유|milk|牛乳
음식|food|食べ物
선물|gift|贈り物
문제|problem|問題
답|answer|答え
말|speech|言葉・発言
이야기|story_talk|話
일|work|仕事・作業
공부|study|勉強
숙제|homework|宿題
시험|exam|試験
운동|exercise|運動
음악|music|音楽
영화|movie|映画
수업|class_lesson|授業
자리|seat|席
'''),
'transport_nature': ('noun', 'nature', '''
버스|bus|バス
지하철|subway|地下鉄
택시|taxi|タクシー
자동차|car|自動車
자전거|bicycle|自転車
기차|train|列車
여행|trip|旅行
날씨|weather|天気
비|rain|雨
눈|snow|雪
바람|wind|風
해|sun|太陽
하늘|sky|空
산|mountain|山
바다|sea|海
꽃|flower|花
나무|tree|木
동물|animal|動物
개|dog|犬
고양이|cat|猫
색|color|色
파랑|blue_color|青（色名）
가격|price|価格
생일|birthday|誕生日
약속|appointment_promise|約束
한국어|korean_language|韓国語
'''),
'verbs': ('verb', 'action', '''
가다|go|行く
오다|come|来る
먹다|eat|食べる
마시다|drink|飲む
보다|see_watch|見る
듣다|hear_listen|聞く
말하다|speak|話す
읽다|read|読む
쓰다|write|書く
하다|do|する
있다|exist|いる・ある|adjective
없다|not_exist|いない・ない|adjective
자다|sleep|寝る
일어나다|get_up|起きる
앉다|sit|座る
서다|stand|立つ
걷다|walk|歩く
뛰다|run|走る
만나다|meet|会う
기다리다|wait|待つ
사다|buy|買う
팔다|sell|売る
주다|give|あげる・渡す
받다|receive|受け取る
열다|open|開ける
닫다|close|閉める
입다|wear_clothes|服を着る
벗다|take_off|脱ぐ
타다|ride|乗る
내리다|get_off|降りる
시작하다|start|始める
끝나다|end_intransitive|終わる
공부하다|study|勉強する
일하다|work|働く
운동하다|exercise|運動する
좋아하다|like|好きである
싫어하다|dislike|嫌う
알다|know|知っている
모르다|not_know|知らない
배우다|learn|学ぶ
가르치다|teach|教える
찾다|find_look_for|探す・見つける
잃다|lose|失う
빌리다|borrow|借りる
돌아가다|go_back|帰る（元の場所へ行く）
들어가다|go_in|入る（向こうへ）
나가다|go_out|出る（向こうへ）
만들다|make|作る
씻다|wash|洗う
요리하다|cook|料理する
전화하다|phone|電話する
사용하다|use|使う
필요하다|necessary|必要である|adjective
살다|live_reside|住む・暮らす
쉬다|rest|休む
도와주다|help|手伝う
생각하다|think|考える
웃다|laugh_smile|笑う
넣다|put_in|入れる
찍다|take_photo|写真を撮る
도착하다|arrive|到着する
출발하다|depart|出発する
'''),
'adjectives': ('adjective', 'description', '''
좋다|good|よい
싫다|unpleasant|嫌だ
크다|big|大きい
작다|small|小さい
많다|many|多い
적다|few|少ない
길다|long|長い
짧다|short|短い
높다|high|高い（高さ）
빠르다|fast|速い
느리다|slow|遅い（速度）
쉽다|easy|易しい
어렵다|difficult|難しい
재미있다|interesting|面白い
재미없다|uninteresting|面白くない
맛있다|tasty|おいしい
맛없다|not_tasty|おいしくない
비싸다|expensive|高い（値段）
싸다|cheap|安い
덥다|hot_weather|暑い
춥다|cold_weather|寒い
따뜻하다|warm|暖かい
시원하다|cool_refreshing|涼しい
바쁘다|busy|忙しい
피곤하다|tired|疲れている
아프다|hurt_sick|痛い・具合が悪い
예쁘다|pretty|きれい・かわいい
깨끗하다|clean|清潔だ
같다|same|同じだ
늦다|late|遅い（時間）
다르다|different|違う
'''),
'adverbs': ('adverb', 'description', '''
아주|very|とても
너무|too|あまりに（過度に）
정말|really|本当に
잘|well|うまく
많이|a_lot|たくさん
조금|a_little|少し
빨리|quickly|速く
천천히|slowly|ゆっくり
자주|often|よく（頻度）
가끔|sometimes|時々
항상|always|いつも
다시|again|また（再度）
먼저|first|先に
그리고|and_then|そして|conjunction
하지만|however|しかし|conjunction
또|also_again|また・さらに
그래서|so|それで|conjunction
그런데|but_then|ところが・ところで|conjunction
'''),
'numbers': ('numeral', 'quantity', '''
하나|one_native|一つ
둘|two_native|二つ
셋|three_native|三つ
넷|four_native|四つ
다섯|five_native|五つ
여섯|six_native|六つ
일곱|seven_native|七つ
여덟|eight_native|八つ
아홉|nine_native|九つ
열|ten_native|十（固有数詞）
일|one_sino|一
이|two_sino|二
삼|three_sino|三
사|four_sino|四
오|five_sino|五
육|six_sino|六
칠|seven_sino|七
팔|eight_sino|八
구|nine_sino|九
십|ten_sino|十（漢数詞）
'''),
}

# Every category is ordered E1, E2, E3; exact hand-curated quotas are checked.
EXPANSION = {
'people_social': ('noun', ['family', 'communication'], (15,15,10), '''
엄마|mom|お母さん（親しい呼び方）
아빠|dad|お父さん（親しい呼び方）
부모|parents|両親
할머니|grandmother|祖母
할아버지|grandfather|祖父
남편|husband|夫
아내|wife|妻
아기|baby|赤ちゃん
이웃|neighbor|隣人
의사|doctor|医師
직원|employee|店員・職員
어른|adult|大人
어린이|child_age_group|子ども（年齢層）
여러분|you_plural|皆さん|pronoun
자기|self|自分|pronoun
부부|married_couple|夫婦
형제|siblings|兄弟
남동생|younger_brother|弟
여동생|younger_sister|妹
친척|relative|親戚
사촌|cousin|いとこ
동료|colleague|同僚
주인|owner|店・物の持ち主
간호사|nurse|看護師
경찰|police|警察（警察官）
기사|driver|運転手
요리사|cook_person|料理人
회사원|office_worker|会社員
외국인|foreigner|外国人
팀|team|チーム
누군가|someone|誰か|pronoun
조부모|grandparents|祖父母
조카|niece_nephew|おい・めい
초등학생|elementary_pupil|小学生
중학생|middle_school_student|中学生
고등학생|high_school_student|高校生
대학생|university_student|大学生
가수|singer|歌手
배우|actor|俳優
관계|relationship|人と人の関係
'''),
'places_objects': ('noun', ['place', 'object'], (35,35,20), '''
부엌|kitchen|台所
거실|living_room|居間
아파트|apartment_building|集合住宅
냉장고|refrigerator|冷蔵庫
컵|cup|コップ
접시|plate|皿
숟가락|spoon|スプーン
젓가락|chopsticks|箸
그릇|bowl|器
수건|towel|タオル
비누|soap|石けん
칫솔|toothbrush|歯ブラシ
치약|toothpaste|歯磨き粉
열쇠|key|鍵
지갑|wallet|財布
시계|clock_watch|時計
안경|glasses|眼鏡
모자|hat|帽子
양말|socks|靴下
바지|trousers|ズボン
치마|skirt|スカート
셔츠|shirt|シャツ
연필|pencil|鉛筆
펜|pen|ペン
지우개|eraser|消しゴム
상자|box|箱
봉지|bag_packet|袋
약국|pharmacy|薬局
마트|supermarket|スーパー
편의점|convenience_store|コンビニ
우체국|post_office|郵便局
호텔|hotel|ホテル
입구|entrance|入口
출구|exit|出口
계단|stairs|階段
엘리베이터|elevator|エレベーター
층|floor_storey|階（建物の階）|counter
건물|building|建物
동네|neighborhood|近所の地域
마을|village|村
고향|hometown|故郷
놀이터|playground|遊び場
주차장|parking_lot|駐車場
빵집|bakery|パン屋
미용실|hair_salon|美容室
세탁기|washing_machine|洗濯機
청소기|vacuum_cleaner|掃除機
에어컨|air_conditioner|エアコン
선풍기|electric_fan|扇風機
소파|sofa|ソファ
이불|bedding|掛け布団
베개|pillow|枕
거울|mirror|鏡
쓰레기|trash|ごみ
쓰레기통|trash_bin|ごみ箱
장갑|gloves|手袋
목도리|scarf|マフラー
코트|coat|コート
운동화|sneakers|運動靴
구두|dress_shoes|革靴
주머니|pocket|ポケット
냄비|pot|鍋
프라이팬|frying_pan|フライパン
칼|knife|包丁・ナイフ
포크|fork|フォーク
침실|bedroom|寝室
욕실|bathroom|浴室
식탁|dining_table|食卓
가위|scissors|はさみ
풀|glue|のり（接着剤）
테이프|adhesive_tape|粘着テープ
지도|map|地図
벽|wall|壁
바닥|floor_surface|床
천장|ceiling|天井
문구점|stationery_shop|文房具店
세탁소|laundry_shop|クリーニング店
동물원|zoo|動物園
수영장|swimming_pool|プール
미술관|art_museum|美術館
박물관|museum|博物館
운동장|sports_ground|運動場
섬|island|島
골목|alley|路地
다리|bridge|橋
인형|doll|人形
장난감|toy|おもちゃ
반지|ring_jewelry|指輪
목걸이|necklace|ネックレス
샴푸|shampoo|シャンプー
'''),
'food_nature': ('noun', ['food', 'nature'], (22,20,8), '''
달걀|egg|卵
생선|fish_food|魚（食材）
닭고기|chicken_meat|鶏肉
돼지고기|pork|豚肉
소고기|beef|牛肉
쌀|uncooked_rice|米
국|soup|スープ
김치|kimchi|キムチ
라면|ramyeon|ラーメン（韓国の即席麺）
김밥|gimbap|のり巻き
주스|juice|ジュース
바나나|banana|バナナ
오렌지|orange|オレンジ
딸기|strawberry|イチゴ
포도|grape|ブドウ
토마토|tomato|トマト
감자|potato|ジャガイモ
당근|carrot|ニンジン
양파|onion|タマネギ
소금|salt|塩
설탕|sugar|砂糖
구름|cloud|雲
치즈|cheese|チーズ
요구르트|yogurt|ヨーグルト
과자|snack|菓子
아이스크림|ice_cream|アイスクリーム
케이크|cake|ケーキ
초콜릿|chocolate|チョコレート
오이|cucumber|キュウリ
배|pear|梨
수박|watermelon|スイカ
귤|tangerine|ミカン
버섯|mushroom|キノコ
두부|tofu|豆腐
반찬|side_dish|おかず
고추|chili_pepper|トウガラシ
달|moon|月（天体）
별|star|星
강|river|川
새|bird|鳥
물고기|fish_animal|魚（動物）
토끼|rabbit|ウサギ
감|persimmon|柿
복숭아|peach|桃
고구마|sweet_potato|サツマイモ
떡|rice_cake|餅（韓国の餅）
꿀|honey|蜂蜜
나뭇잎|leaf|木の葉
돌|stone|石
풀|grass|草
'''),
'verbs': ('verb', ['action', 'story_event'], (42,38,20), '''
되다|become|なる
울다|cry|泣く
놀다|play|遊ぶ
보내다|send|送る
대답하다|answer|答える
물어보다|ask|尋ねる
준비하다|prepare|準備する
고르다|choose|選ぶ
놓다|put_down|置く
가지다|have_possess|持つ
가져오다|bring|持ってくる
가져가다|take_along|持っていく
돌아오다|come_back|戻ってくる
들어오다|come_in|入ってくる
나오다|come_out|出てくる
잊다|forget|忘れる
기억하다|remember|覚えている
보이다|be_visible|見える
들리다|be_audible|聞こえる
청소하다|clean|掃除する
빨래하다|do_laundry|洗濯する
끝내다|finish_transitive|終える
켜다|switch_on|つける（電源）
끄다|switch_off|消す（電源）
신다|wear_footwear|靴・靴下を履く
벗기다|remove_clothing|服などを脱がせる
잡다|grasp|つかむ
꺼내다|take_out|取り出す
바꾸다|change_exchange|替える
돌려주다|return_object|返す
빌려주다|lend|貸す
지내다|spend_days|過ごす
이해하다|understand|理解する
연습하다|practice|練習する
걱정하다|worry|心配する
주문하다|order_food|注文する
계산하다|pay_bill|会計する
예약하다|reserve|予約する
인사하다|greet|挨拶する
다니다|attend_regularly|通う
건너다|cross|渡る
넘어지다|fall_over|転ぶ
가져다주다|bring_to_someone|持ってきて渡す
데리다|take_someone_along|人を連れる
따라가다|follow_away|ついていく
따라오다|follow_here|ついてくる
올라가다|go_up|上がっていく
내려가다|go_down|下りていく
오르다|rise_climb|上る
내려오다|come_down|下りてくる
올라오다|come_up|上がってくる
돌다|turn_go_round|回る
돌리다|turn_something|回す
옮기다|move_something|移す
지우다|erase|消す（文字）
버리다|discard|捨てる
모으다|collect|集める
나누다|divide_share|分ける
씹다|chew|かむ
끓이다|boil_transitive|煮る・沸かす
굽다|bake_grill|焼く
자르다|cut|切る
섞다|mix|混ぜる
흘리다|spill|こぼす
떨어지다|fall_drop|落ちる
열리다|open_intransitive|開く
닫히다|close_intransitive|閉まる
고치다|repair|直す
다치다|get_hurt|けがをする
놀라다|be_surprised|驚く
설명하다|explain|説明する
소개하다|introduce|紹介する
초대하다|invite|招待する
방문하다|visit|訪問する
찍다|stamp|印を押す
그리다|draw|描く
노래하다|sing|歌う
춤추다|dance|踊る
수영하다|swim|泳ぐ
산책하다|take_walk|散歩する
밀다|push|押す
당기다|pull|引く
던지다|throw|投げる
줍다|pick_up|拾う
숨다|hide_self|隠れる
숨기다|hide_something|隠す
찾아가다|go_visit|訪ねていく
찾아오다|come_visit|訪ねてくる
이사하다|move_house|引っ越す
돌아다니다|roam|歩き回る
모이다|gather|集まる
헤어지다|part|別れる
싸우다|fight|けんかする
화내다|get_angry|怒る
사과하다|apologize|謝る
약속하다|promise|約束する
찍히다|be_photographed|写真に写る
부르다|call_person|呼ぶ
멈추다|stop|止まる・止める
확인하다|check|確かめる
'''),
'adjectives': ('adjective', ['description', 'emotion'], (28,25,12), '''
괜찮다|okay|大丈夫だ
뜨겁다|hot_object|熱い（物）
차갑다|cold_object|冷たい（物）
배고프다|hungry|お腹がすいている
배부르다|full_after_eating|お腹がいっぱいだ
목마르다|thirsty|喉が渇いている
졸리다|sleepy|眠い
슬프다|sad|悲しい
기쁘다|glad|うれしい
행복하다|happy|幸せだ
무섭다|scary_afraid|怖い
힘들다|tiring_hard|つらい・大変だ
가깝다|near|近い
멀다|far|遠い
낮다|low|低い
무겁다|heavy|重い
가볍다|light_weight|軽い
더럽다|dirty|汚い
조용하다|quiet|静かだ
시끄럽다|noisy|うるさい
밝다|bright|明るい（光）
어둡다|dark|暗い（光）
넓다|wide|広い
좁다|narrow|狭い
편하다|comfortable|楽だ・快適だ
불편하다|uncomfortable|不便だ・不自由だ
친절하다|kind_courteous|親切だ
중요하다|important|大切だ
귀엽다|cute|かわいい
젊다|young|若い
오래되다|old_object|古い（物）
새롭다|new|新しい
건강하다|healthy|健康だ
안전하다|safe|安全だ
위험하다|dangerous|危険だ
빨갛다|red|赤い
복잡하다|complicated|複雑だ
간단하다|simple_easy|簡単だ（手軽だ）
달다|sweet|甘い
짜다|salty|塩辛い
맵다|spicy|辛い
시다|sour|酸っぱい
쓰다|bitter|苦い
부드럽다|soft|柔らかい
딱딱하다|hard_texture|硬い
두껍다|thick|厚い
얇다|thin|薄い
깊다|deep|深い
하얗다|white|白い
비슷하다|similar|似ている
급하다|urgent|急だ
파랗다|blue|青い
부끄럽다|embarrassed|恥ずかしい
화나다|angry|怒っている|verb
심심하다|bored|退屈だ
즐겁다|enjoyable|楽しい
신나다|excited|うきうきする|verb
까맣다|black|黒い
아쉽다|regretful|残念だ
부럽다|envious|うらやましい
친하다|close_relationship|親しい
노랗다|yellow|黄色い
어떻다|how_state|どうだ
이상하다|strange|変だ
미안하다|sorry|申し訳ない
'''),
'adverbs_connectors': ('adverb', ['description', 'communication'], (18,22,10), '''
네|yes|はい|interjection
아니요|no_polite|いいえ|interjection
이|this|この|determiner
그|that|その|determiner
저|that_over_there|あの|determiner
무슨|what_kind|何の・どんな|determiner
몇|how_many|いくつの|determiner
더|more|もっと
덜|less|より少なく
아직|still_yet|まだ
벌써|already|もう（予想より早く）
곧|soon|もうすぐ
이제|now_from_here|今から・もう（今や）
꼭|without_fail|必ず
바로|immediately|すぐに
계속|continuously|続けて
미리|in_advance|前もって
혹시|perhaps_question|もしかして
아마|probably|たぶん
거의|almost|ほとんど
전혀|not_at_all|全く（否定と）
혼자|alone|一人で
서로|each_other|お互いに
직접|directly_personally|自分で直接
갑자기|suddenly|突然
자꾸|repeatedly|何度も（繰り返して）
열심히|diligently|一生懸命
똑바로|straight_correctly|まっすぐ・正しく
조용히|quietly|静かに
특히|especially|特に
보통|usually|普通は
가장|most|最も
제일|most_colloquial|一番
만약|if|もし
왜냐하면|because_intro|なぜなら|conjunction
그러면|then|それなら|conjunction
또는|or|または|conjunction
그래도|nevertheless|それでも|conjunction
오래|long_time|長く
일단|first_for_now|まずは
따로|separately|別々に
함께|together|一緒に
새|new_attributive|新しい|determiner
아무|any_attributive|どんな〜も（否定と）|determiner
점점|increasingly|だんだん
가득|full_to_capacity|いっぱいに
잠깐|briefly|少しの間
차례로|in_order|順番に
마침|just_then|ちょうどその時
결국|eventually|結局
'''),
'time_counters_units': ('noun', ['time', 'quantity'], (16,14,5), '''
오전|am|午前
오후|pm|午後
이번|this_time|今回
다음|next|次
전|before|前（時間）
후|after|後（時間）
달|month_duration|か月（期間）|counter
개|item_unit|個|counter
명|person_unit|人（人数）|counter
살|age_year|歳|counter
번|occurrence_unit|回|counter
잔|cup_unit|杯|counter
병|bottle_unit|本（瓶）|counter
장|sheet_unit|枚|counter
원|won|ウォン|counter
백|hundred|百|numeral
천|thousand|千|numeral
만|ten_thousand|万|numeral
스물|twenty_native|二十（固有数詞）|numeral
마리|animal_unit|匹・羽|counter
대|machine_unit|台|counter
켤레|pair_footwear|足（靴の一組）|counter
봉지|bag_unit|袋（袋の数）|counter
킬로미터|kilometer|キロメートル|counter
미터|meter|メートル|counter
킬로그램|kilogram|キログラム|counter
그램|gram|グラム|counter
초|second_unit|秒|counter
날짜|date|日付
평일|weekday|平日
새벽|dawn|明け方
지난번|last_time|前回
순간|moment|瞬間
권|book_unit|冊|counter
나중|later_time|後（後ほど）
'''),
'abstract_body_emotion': ('noun', ['body', 'emotion'], (15,15,10), '''
몸|body|体
머리|head|頭
눈|eye|目
귀|ear|耳
코|nose|鼻
입|mouth|口
손|hand|手
발|foot|足（足首より先）
다리|leg|脚
배|belly|お腹
마음|mind_feeling|心・気持ち
기분|mood|気分
건강|health|健康
감기|cold_illness|風邪
약|medicine|薬
목|neck_throat|首・喉
어깨|shoulder|肩
팔|arm|腕
등|back_body|背中
이|tooth|歯
얼굴|face|顔
머리카락|hair|髪
피|blood|血
눈물|tear|涙
소리|sound|音
냄새|smell|におい
맛|taste|味
힘|strength|力
생각|thought|考え
걱정|worry|心配
꿈|dream_sleep|夢（睡眠中）
기억|memory|記憶
실수|mistake|間違い（うっかり）
방법|method|方法
이유|reason|理由
계획|plan|計画
도움|help|助け
관심|interest|関心
취미|hobby|趣味
습관|habit|習慣
'''),
'school_work_transport_info': ('noun', ['school', 'work', 'transport', 'communication'], (9,16,5), '''
비행기|airplane|飛行機
공항|airport|空港
정류장|bus_stop|停留所
표|ticket|切符
번호|number_label|番号
주소|address|住所
인터넷|internet|インターネット
메시지|message|メッセージ
단어|word|単語
문장|sentence|文
질문|question|質問
사전|dictionary|辞書
칠판|blackboard|黒板
교과서|textbook|教科書
학년|school_year|学年
방학|school_vacation|学校の長期休暇
휴가|work_vacation|休暇（仕事）
회의|meeting_work|会議
사무실|office|事務室
수학|mathematics|数学
체육|physical_education|体育
미술|art_subject|美術
편지|letter|手紙
이메일|email|電子メール
신호|traffic_signal|信号
횡단보도|crosswalk|横断歩道
기차역|train_station|鉄道の駅
짐|luggage|荷物
영수증|receipt|領収書・レシート
정보|information|情報
'''),
}

def rows(block):
    for line in block.strip().splitlines():
        if line.strip():
            parts = line.strip().split('|')
            assert len(parts) in (3,4), line
            yield parts

def save(name, value):
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def entry(parts, pos, rank, tier, category, tags):
    lemma,sense,gloss = parts[:3]
    pos = parts[3] if len(parts) == 4 else pos
    return dict(id=f'ko_k1_{rank:04}',language='ko',lemma=lemma,pos=pos,
                sense=sense,gloss_ja=gloss,level='K1',tier=tier,rank=rank,
                tags=list(dict.fromkeys(['daily_life',*tags])),
                allow_inflection=pos in ('verb','adjective'),
                introduced_from=None,introduced_to=None,target_exposures=None,
                forms=[],notes=None,category=category,confidence='high')

def build_vocab():
    source=[]
    for category,(pos,tag,block) in CORE.items():
        for parts in rows(block):
            source.append(entry(parts,pos,len(source)+1,'core',category,[tag]))
    assert len(source)==300, len(source)
    save('core_vocab.source.json',source)
    core=json.loads(json.dumps(source))
    replacement=next(e for e in core if e['lemma']=='한국')
    replacement.update(lemma='아니다',pos='adjective',sense='not_be',
                       gloss_ja='〜ではない',allow_inflection=True,category='adjectives',
                       tags=['daily_life','description'],forms=['아니에요'],
                       notes='原案한국を固有名詞台帳へ移動した置換候補。N이/가 아니에요のみ。')
    expansions=[]
    for category,(pos,tags,quotas,block) in EXPANSION.items():
        data=list(rows(block))
        assert len(data)==sum(quotas), (category,len(data),quotas)
        for i,parts in enumerate(data):
            tier='E1' if i<quotas[0] else 'E2' if i<sum(quotas[:2]) else 'E3'
            expansions.append(entry(parts,pos,0,tier,category,tags))
    # Promote essential counters/apology without changing the total tier quotas.
    for e in expansions:
        if e['lemma'] in ('권','미안하다'):e['tier']='E1'
        elif e['lemma'] in ('벗기다','기억하다'):e['tier']='E3'
    # Stable category/priority order within each tier, not alphabetical ordering.
    expansions.sort(key=lambda e:e['tier'])
    assert Counter(e['tier'] for e in expansions)=={'E1':200,'E2':200,'E3':100}
    tier_index=Counter()
    for rank,e in enumerate(expansions,301):
        e.update(id=f'ko_k1_{rank:04}',rank=rank,target_exposures=6)
        index=tier_index[e['tier']];tier_index[e['tier']]+=1
        # Wide candidate windows. A later validator checks global slot feasibility.
        if e['tier']=='E1':
            start,end=1+(index//50)*10,100+(index//50)*20
        elif e['tier']=='E2':
            start,end=61+(index//50)*10,190+(index//50)*20
        else:
            start,end=151+(index//25)*10,220+(index//25)*10
        e.update(introduced_from=start,introduced_to=end)
    annotate(core,expansions)
    apply_phase1_1(core,expansions)
    apply_phase1_2(expansions)
    save('core_vocab.json',core)
    save('expansion_vocab.json',expansions)
    save('proper_names.json', {'counted_in_vocab_budget':False,'entries':[
        {'lemma':'한국','kind':'country','gloss_ja':'韓国','source':'Core原案の41番',
         'notes':'Phase 1.1で予算外への移動を正式採用。事前提示して理解可能にし、無制限の固有名詞追加は避ける。'}]})
    return source,core,expansions

TIER_CHANGES = {
    '기억하다':('E2','記憶保持は学習・約束・忘れ物で再利用でき、E3から前倒し。'),
    '잠깐':('E1','待つ・短時間の行動で高い再利用性。E3から前倒し。'),
    '어떻다':('E1','어때요で状態を簡単に質問できる。E3から前倒し。'),
    '부모':('E2','Core 아버지/어머니/가족とE1 엄마/아빠で初期の家族描写を確保。'),
    '딸기':('E2','特定果物はCore 과일/사과等より導入優先度が低い。'),
    '가장':('E3','K1では제일を優先。K2送り・入替の判断待ちとして後段へ。'),
    '사촌':('E3','親族の細分化は基本の家族語より後段へ。'),
    '고추':('E3','特定食材は日常の基本食材より後段へ。'),
}

# Review proposals are separate from the active 500; no automatic gap filling.
REPLACEMENT_PROPOSALS = [
    ('함께','together','가만히','adverb','without_moving','動かずに',
     'adverbs_connectors','Core 같이とほぼ同義。',
     '静止した状態で待つ・座る等の具体動作を補い、静かな音量の조용히とは区別できる。',
     '副詞義のみ。-아/어 있다等の未許可構文を足さずに使える用例を確認する。'),
    ('조부모','grandparents','아저씨','noun','adult_man_address','おじさん（成人男性の呼称）',
     'people_social','E1 할머니/할아버지で表現できる。',
     '近所・店・交通の人物描写に再利用しやすい具体的呼称。',
     '実際の呼びかけは人物関係と丁寧さを母語話者が確認する。'),
    ('기차역','train_station','시간표','noun','timetable','時間割・時刻表',
     'school_work_transport_info','Core 역との差が小さい。',
     '学校・交通・仕事の予定で使う具体物を補い、既存語の言い換えにならない。',
     '時間の一覧という共通中心義。ジャンル別の用例と意味の範囲を確認する。'),
    ('찍히다','be_photographed','충전하다','verb','charge_battery','充電する',
     'verbs','受動の負荷に対して場面が限定される。',
     '携帯電話・コンピューターを使う家・学校・仕事・旅行で、単純な能動文を作れる。',
     '電気機器の充電のみ。補助構文や専門的な電気説明へ拡張しない。'),
    ('관계','relationship','동갑','noun','same_age','同い年',
     'people_social','抽象的で、具体的な人物関係は既存語で表現できる。',
     '年齢・家族・学校・新しい友達をつなぐ具体的属性。이다/하고で表現できる。',
     '同じ年齢の人物という中心義に限定し、比較보다は使用しない。'),
    ('정보','information','충전기','noun','charger','充電器',
     'school_work_transport_info','住所・時刻等の具体語で代替できる。',
     '持ち物・貸し借り・忘れ物・旅行に使える具体的な機器。',
     '携帯電話等の充電器。충전하다と同根だが物と動作で役割が異なる。'),
    ('가장','most','방금','adverb','just_now','たった今',
     'adverbs_connectors','제일をK1の最上級として優先し、重複を減らす。',
     '直前の出来事を過去形で示せる。곧の近い未来、지금の現在とは時間義が異なる。',
     '副詞の直前過去義のみ。副詞/名詞の多品詞用法を一括許可しない。'),
]

def apply_phase1_1(core,expansions):
    next(e for e in core if e['lemma']=='아니다')['notes']='Phase 1.1で正式採用。原案한국を固有名詞台帳へ移動。N이/가 아니에요のみ。'
    for e in expansions:
        previous=e['tier']
        if e['lemma'] in TIER_CHANGES:
            tier,reason=TIER_CHANGES[e['lemma']]
            e['tier']=tier
            e['notes']=' / '.join(filter(None,[e['notes'],f'Phase 1.1: {previous}→{tier}。{reason}']))
            if tier=='E1':e.update(introduced_from=1,introduced_to=100)
            elif tier=='E2':e.update(introduced_from=61,introduced_to=220)
            else:e.update(introduced_from=151,introduced_to=275)
        elif e['tier']=='E2':e['introduced_to']=min(260,e['introduced_to']+10)
        elif e['tier']=='E3':e['introduced_to']+=25
    by_key={(e['lemma'],e['sense']):e for e in core+expansions}
    proposals=[]
    for old,sense,new,pos,new_sense,gloss,category,removal,reason,notes in REPLACEMENT_PROPOSALS:
        source=by_key[old,sense]
        source['confidence']='medium'
        source['notes']=' / '.join(filter(None,[source['notes'],f'Phase 1.1再査定: K2送り・入替を推奨。代替候補{new}は未採用、現行500に保持。']))
        assert not any(e['lemma']==new for e in core+expansions),new
        assert source['category']==category,(old,category)
        proposals.append(dict(source_id=source['id'],source_lemma=old,source_pos=source['pos'],source_sense=sense,
                              action='propose_defer_to_K2',removal_reason=removal,
                              candidate=dict(lemma=new,pos=pos,sense=new_sense,gloss_ja=gloss,
                                             category=category,tier=source['tier'],notes=notes),
                              replacement_reason=reason,status='pending_human_review'))
    most=by_key['제일','most_colloquial']
    most['confidence']='high'
    most['notes']='가장よりK1で優先。会話での最上級「一番」のみ。比較보다/와・과を追加許可しない。'
    assert Counter(e['tier'] for e in expansions)=={'E1':200,'E2':200,'E3':100}
    save('expansion_replacement_proposals.json',{
        'phase':'1.1','status':'pending_human_review','applied':False,
        'counted_in_vocab_budget':False,'entries':proposals,
        'notes':'7組は一対一の提案。現在の500語は削除・追加せず、採用後は旧IDを新語に再利用しない。候補Tierは一対一で件数を維持する配置案。'})

def apply_phase1_2(expansions):
    proposal=json.loads((DEST/'expansion_replacement_proposals.json').read_text(encoding='utf-8'))
    mappings=[];retired=[]
    tags={
        '가만히':['daily_life','action','description'],
        '아저씨':['daily_life','communication','social_relation'],
        '시간표':['daily_life','school','work','transport','time','object'],
        '충전하다':['daily_life','action','communication','object','travel','story_event'],
        '동갑':['daily_life','family','school','social_relation'],
        '충전기':['daily_life','object','communication','travel','problem'],
        '방금':['daily_life','time','story_event'],
    }
    for index,p in enumerate(proposal['entries'],801):
        old=next(e for e in expansions if e['id']==p['source_id'])
        new_id=f'ko_k1_{index:04}'
        candidate=p['candidate']
        new=entry([candidate['lemma'],candidate['sense'],candidate['gloss_ja']],candidate['pos'],
                  old['rank'],old['tier'],old['category'],tags[candidate['lemma']])
        new.update(id=new_id,introduced_from=old['introduced_from'],
                   introduced_to=old['introduced_to'],target_exposures=6,
                   notes='Phase 1.2で正式採用。'+candidate['notes'])
        if candidate['lemma']=='아저씨':
            new['notes']+=' 人物関係・呼称の社会語用に注意。未知の成人男性への直接呼びかけを無条件に生成しない。叙述や関係が明確な場面を優先。'
            new['confidence']='medium'
        expansions[expansions.index(old)]=new
        mappings.append(dict(old_id=old['id'],old_lemma=old['lemma'],old_pos=old['pos'],old_sense=old['sense'],
                             new_id=new_id,new_lemma=new['lemma'],new_pos=new['pos'],new_sense=new['sense'],
                             rank=old['rank'],tier=old['tier'],category=old['category']))
        retired.append(dict(former_id=old['id'],lemma=old['lemma'],pos=old['pos'],sense=old['sense'],
                            gloss_ja=old['gloss_ja'],status='K2_candidate_only',reason=p['removal_reason'],replacement_id=new_id))
        p.update(status='accepted',action='retire_from_K1',adopted_id=new_id)
    for e in expansions:
        if e['tier'] in ('E2','E3'):e['introduced_to']=min(e['introduced_to'],255)
    save('id_migration.json',dict(phase='1.2',status='applied',
        id_policy={'immutable':True,'reuse_retired_ids':False,'next_id_sequence':808,
                   'id_rank_independent':True,'rank_policy':'rankは1〜800の表示スロット。新語は旧語のrankを引き継ぐが恒久IDは0801〜0807を新規採番。'},
        mappings=mappings))
    save('k2_candidates.json',dict(status='candidate_ledger_only',counted_in_K1_budget=False,
         notes='K1から退役した7語の候補台帳のみ。K2の語彙・Tier・教材計画は設計しない。',entries=retired))
    proposal.update(phase='1.2',status='accepted',applied=True,
                    notes='Phase 1.2の正式採用履歴。現行語彙DBへの結合は不要。旧IDは退役し新IDへ置換済み。')
    save('expansion_replacement_proposals.json',proposal)

def annotate(core,expansions):
    all_entries=core+expansions
    keyed={(e['lemma'],e['sense']):e for e in all_entries}
    def note(lemma,sense,text,forms=None,confidence=None):
        e=keyed[lemma,sense]
        e['notes']=' / '.join(filter(None,[e['notes'],text]))
        if forms is not None:e['forms']=forms
        if confidence:e['confidence']=confidence
    for lemma,sense,text in [
        ('있다','exist','存在・所有の形容詞として登録。滞在動詞있다・補助用言の意味は追加しない。連体形있는は特別活用。-고 있다と수 있다は文法側で許可。'),
        ('없다','not_exist','原案の動詞欄から形容詞へ分類。連体形없는は特別活用。'),
        ('필요하다','necessary','原案の動詞欄から形容詞へ分類。N이/가 필요해요。'),
        ('모두','all_together','副詞用法のみ。모두가の名詞用法はこのエントリでは許可しない。'),
        ('언제','when','언제 가요?の副詞用法のみ。언제가の代名詞用法は未登録。'),
        ('지금','now','副詞用法のみ。지금은の名詞用法は未登録。'),
        ('같이','together','共同動作のみ。N같이の比況・助詞用法は未登録。'),
        ('시','clock_hour','韓国語の依存名詞を共通POS counterへ写像。固有数詞と組み合わせる。'),
        ('분','minute','時間単位のみ。敬称분は未登録。'),
        ('월','calendar_month','暦の月のみ。期間はExpansion 달/month_duration。'),
        ('시간','time','時間の長さを含む同一中心義。한 시간の単位用法もこの名詞エントリへ正規化し二重計上しない。'),
        ('쓰다','write','書くのみ。使う・かぶるはこの義では未許可。'),
        ('찍다','take_photo','写真を撮るのみ。印を押すはExpansionの別sense。'),
        ('차','tea','飲み物のお茶のみ。自動車の略称차は未登録。'),
        ('말','speech','言葉・発言のみ。馬は未登録。'),
        ('눈','snow','雪のみ。目はExpansionの別sense。'),
        ('일','work','仕事・作業のみ。日付の일と事件の일はこの義では未許可。'),
        ('이','two_sino','漢数詞2のみ。指示詞・歯は別エントリ。'),
        ('팔','eight_sino','漢数詞8のみ。腕は別エントリ。'),
        ('너','you_informal','해요체で安易に相手へ使わない。主に親しい人物関係に限定。'),
        ('우리','we','韓国語の우리 집等の共有・所属表現も許可。'),
        ('너무','too','過度の中心義に限定。単なる強調はCore 아주を優先。'),
        ('밥','cooked_rice_meal','炊いた米と日常の食事の慣用的な連続義を1エントリとする。穀物は쌀。'),
        ('저녁','evening','夕方・晩の時間義のみ。夕食義は밥/음식で表現し未許可。'),
        ('아침','morning','朝の時間義のみ。朝食義は未許可。'),
        ('점심','lunch','昼食を中心義に採用。正午の厳密な時刻義は未許可。'),
        ('전화','telephone','電話機・電話という連続義。전화하다は別見出し語。'),
        ('선생님','teacher','教師への呼称のみ。一般の相手への敬称に拡張しない。'),
    ]:note(lemma,sense,text)
    for lemma,sense,forms in [
        ('하나','one_native',['한']),('둘','two_native',['두']),('셋','three_native',['세']),
        ('넷','four_native',['네']),('스물','twenty_native',['스무']),
        ('듣다','hear_listen',['들어요','듣는']),('걷다','walk',['걸어요','걷는']),
        ('모르다','not_know',['몰라요','모르는']),
        ('춥다','cold_weather',['추워요','추운']),('덥다','hot_weather',['더워요','더운']),
        ('좋다','good',['좋아요','좋은']),('있다','exist',['있어요','있는']),
        ('없다','not_exist',['없어요','없는']),('시다','sour',['셔요','신']),
        ('쓰다','bitter',['써요','쓴']),('고르다','choose',['골라요','고르는']),
        ('줍다','pick_up',['주워요','줍는']),('굽다','bake_grill',['구워요','굽는']),
        ('오래되다','old_object',['오래돼요','오래된']),
        ('빨갛다','red',['빨개요','빨간']),('파랗다','blue',['파래요','파란']),
        ('하얗다','white',['하얘요','하얀']),('까맣다','black',['까매요','까만']),
        ('노랗다','yellow',['노래요','노란']),('어떻다','how_state',['어때요']),
    ]:
        if (lemma,sense) in keyed:note(lemma,sense,'formsは例示で網羅的活用表ではない。数詞の連体異形は同一語に正規化。' if keyed[lemma,sense]['pos']=='numeral' else '不規則・縮約・連体形の例示。網羅的な活用表ではない。',forms)
    for lemma,sense,text in [
        ('이','this','Core 이/two_sinoとは別義・別POS。'),
        ('저','that_over_there','Core 저/i_humbleとは別義・別POS。'),
        ('눈','eye','Core 눈/snowとは同形異義。'),
        ('개','item_unit','Core 개/dogとは同形異義。'),
        ('팔','arm','Core 팔/eight_sinoとは同形異義。'),
        ('이','tooth','Core 이/two_sino・Expansion 이/thisとは同形異義。'),
        ('찍다','stamp','Core 찍다/take_photoとは別義。印・スタンプを押す意味のみ。'),
        ('풀','glue','Expansion 풀/grassとは同形異義。'),
        ('달','month_duration','Expansion 달/moonとは同形異義。'),
        ('배','belly','Expansion 배/pearとは同形異義。船は未登録。'),
        ('다리','leg','Expansion 다리/bridgeとは同形異義。'),
        ('봉지','bag_unit','袋の数を数える依存名詞。物体としての봉지/bag_packetと別POS。'),
        ('쓰다','bitter','Core 쓰다/writeとは同形異義。'),
        ('화나다','angry','状態カテゴリに置くが韓国語のPOSは動詞。連体形화나는。'),
        ('신나다','excited','状態カテゴリに置くが韓国語のPOSは動詞。連体形신나는。'),
        ('되다','become','N이/가 되다のみ。受動・許可・義務の補助構文は未許可。'),
        ('데리다','take_someone_along','単独の終止形より데리고 가다/오다を使用。'),
        ('빌려주다','lend','辞書見出し語として扱う。빌리다から全語を自由に-어 주다派生させない。'),
        ('벗기다','remove_clothing','辞書見出し語として扱う。一般的な使役接辞の許可ではない。'),
        ('보이다','be_visible','見えるの自動詞義のみ。見せるの使役義は未許可。'),
        ('혼자','alone','副詞用法のみ。혼자가等の名詞用法は未登録。'),
        ('서로','each_other','副詞用法のみ。서로의等の名詞用法は未登録。'),
        ('조용히','quietly','副詞の辞書見出し語。조용하다と異なるPOS。'),
        ('잠깐','briefly','副詞用法のみ。잠깐은等の名詞用法は未登録。'),
        ('전','before','시간・食事等の名詞+전だけ許可。動詞の-기 전・連体形構文は未許可。'),
        ('후','after','名詞+후だけ許可。動詞過去連体形-(으)ㄴ 후は未許可。'),
        ('꿈','dream_sleep','睡眠中の夢のみ。将来の夢・希望の抽象義は未許可。'),
        ('표','ticket','交通・入場の切符のみ。表・票の意味は未許可。'),
        ('기사','driver','運転手のみ。新聞記事・騎士の意味は未許可。'),
        ('자꾸','repeatedly','意図せず繰り返す・反復する場面。単なる頻度はCore 자주を優先。'),
        ('아무','any_attributive','아무 N도 없다等の否定文のみ。아무나/아무거나へ自由に拡張しない。'),
        ('새','new_attributive','새 책の連体詞。鳥の새/birdとは同形異義。'),
    ]:
        if (lemma,sense) in keyed:note(lemma,sense,text)
    boundary={
        '조부모':'할머니/할아버지で代替できる。家族全体をまとめる場面に限定。',
        '관계':'抽象語。親しい・家族等の具体文脈に限定。',
        '미술관':'芸術鑑賞の具体場面に限り再遭遇計画を要確認。',
        '박물관':'旅行・学校行事で6教材の再使用を確認。',
        '찍히다':'受動の理解負荷。写真という具体場面の辞書語に限定。',
        '결국':'談話理解の負荷。短い因果連鎖に限定。',
        '관심':'抽象語。趣味・好きな活動に限定。',
        '정보':'抽象語。住所・時刻等の具体情報に限定。',
        '기차역':'Core 역との差が小さいが、鉄道と地下鉄を区別する具体場面用。',
        '함께':'Core 같이とほぼ同義。理解語として保持、生成は같이優先。',
        '제일':'가장とほぼ同義。会話用、同一教材で言い換えない。',
    }
    for e in expansions:
        if e['lemma'] in boundary:
            note(e['lemma'],e['sense'],boundary[e['lemma']],confidence='medium')
        if e['tier']=='E1' and e['lemma'] in {'네','아니요','이','그','저','무슨','몇','더','아직','괜찮다','되다','개','명','살','권'}:
            e.update(introduced_from=1,introduced_to=80)
    # Individual tags describe permitted contexts, not just the quota bucket.
    for e in all_entries:
        if e['pos']=='verb':e['tags'].append('action')
        if e['pos']=='adjective':e['tags'].append('description')
        if e['pos']=='counter' or e['pos']=='numeral':e['tags'].append('quantity')
        e['tags']=list(dict.fromkeys(e['tags']))
    # Replace broad quota-bucket tags with narrower generation contexts where needed.
    contexts={
        'school': '학교 학생 선생님 교실 책 공책 종이 책상 연필 펜 지우개 풀 가위 칠판 교과서 학년 수학 체육 미술 숙제 시험 수업 공부 공부하다 배우다 가르치다 읽다 쓰다 단어 문장 질문 사전 초등학생 중학생 고등학생 대학생 방학',
        'work': '회사 회사원 직원 동료 회의 사무실 일 일하다 휴가',
        'food': '물 밥 빵 과일 사과 고기 채소 커피 차 우유 음식 점심 달걀 생선 닭고기 돼지고기 소고기 쌀 국 김치 라면 김밥 주스 바나나 오렌지 딸기 포도 토마토 감자 당근 양파 소금 설탕 치즈 요구르트 과자 아이스크림 케이크 초콜릿 오이 배 수박 귤 버섯 두부 반찬 고추 감 복숭아 고구마 떡 꿀 먹다 마시다 씹다 끓이다 굽다 섞다 자르다 요리하다 요리사 주문하다 배고프다 배부르다 목마르다 달다 짜다 맵다 시다 쓰다 맛있다 맛없다 컵 접시 숟가락 젓가락 그릇 냄비 프라이팬 칼 포크 식탁',
        'transport': '버스 지하철 택시 자동차 자전거 기차 역 비행기 공항 정류장 표 신호 횡단보도 기차역 기사 주차장 건너다 타다 내리다 도착하다 출발하다',
        'travel': '여행 호텔 공항 지도 짐 고향 도시 섬 미술관 박물관 동물원',
        'weather': '날씨 비 눈 바람 해 하늘 구름 덥다 춥다 따뜻하다 시원하다',
        'time': '아직 벌써 곧 이제 계속 미리 오래 일단 잠깐 차례로 마침 결국 전 후 다음 이번 나중',
        'nature': '산 바다 꽃 나무 동물 개 고양이 구름 달 별 강 새 물고기 토끼 나뭇잎 돌 풀 섬',
        'health': '병원 약국 의사 간호사 약 건강 건강하다 감기 아프다 다치다 몸 피',
        'body': '몸 머리 눈 귀 코 입 손 발 다리 배 목 어깨 팔 등 이 얼굴 머리카락 피 눈물',
        'shopping': '가게 시장 마트 편의점 가격 돈 사다 팔다 고르다 계산하다 영수증 원 백 천 만 지갑',
        'emotion': '마음 기분 생각 걱정 꿈 기억 관심 기쁘다 슬프다 행복하다 무섭다 힘들다 부끄럽다 심심하다 즐겁다 신나다 아쉽다 부럽다 화나다 화내다 미안하다 좋아하다 싫어하다 걱정하다 울다 웃다',
        'communication': '말 이야기 이름 나라 한국어 누구 뭐 무엇 어디 언제 왜 어떻게 어느 여러분 자기 누군가 네 아니요 이 그 저 무슨 몇 아무 말하다 전화 전화하다 인터넷 메시지 편지 이메일 정보 인사하다 사과하다 소개하다 설명하다 대답하다 물어보다 약속 약속하다',
    }
    families=set('사람 친구 가족 아버지 어머니 아들 딸 형 오빠 누나 언니 동생 남자 여자 아이 엄마 아빠 부모 할머니 할아버지 남편 아내 아기 이웃 어른 어린이 부부 형제 남동생 여동생 친척 사촌 조부모 조카 관계'.split())
    for e in all_entries:
        tags=['daily_life']
        if e['lemma'] in families:tags.append('family')
        for tag,lemmas in contexts.items():
            if e['lemma'] in lemmas.split():tags.append(tag)
        # Homographs must not inherit the other sense's semantic tags.
        excludes={('눈','snow'):{'body','health'},('눈','eye'):{'weather','nature'},
                  ('개','item_unit'):{'nature'},('이','this'):{'body'},
                  ('이','two_sino'):{'body','communication'},('이','tooth'):{'communication'},
                  ('팔','eight_sino'):{'body'},('새','new_attributive'):{'nature'},
                  ('풀','grass'):{'school'},('풀','glue'):{'nature'},
                  ('달','month_duration'):{'nature'},('배','pear'):{'body'},
                  ('배','belly'):{'food'},('다리','bridge'):{'body'},
                  ('쓰다','write'):{'food'},('쓰다','bitter'):{'school'}}
        tags=[t for t in tags if t not in excludes.get((e['lemma'],e['sense']),set())]
        if e['category'] in ('places','places_objects'):tags.append('place' if e['lemma'] in {'집','학교','회사','가게','식당','카페','병원','은행','시장','공원','도서관','화장실','방','교실','길','거리','역','밖','안','앞','뒤','옆','위','아래','곳','도시','부엌','거실','아파트','약국','마트','편의점','우체국','호텔','입구','출구','계단','엘리베이터','건물','동네','마을','고향','놀이터','주차장','빵집','미용실','침실','욕실','문구점','세탁소','동물원','수영장','미술관','박물관','운동장','섬','골목','다리'} else 'object')
        if e['category'] in ('time','time_counters_units'):tags.append('time')
        if e['category']=='daily_objects' and not set(tags)&{'food','school','work','communication','emotion'}:tags.append('object')
        if e['pos']=='verb':tags.extend(['action','story_event'])
        if e['pos']=='adjective':tags.append('description')
        if e['pos'] in ('counter','numeral'):tags.append('quantity')
        if e['lemma'] in {'문제','실수','이유','방법','걱정','잃다','잊다','고치다','넘어지다','다치다'}:tags.append('problem')
        e['tags']=list(dict.fromkeys(tags))

GRAMMAR = '''
이다: 이에요/예요|〜です|copula|여기는 우리 집이에요.|名詞述語。받침あり이에요、なし예요。過去였어요/이었어요はg03と組み合わせる。否定はCore 아니다でN이/가 아니에요。
-아요/어요|〜ます・〜です（現在）|ending|저는 매일 학교에 가요.|動詞・形容詞の해요체。하다→해요等の縮約・不規則活用を認める。独立した新文法を追加しない。
-았/었어요|〜ました・〜でした|tense|저는 어제 책을 읽었어요.|했어요等の縮約を認める。経験・過去連体形や大過去-았었-は未許可。
-(으)ㄹ 거예요|〜する予定です|tense|저는 내일 학교에 갈 거예요.|予定中心。推量の多用は避ける。거/것のこの構文内用法だけ許可。自由な名詞化は不可。
-고 있다|〜しています|aspect|저는 지금 책을 읽고 있어요.|進行のみ。着用・結果状態や-아/어 있다は未許可。있다は補助用言として文法内で認可。
-고 싶다|〜したいです|modality|저는 지금 물을 마시고 싶어요.|動詞に接続。本人の希望・相手への質問を中心にする。第三者の-고 싶어하다は未許可。
안|〜しません・〜くありません|negation|저는 오늘 학교에 안 가요.|短形否定。名詞+하다語では공부 안 해요等を認めるが、否定できない語に機械的に付けない。-지 않다は未許可。
못|〜できません|negation|저는 오늘 학교에 못 가요.|動詞の不可能のみ。能力・状況による不可能。形容詞への一律付加は禁止。
-고|〜して・〜で（並列・順序）|connector|저는 밥을 먹고 학교에 가요.|2事態までを優先。長い列挙は避ける。
-지만|〜ですが|connector|방은 작지만 아주 좋아요.|対比・逆接。1文の接続節は通常1つ。
-아/어서|〜なので・〜して（順序）|connector|오늘은 비가 와서 집에 있어요.|理由と密接な順序。理由用法の後ろの命令・勧誘、接続直前の過去-았/었-は避ける。
-(으)니까|〜なので|connector|오늘은 비가 오니까 우산을 가져가세요.|理由。命令・勧誘への接続も許可。発見用法は未許可。
-(으)면|〜なら・〜したら|connector|시간이 있으면 같이 책을 읽어요.|具体的な条件のみ。反実仮想・複雑な仮定は避ける。
-(으)세요|〜してください|request|여기에서 우리 친구를 기다리세요.|依頼・指示のみ。一般的な尊敬-(으)시-や드리다の派生を許可しない。命令対象は動作動詞を中心にする。
-(으)ㄹ까요|〜しましょうか・〜でしょうか|proposal|우리 같이 공원에 갈까요?|勧誘・意向確認を中心にする。複雑な推量質問は避ける。
-(으)ㄹ 수 있다/없다|〜できます・できません|modality|저는 한국어를 읽을 수 있어요.|수はこの構文専用の依存名詞。있다/없다の補助用法のみ許可。自由な수の語義は不可。
-아/어야 하다|〜しなければなりません|modality|저는 오늘 숙제를 해야 해요.|義務の基本形。-아/어야 되다や-아/어야等の別構文は未許可。
-아/어 보다|試しに〜してみます|auxiliary|이 책을 읽어 봐요.|試行のみ。보다は補助用法を文法内で許可。経験-아/어 봤다はg03と組み合わせ可。一般的な補助動詞構文への拡張は不可。
은/는|主題・対比|particle|저는 매일 학교에 가요.|話題を示す。隠れた対比の説明負荷は避ける。
이/가|主語|particle|친구가 지금 집에 있어요.|아니다の補語にも使用。누구+가→누가、나+가→내가、저+가→제가、너+가→네가を同一語に正規化。
을/를|目的語|particle|저는 매일 책을 읽어요.|目的語の基本用法のみ。数え方では助詞を語彙に含めない。
에|場所・行先・時点|particle|저는 아침에 학교에 가요.|存在の場所、移動の行先、時点。数量당等の拡張は未許可。
에서|動作の場所|particle|저는 집에서 책을 읽어요.|動作の場所のみ。起点は追加候補として保留。
도|〜も|particle|저도 오늘 학교에 가요.|単純な追加。疑問語+도等は아무 N도の許可範囲以外へ拡張しない。
하고|〜と（名詞並列・共同）|particle|저는 친구하고 밥을 먹어요.|接続・共同格。用言하다+고と区別する。와/과・(이)랑は未許可。
-(으)ㄴ|〜い・〜な（形容詞連体）|adnominal|저는 작은 가방을 샀어요.|形容詞のみ。있다/없다の있는/없는は個別異形。動詞過去連体形は未許可。連体節の深い埋め込みは避ける。
-는|〜する（動詞現在連体）|adnominal|저는 친구가 읽는 책을 봐요.|現在連体形のみ。動詞の-(으)ㄴ/-(으)ㄹはこの項目では未許可。
에게/한테|人に（受け手・相手）|particle|저는 친구한테 책을 줘요.|해요체では한테優先。에게서/한테서は未許可。
의|〜の（所有）|particle|이것은 친구의 책이에요.|所有・所属のみ。나의→내、저의→제を同一語に正規化。이/그/저の指示連体詞と混同しない。
-(으)로|〜で（手段）・〜へ（方向）|particle|저는 버스로 학교에 가요.|名詞に接続。母音・ㄹ받침の後は로、それ以外の받침は으로。交通手段・道具・移動方向に限定。資格・材料・原因・結果義、(으)로써/로서は未許可。
부터 / 까지|〜から・〜まで（起点・終点）|particle|저는 아침부터 저녁까지 일해요.|時間・場所の区間の開始と終わりに限定。この一対を1文法項目と数える。場所起点は집에서부터等の에서との組合せを優先。強調の「〜さえ」までへ拡張しない。
만|〜だけ（限定）|particle|저는 오늘 물만 마셔요.|名詞等の単純な限定のみ。숫자 만「万」と区別。-기만、만에、-(으)ㄹ 만하다等の別構文は未許可。
'''

def build_support():
    grammar=[]
    for i,line in enumerate(GRAMMAR.strip().splitlines(),1):
        form,meaning,category,example,notes=line.split('|')
        grammar.append(dict(id=f'ko_k1_g{i:02}',form=form,meaning_ja=meaning,
                            category=category,example=example,notes=notes))
    save('grammar.json',grammar)
    save('lexical_exceptions.json',{
        'status':'proposed','counted_in_vocab_budget':False,
        'policy':{'match':'exact_surface_sequence','allow_inflection':False,
                  'license_constituents':False,'max_occurrences_per_text':2,
                  'context':'登場人物の挨拶・感謝・謝罪・別れの会話に限定',
                  'coverage_policy':'登録されたfrozen_exceptionは導入基準教材0の固定spanとしてNへ1 tokenを計数する。regular_vocab_formは依存語彙の導入教材に従う。学習者の実際の知識は推定しない。',
                  'notes':'文法外の定型表現は5種類のみ。新しい例外は人間レビュー後に台帳へ追加。'},
        'entries':[
            dict(id='ko_k1_x01',form='안녕하세요',meaning_ja='こんにちは',
                 kind='frozen_exception',requires_vocab=[],notes='挨拶の固定形のみ。안녕하다・尊敬表現全般は許可しない。'),
            dict(id='ko_k1_x02',form='감사합니다',meaning_ja='ありがとうございます',
                 kind='frozen_exception',requires_vocab=[],notes='固定形のみ。감사하다の活用や합니다体全般は許可しない。'),
            dict(id='ko_k1_x03',form='죄송합니다',meaning_ja='申し訳ありません',
                 kind='frozen_exception',requires_vocab=[],notes='固定形のみ。죄송하다の自由活用は許可しない。'),
            dict(id='ko_k1_x04',form='안녕히 가세요',meaning_ja='さようなら（去る相手へ）',
                 kind='frozen_exception',requires_vocab=[],notes='別れの固定句。안녕히の自由使用は許可しない。'),
            dict(id='ko_k1_x05',form='안녕히 계세요',meaning_ja='さようなら（残る相手へ）',
                 kind='frozen_exception',requires_vocab=[],notes='別れの固定句。계시다の自由活用は許可しない。'),
            dict(id='ko_k1_x06',form='괜찮아요',meaning_ja='大丈夫です',
                 kind='regular_vocab_form',requires_vocab=['괜찮다'],
                 notes='E1 괜찮다とg02の通常活用。語彙例外による未導入語の迂回を認めない。')
        ]})
    save('profile.json',{
        'language':'ko','level':'K1','version':'0.1.2','status':'vocabulary_final_exposure_planned',
        'target_texts':300,'vocab_budget':{'core':300,'expansion':500,'total':800},
        'length':{'min_eojeol':120,'max_eojeol':180},
        'sentence_length':{'preferred_min_eojeol':4,'preferred_max_eojeol':7,'hard_max_eojeol':10},
        'new_vocab':{'min':0,'max':2,'unit':'lemma','max_entries_per_text':2,
                     'first_text_new_lemma_token_soft_max':3,
                     'token_policy':'初出教材の新出語token合計は原則3以下。各語3回ではない。逸脱は人間レビューを要する。'},
        'controlled_vocab_coverage_hard_min':1.0,
        'previous_vocab_coverage_hard_min':0.98,'previous_vocab_coverage_target':0.99,
        'repetition':{'near_repetition_allowed':True,'near_repetition_encouraged':True,'paraphrase_required':False,
                      'new_lemma_mass_repetition_in_first_text':False,'prefer_new_lemma_repetition_in_later_texts':True,
                      'near_repetition_scope':'既知語の近距離反復を推奨。初出の新出語は全語合計token3以下の方針を優先。'},
        'style':{'default_register':'해요체','prefer_processing_ease':True,'prefer_naturalness_over_variety':True},
        'grammar_count':32,
        'core_decision':{'status':'accepted','replacement':'한국→아니다','proper_names_outside_budget':True},
        'expansion_decision':{'active_entries':500,'replacement_proposals_applied':True,'status':'accepted',
                              'notes':'7組の正式入替とPhase 1.1のTier変更8語を採用。新語は旧語と同じE3・カテゴリ。'},
        'counting':{
            'vocab_unit':['lemma','pos','sense'],
            'proper_names_in_budget':False,'grammar_bound_forms_in_budget':False,
            'eojeol':'空白区切りの非空トークン数。句読点だけのトークンを数えない。',
            'coverage_denominator_N':'本文の解決済み内容語・意味単位tokenの延べ数。各活用は同一エントリの1出現。許可固有名詞は1出現1token、固定例外は1一致スパン1token。未許可内容語も分母に含む。助詞・語尾・句読点・許可構文の文法専用要素は除外。',
            'new_tokens_U':'当該教材で初出するExpansionエントリの全出現token数。controlled100%合格時はN-Uがprevious token数となる。未許可語・未来語はcontrolled違反として先に不合格。',
            'compound_lemmas':'공부하다等の登録済み辞書語は1token。공부를 하다の独立語공부と하다は2token。수/거/補助用言等は許可構文の文法専用用法に限って除外。',
            'new_vocab_definition':'新出lemmaは最大2。別senseの初出も導入として数え、DBエントリの初出も保守的に最大2に制限する。500エントリすべてを配置する。事前提示も初出教材の導入数に含める。',
            'new_lemma_token_count':'初出のlemma+POS+senseに対応する本文内tokenを合算。活用形も同一語として計数し、既出senseや文法専用語は新出tokenへ含めない。',
            'number_forms':'한/두/세/네/스무を固有数詞へ正規化。漢数詞の組合せは登録された数詞に分解。ゼロ・日付単位일・未登録の十位固有数詞は未許可。'},
        'coverage_policy':{
            'controlled_allowed_classes':['core','previous_expansion','current_expansion','proper_name','frozen_exception'],
            'baseline_introduction_text':0,
            'baseline_classes':['core','registered_proper_names','frozen_exceptions'],
            'controlled_formula':'controlled_tokens / N = 1',
            'previous_formula':'previous_tokens / N; controlled=1のとき(N-U)/N',
            'dynamic_hard_new_token_limit':'floor(N / 50)。hard98%をsoft3より優先。target99%にはfloor(N / 100)を目標。',
            'empty_denominator':'N=0は不合格。',
            'regular_exception_form':'괜찮아요は괜찮다のvocab tokenとして扱う。固定例外の基準導入で迂回しない。',
            'not_learner_knowledge':'導入済みという計画上の属性。習得・記憶・読解速度の証明ではない。'},
        'introduction':{'first_text':1,'last_text':275,'consolidation_from':276,
                        'tier_counts':{'E1':200,'E2':200,'E3':100},
                        'ranges':{'E1':[1,170],'E2':[61,255],'E3':[151,255]},
                        'target_exposures':6,'distinct_texts_required':True},
        'feasibility':{
            'introduction_slots':550,'required_new_entries':500,'slack_slots':50,
            'warning':'275本×2枠=550枠。500語導入後に50枠の余裕。0語・1語導入回を分散した配置例も検証する。',
            'coverage_resolution':'controlled100%がhard、previous98%がhard、previous99%がtarget。初出tokenは実際のNに応じfloor(N/50)以内に動的制限。',
            'generation_gate':'Phase 1.2で本文生成は行わない。次Phaseの少数試作は本計画・coverage検証に従って実施可能。'},
        'exposure_policy':{'recent_window_texts':20,'planned_exposures_per_entry':6,
                           'all_text_load_warn_above':16,'fast_zone_load_warn_above':12,
                           'fast_zone_E3_warn_above':6,'fast_zone_recent_E3_warn_above':0,
                           'near_max_gap':5,'medium_gap_min':6,'medium_gap_max':30,
                           'long_gap_rule':'min(60, floor(0.75 * (300-first)))以上の距離を最低1回。',
                           'notes':'負荷閾値は計画の運用目安。習得の保証ではない。初出も最近導入数へ含む。'},
        'grammar_policy':{
            'max_connector_clauses_preferred':2,'allow_unlisted_productive_derivation':False,
            'inflection_not_new_vocab':True,
            'excluded_grammar':['比較 보다','와/과','-지 않다','名詞化 -기'],
            'notes':'活用の許可は新たな語義・構文の許可ではない。辞書語の使役・受動・移動複合動詞は個別lemmaとしてのみ許可。'},
        'review_required':['母語話者による意味・社会語用・32文法の自然さ確認',
                           '新出token soft3の例外運用','生成後の実出現と形態素・sense解決の確認',
                           '基準導入0のCore・固有名詞・固定句の提示方法']
    })
    pos=['noun','verb','adjective','adverb','pronoun','determiner','numeral','counter','conjunction','interjection']
    nonempty={'type':'string','minLength':1}
    integer_or_null={'type':['integer','null'],'minimum':1,'maximum':275}
    vocab_item={
        'type':'object','additionalProperties':False,
        'required':['id','language','lemma','pos','sense','gloss_ja','level','tier','rank','tags',
                    'allow_inflection','introduced_from','introduced_to','target_exposures','forms','notes'],
        'properties':{
            'id':{'type':'string','pattern':'^ko_k1_[0-9]{4}$'},'language':{'const':'ko'},
            'lemma':nonempty,'pos':{'enum':pos},'sense':{'type':'string','pattern':'^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$'},
            'gloss_ja':nonempty,'level':{'const':'K1'},'tier':{'enum':['core','E1','E2','E3']},
            'rank':{'type':'integer','minimum':1,'maximum':800},
            'tags':{'type':'array','minItems':1,'uniqueItems':True,'items':{'type':'string','pattern':'^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$'}},
            'allow_inflection':{'type':'boolean'},'introduced_from':integer_or_null,'introduced_to':integer_or_null,
            'target_exposures':{'type':['integer','null'],'minimum':6,'maximum':300},
            'forms':{'type':'array','uniqueItems':True,'items':nonempty},'notes':{'type':['string','null'],'minLength':1},
            'category':{'type':'string','pattern':'^[a-z]+(?:_[a-z]+)*$'},'confidence':{'enum':['high','medium','low']}
        },
        'allOf':[{
            'if':{'properties':{'tier':{'const':'core'}}},
            'then':{'properties':{k:{'type':'null'} for k in ('introduced_from','introduced_to','target_exposures')}},
            'else':{'properties':{'introduced_from':{'type':'integer','minimum':1,'maximum':275},
                                  'introduced_to':{'type':'integer','minimum':1,'maximum':275},
                                  'target_exposures':{'type':'integer','minimum':6,'maximum':300}}}
        }]
    }
    schema_base={'$schema':'https://json-schema.org/draft/2020-12/schema'}
    save('vocab.schema.json',dict(schema_base,title='Korean K1 vocabulary array',type='array',items=vocab_item))
    grammar_properties={k:nonempty for k in ('id','form','meaning_ja','category','example','notes')}
    grammar_properties['id']={'type':'string','pattern':'^ko_k1_g[0-9]{2}$'}
    grammar_properties['category']={'enum':['copula','ending','tense','aspect','modality','negation','connector','request','proposal','auxiliary','particle','adnominal']}
    save('grammar.schema.json',dict(schema_base,title='Korean K1 grammar array',type='array',minItems=32,maxItems=32,
        items={'type':'object','additionalProperties':False,'required':list(grammar_properties),'properties':grammar_properties}))
    def shape(value):
        if isinstance(value,dict):
            return {'type':'object','additionalProperties':False,'required':list(value),
                    'properties':{k:shape(v) for k,v in value.items()}}
        if isinstance(value,list):
            return {'type':'array','items':shape(value[0]) if value else {'type':'string'}}
        if isinstance(value,bool):return {'type':'boolean'}
        if isinstance(value,int):return {'type':'integer'}
        if isinstance(value,float):return {'type':'number'}
        if isinstance(value,str):return {'type':'string','minLength':1}
        raise TypeError(value)
    read=lambda name:json.loads((DEST/name).read_text(encoding='utf-8'))
    profileshape=shape(read('profile.json'))
    # The Phase 1 constraints are not configurable through a silently edited profile.
    for field in ('language','level','target_texts','vocab_budget','length','sentence_length',
                  'new_vocab','repetition','style','grammar_count','introduction','core_decision','expansion_decision',
                  'coverage_policy','exposure_policy'):
        profileshape['properties'][field]={'const':read('profile.json')[field]}
    for field,value in [('controlled_vocab_coverage_hard_min',1.0),('previous_vocab_coverage_hard_min',0.98),('previous_vocab_coverage_target',0.99)]:
        profileshape['properties'][field]={'type':'number','minimum':0,'maximum':1,'const':value}
    exception_shape=shape(read('lexical_exceptions.json'))
    exception_shape['properties']['counted_in_vocab_budget']={'const':False}
    for field in ('match','allow_inflection','license_constituents','max_occurrences_per_text'):
        exception_shape['properties']['policy']['properties'][field]={'const':read('lexical_exceptions.json')['policy'][field]}
    exception_item=exception_shape['properties']['entries']['items']
    exception_item['properties']['kind']={'enum':['frozen_exception','regular_vocab_form']}
    exception_item['properties']['id']={'type':'string','pattern':'^ko_k1_x[0-9]{2}$'}
    proper_shape=shape(read('proper_names.json'))
    proper_shape['properties']['counted_in_vocab_budget']={'const':False}
    proposal_shape=shape(read('expansion_replacement_proposals.json'))
    for field in ('phase','status','applied','counted_in_vocab_budget'):
        proposal_shape['properties'][field]={'const':read('expansion_replacement_proposals.json')[field]}
    proposal_shape['properties']['entries'].update(minItems=7,maxItems=7)
    schedule_shape={'type':'object','additionalProperties':False,
        'required':['language','level','status','notes','rows'],
        'properties':{'language':{'const':'ko'},'level':{'const':'K1'},
            'status':{'const':'introduction_plan'},'notes':nonempty,
            'rows':{'type':'array','minItems':300,'maxItems':300,'items':{
                'type':'object','additionalProperties':False,'required':['text','entry_ids'],
                'properties':{'text':{'type':'integer','minimum':1,'maximum':300},
                    'entry_ids':{'type':'array','maxItems':2,'uniqueItems':True,
                                 'items':{'type':'string','pattern':'^ko_k1_[0-9]{4}$'}}}}}}}
    save('support.schema.json',dict(schema_base,title='K1 supporting data schemas',
        **{'$defs':{'profile':profileshape,'exceptions':exception_shape,'proper_names':proper_shape,
                   'replacement_proposals':proposal_shape,'introduction_schedule':schedule_shape,
                   'id_migration':shape(read('id_migration.json')),'k2_candidates':shape(read('k2_candidates.json'))}}))

def build_introduction_schedule(expansion):
    from validate_k1_vocab import introduction_assignment
    # Advance the last introduction to 255: six single + two zero texts use 10 slots.
    # Texts 256..275 supply the other 40 slack slots and 276..300 stay new-free.
    zero={85,170}
    single={40,80,120,160,200,240}
    capacities={t:0 if t in zero or t>255 else 1 if t in single else 2 for t in range(1,276)}
    witness,failure=introduction_assignment(expansion,texts=275,capacity=2,capacities=capacities,include_empty=True)
    assert failure is None,failure
    witness += [{'text':t,'entry_ids':[]} for t in range(276,301)]
    save('introduction_schedule.json',{
        'language':'ko','level':'K1','status':'introduction_plan',
        'notes':'初出は255まで。001〜275に0語22本、1語6本、2語247本。276〜300は新出0。再遭遇計画と一致する初出台帳。本文は未生成。',
        'rows':witness})
    from k1_schedule import build_exposure_plan
    save('vocab_exposure_schedule.json',build_exposure_plan(expansion,witness))
    schema_base={'$schema':'https://json-schema.org/draft/2020-12/schema'}
    ident={'type':'string','pattern':'^ko_k1_[0-9]{4}$'}
    text={'type':'integer','minimum':1,'maximum':300}
    nonnegative={'type':'integer','minimum':0,'maximum':500}
    row_props={'text':text,'new_vocab_ids':{'type':'array','items':ident,'maxItems':2,'uniqueItems':True},
               'review_vocab_ids':{'type':'array','items':ident,'uniqueItems':True},
               **{k:nonnegative for k in ('new_vocab_count','review_vocab_count','recently_introduced_vocab_count',
                                         'recently_introduced_E3_count','total_scheduled_expansion_count')},
               'tier_counts':{'type':'object','additionalProperties':False,'required':['E1','E2','E3'],
                              'properties':{tier:nonnegative for tier in ('E1','E2','E3')}}}
    save('vocab_exposure_schedule.schema.json',dict(schema_base,type='object',additionalProperties=False,
        required=['language','level','phase','status','notes','recent_window_texts','entries','texts','statistics'],
        properties={'language':{'const':'ko'},'level':{'const':'K1'},'phase':{'const':'1.2'},
                    'status':{'const':'planned_not_observed'},'notes':{'type':'string','minLength':1},
                    'recent_window_texts':{'const':20},'entries':{'type':'array','minItems':500,'maxItems':500,
                    'items':{'type':'object','additionalProperties':False,
                             'required':['vocab_id','first_introduction_text','review_texts'],
                             'properties':{'vocab_id':ident,'first_introduction_text':{'type':'integer','minimum':1,'maximum':275},
                                 'review_texts':{'type':'array','minItems':5,'uniqueItems':True,'items':text}}}},
                    'texts':{'type':'array','minItems':300,'maxItems':300,'items':{
                        'type':'object','additionalProperties':False,'required':list(row_props),'properties':row_props}},
                    'statistics':{'type':'object'}}))

if __name__=='__main__':
    from k1_history import protect_historical_build
    protect_historical_build(Path(__file__).resolve().parents[1])
    source,core,expansion=build_vocab()
    build_support()
    build_introduction_schedule(expansion)
    print(json.dumps({'source':len(source),'core':len(core),'expansion':len(expansion),
                      'total':len(core)+len(expansion)},ensure_ascii=False))
