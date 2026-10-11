# Phase 3.4 — 001〜050 forward candidate schema

**PASS。** 元v3のschemaはsmoke用 `^K1-00[12]$` を残して003〜050を拒否した。この更新漏れは旧停止runを変更せず、新versionで修正した。

## 契約と実行上限

新builderはgeneric `^K1-[0-9]{3}$` 形式を `$defs` に置き、run契約の001〜050 enumとtext_number 1〜50を組み合わせる。さらにIDとtext_numberが一致する条件を50件設定した。candidate全体にhard PASSのcoverage・length等の既存Schema条件も残す。source Schemaの教材範囲も1〜50。gateはoutput candidateも保存前にSchema検証する。

schemaは50まで受理するが、本smokeのcontrolは `max_text=3`。003 commit後にcompletedとなり、snapshot004を拒否する。text004を生成して境界検査することはしない。将来の100等のrunはbuilderのrange引数で別契約を生成する設計であり、smoke regexをコピーしない。100番のsynthetic Schema testは実本文生成ではない。

## JSON Schema contract test

- 全50 ID：001〜050を、hard-PASS candidateの実データ形を持つobjectで検証して50/50受理。
- 指定negative8件：K1-000 / K1-051 / K1-099 / K1-300 / K1-01 / K1-1 / KO-K1-001 / K2-001をcandidate objectとして8/8拒否。
- ID/番号不一致、controlled coverage不足も拒否。
- 本smokeの実003 candidateがSchemaを通り、予定이・그を本文中で解析してhard PASS・commit。

regexだけの検査ではなく、Draft202012Validatorによる全candidate object validation。詳細は[Schema audit JSON](k1_phase3_4_forward_schema_audit.json)。

## Metadata監査

scene17値は正式 `vocab_review_windows.json.scene_catalog` から継承し、追加なし。weatherはtag/genreであってscene値ではなくnatureへ対応する。元v3のweather format rejectは正しい境界として維持する。

以前genreは任意の非空文字列だった。新source Schemaは人間指定のPhase 3 genre候補と既存承認済みpilot labelを合わせた19値に限定：daily_life, school, family, friends, friendship, food, shopping, transport, weather, home, small_problem, short_dialogue, simple_outing, objects, simple_hobby, health, outdoor, travel, work。friendsとfriendshipは既存labelの互換性を保持する。genre quota・scene taxonomyの変更はしない。未知genreと未登録sceneはformat rejectし、retry可能。

これらmetadata enumはレビュー・監視のtaxonomyであり、語彙許可や意味identityの代用ではない。scene/hard grammar/vocab gateは別途実行する。

## 結果

full240 / focused33 tests PASS。最終clean smokeのactual candidate/source Schema違反0、001〜003 commit済み。run upper bound3と契約upper bound50を分離するtests PASS。最初のsmokeの003で見落とした文法意味制限違反はuri reportとpost-semantic failureに記録し、元creditを引き継がない。旧engines・schemas・停止結果を変更していない。

[우리 report](k1_phase3_4_uri_context_report.md) / [validation JSON](k1_phase3_4_validation_result.json)
