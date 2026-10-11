# Phase 3.6a response identity recovery

Phase 3.6のproduction-lite policy、grammar registry、DB、scheduleと停止runを変更しません。新versionのresolverだけで`네`の今回の誤分割を扱います。

登録yes ID、original exact span、応答冒頭、句読点境界、所有名詞との直接連結不成立、同じ1文字に重なる`너/NP + 의/JKG`の連続raw indices、既存resolverによるshort scopeの`네/IC/yes`をすべて要求します。モデルannotationは根拠にしません。rawはそのまま保存し、復元前annotation・quotation evidence・short probe・decisionを別auditへ残します。`네 책 / 네 가방 / 네 사람이`は適用対象にしません。

current new・high-risk alias/homograph・resolver対象のspanは、単文／段落／全文の登録IDをoriginal coordinatesへ戻して比較します。限定復元後もIDが違えばSCOPE_IDENTITY_MISMATCHをhard reject・構造STOPとします。安全に同じIDへ収束した場合はdiagnosticを残して続行します。semantic roleをこの比較へ持ち込まず、過去のgrammar REVIEW/heuristic FAILはwarningのままです。

snapshotにはCore・actual introduced・current planned・許可proper/frozen exceptionsだけを含めます。新runの001〜010はsnapshot取得後にfresh authoringし、回帰fixtureを生成本文としてコピーしません。max5attempt、停滞2回STOP、atomic commitを維持します。production開始後はengine/configをhash固定し、修正は禁止します。

timingはlive LLM作者のローカルcallback方式です。韓国語・日本語訳の執筆、確認、ファイル転送を含むwallを測り、engineering/pre-suiteを除外します。単体API latencyや保存本文replayの速度とは主張しません。300本外挿は10本完走時のみ、正式性能判定はn>=5に限定します。
