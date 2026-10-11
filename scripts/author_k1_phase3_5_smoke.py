"""Five bounded smoke drafts, authored sequentially from actual snapshots.

No old ledger, annotations or text projections are imported. This is a local
pilot authoring callback, not a production generator or an independent gold.
"""
from k1_phase3_5 import SmokeGate,PILOT,submit,freeze_errors
from k1_phase3_5_gate import ROOT,read,write
from k1_phase3 import metrics

PAIRS_001=[
('오늘은 학교에서 한국어를 배워요.','今日は学校で韓国語を学びます。'),
('저는 아침에 친구를 만나요.','私は朝、友人に会います。'),
('친구는 교실 앞에 있어요.','友人は教室の前にいます。'),
('저는 친구하고 교실에 들어가요.','私は友人と教室に入ります。'),
('교실에는 책상이 많이 있어요.','教室には机がたくさんあります。'),
('저는 친구 옆에 앉아요.','私は友人の隣に座ります。'),
('친구는 가방을 열고 책을 봐요.','友人はかばんを開け、本を見ます。'),
('저는 가방을 열고 공책을 봐요.','私はかばんを開け、ノートを見ます。'),
('책은 크고 공책은 작아요.','本は大きく、ノートは小さいです。'),
('저는 한국어 책을 읽고 싶어요.','私は韓国語の本を読みたいです。'),
('하지만 저는 책이 없어요.','でも私は本を持っていません。'),
('선생님은 교실 앞에 있어요.','先生は教室の前にいます。'),
('수업 시간이 돼요.','授業の時間になります。'),
('선생님이 교실 문을 열어요.','先生が教室のドアを開けます。'),
('선생님은 저에게 책을 줘요.','先生は私に本を渡します。'),
('저는 책을 받고 읽어요.','私は本を受け取って読みます。'),
('책은 한국어 책이에요.','本は韓国語の本です。'),
('친구도 선생님 이야기를 들어요.','友人も先生の話を聞きます。'),
('저는 문제를 보고 답을 써요.','私は問題を見て答えを書きます。'),
('하지만 답을 잘 몰라요.','でも答えがよく分かりません。'),
('저는 선생님에게 말해요.','私は先生に言います。'),
('"문제가 너무 어려워요."','「問題が難しすぎます。」'),
('선생님은 저를 보고 말해요.','先生は私を見て言います。'),
('"괜찮아요."','「大丈夫です。」'),
('선생님은 책을 열고 이야기를 해요.','先生は本を開けて話します。'),
('저는 듣고 책을 다시 읽어요.','私は聞いて、本をもう一度読みます。'),
('친구는 책을 보고 답을 써요.','友人は本を見て答えを書きます。'),
('저도 책을 보고 답을 써요.','私も本を見て答えを書きます。'),
('선생님은 답을 읽고 웃어요.','先生は答えを読んで笑います。'),
('수업이 끝나고 저는 책을 닫아요.','授業が終わり、私は本を閉じます。'),
('친구도 책을 가방에 넣어요.','友人も本をかばんに入れます。'),
('저는 친구하고 학교 밖으로 나가요.','私は友人と学校の外に出ます。'),
('그리고 집으로 돌아가요.','そして家へ帰ります。'),
]

def source(t,pairs,title,genre,scene,goal,actions,reviews=()):
    evidence={k:dict(verdict='YES',reason='One ordinary bounded scene; action roles and references checked by author, not independent approval.') for k in
        ('coherent_goal','plausible_actions','no_review_only_actions','natural_arguments','clear_references','necessary_genitives','meaningful_adverbs','simple_natural_construction')}
    return dict(text_number=t,title_ko=title,genre=genre,scene=scene,review_candidates=list(reviews),
        scene_fingerprint=dict(goal=goal,setting=scene[0],participants=['speaker','friend'],problem_type='ordinary_small_goal',resolution_type='concrete_action',main_actions=actions),
        semantic_evidence=evidence,notes='Fresh Phase 3.5 zero-state candidate. No historical credit. Grammar meaning is decided by the independent rule/evidence layer.',
        sentences=[p[0] for p in pairs],translations_ja=[p[1] for p in pairs])

def first():
    return source(1,PAIRS_001,'학교 수업','school',['school','communication'],'complete_a_lesson',['read','write','listen'])

if __name__=='__main__':
    assert not freeze_errors()
    g=SmokeGate();g.initialize()
    s=first();print(metrics(' '.join(s['sentences'])))
    r=submit(s)
    print(dict(text=r['text_number'],hard_pass=r['hard_pass'],coverage=r.get('coverage'),errors=[(e['code'],e['detail'].get('sentence') if isinstance(e['detail'],dict) else e['detail']) for e in r['hard_errors']],control=read(g.control)['status']))
