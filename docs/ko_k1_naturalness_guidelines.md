# 韓国語K1 自然さ生成guideline

語彙800・文法32・導入予定・window・coverageは固定。自然さをreview語数より優先する。短い自然な文を、好ましい文長へ副詞で引き伸ばさない。

## 生成から承認まで

frozen introduction state → single scene/goal and agents → scene-specific positive review gate → draft Korean → hard lexical/grammar/coverage QA → warning lint → naturalness_semantic_review → omit/defer gaps; revalidate → freeze Korean body hash → fresh Japanese translation → translation fidelity second pass → human review

直接会話は話者を明示する。引用内も同じ32文法で検証し、間接引用や名詞化を追加許可しない。

## genitive_overuse

avoid literal Japanese-style genitive chaining; prefer conventional noun adjacency or a simple clause. Retain 의 for meaningful ownership/clarity.

危険例: 학교의 학생 / 수업의 시간 / 버스의 문 / 영화의 이야기

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## verb_argument_frame

Preserve verb intent and argument roles. Ask a direct question or omit; hold with introduced 들다; sit rather than fabricate a chair transfer.

危険例: 책을 물어보다 as borrow request / 친구의 이름을 말하다 as call / 무거운 가방을 받다 as carry help / 친구에게 의자를 주다

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## vague_positive_reaction

State a concrete licensed reaction such as 웃다, 괜찮다 or 재미있다 if that is the intended meaning. Otherwise omit. 좋아하다 remains valid for actual preferences.

危険例: 약속을 아주 좋아해요 / 이야기를 듣고 아주 좋아해요 / 친구는 잘 잡고 아주 좋아해요

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## filler_adverb

Do not pad to 4–7 eojeol. Short natural sentences are acceptable within hard max. Repetition within 2–3 sentences needs a semantic reason.

危険例: 먼저 같이 천천히 / 아주 정말 / repeating 조금 to pad length

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## scene_plausibility

One goal or closely linked goals. Ask why the person is there, whether action is ordinary here, and whether the review word alone motivated it.

危険例: employee waiting at entrance for this customer / handing phone to employee to buy charger / travel narration to shop employee

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## reference_clarity

Name antecedent/agent when switching. Distinguish depiction from object and absence in picture from nonexistence. Window eligibility is not referent evidence.

危険例: 사진의 저하고 동생 / 이것은 작은 집하고 학교예요 / 그 집은 지금 없어요

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## habit_vs_progressive

Habit: simple present. -고 있다 only for an action in progress at the reference time; habitual words are candidate warnings, not a ban.

危険例: 자주 공부하고 있어요

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## restricted_sense

License lemma + POS + sense, not lemma alone. Check 들다 hold/lift, 풀 glue/grass, 이 tooth/determiner/numeral, 눈 eye/snow, 쓰다 write/bitter. Retired identities are hard lexical violations.

危険例: 종이에 자리가 없다 / 칼을 쓰다 with write ID / 마음에 들다 with hold ID

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## unnatural_substitution

If natural permitted wording is unavailable, omit/defer and record natural_expression_gap. Never stretch a synonym, sense or character action.

危険例: friend name used instead of calling / time used instead of a memory of the day

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## translation_fidelity

Finalize Korean first; freshly translate its meaning, omitted subject and timeline faithfully. A bilingual second pass records evidence; model review is not approval.

危険例: 좋아해요 translated as 喜ぶ / translation fixing a wrong subject or causal relation

Lint only implemented subsets; intention, real-world plausibility and sense cannot be proved by regex. Human review required.

## 二次意味レビュー

coherent_goal / plausible_actions / no_review_only_actions / natural_arguments / clear_references / necessary_genitives / meaningful_adverbs / simple_natural_construction

各項目をYES/NO/REVIEW＋文脈の根拠で記録する。YESもモデルの仮判定であり、人間承認へ昇格させない。NOは書き直し・省略・defer、REVIEWは根拠付きで人間へ絞り込む。

## 語義と台帳

자리は席。紙の余白に広げない。Core 쓰다は書く、道具には사용하다。들다は手に持つ・持ち上げるだけ。아저씨のadult_man_addressは現行notesの叙述優先と名称がずれるため将来レビューへ送り、今回変更しない。

reviewの取りこぼしは選択予定を実出現として数えない。incidental exposureは本文の実使用だけから記録する。自然に書けない箇所はnatural_expression_gapにし、未許可語を使うより省略・延期する。

99%はtarget。U=2,N<200のtarget missは予想される。controlled100%とprevious98%をhard検査し、Nから未知語を隠さない。
