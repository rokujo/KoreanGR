# Phase 3.9a 停止根拠

K1-001〜066をcommit。K1-067の候補1はrejectされ、K1-068以降は生成していない。author contractの事故による停止ではない。

## 今回の限定的なblocker

当該教材の正式予定語 `ko_k1_0419 / 졸리다 / adjective / sleepy` が、単文内の正常な活用でもKiwiから `졸리 / VV` と返される。凍結中のPOS整合gateはVVと登録adjectiveの組合せを承認せず、identity_boundary REVIEW / unknown_or_unresolvedを返す。

正式候補の実際の用例：`"저는 졸려요."`。結果：planned新出IDがmissing、controlled coverage 99.13%、hard reject。韓国語の自然さと登録・解析器のPOS整合は別問題である。

同じ候補内での短いfocused probeでも `저는 졸려요. / 졸린 친구가 집에 가요. / 저는 졸리고 피곤해요. / 졸려서 집에 가요. / 저는 졸리니까 집에 갈 거예요. / "졸려요."` はいずれも対象lemmaをVVとして返した。これはparagraph/full scopeのみの不一致ではなく、sentence-local gate自身の不整合である。活用結果の生データは別audit JSONに保存する。

新出語を削除したり、別語へ置換したり、登録IDを欠いたままcommitすることはplanned==actualに反する。作者annotationによる無条件承認も行わない。通常のprose retryで直せるという根拠がなく、production中のcode/DB/resolver変更は禁止されているため、構造障害として停止した。max5 exhaustionやcontract max3 exhaustionを偽って理由にしない。

## 状態

停止直後：epoch=66、最終commit=K1-066。ko_k1_0419と同じ教材のko_k1_0420はactual_first=null、actual_texts=[]、exposure=0。候補067をintro/review/debt/genre/sceneへ反映していない。失敗候補・raw morphology・正式validation結果を保存した。

## 次に提案する一点（未適用）

別開発フェーズで、登録 `졸리다 / adjective / sleepy` とKiwiの当該lemma VV分類との限定的な互換を検討する。登録ID・sense・活用の妥当性・単文文脈を要求し、VV→adjectiveの一般fallbackにはしない。既存の32文法、語彙800、初出予定を変更しない。positive活用・別lemma negative・planned identity・failed-state isolationを確認してから、別zero-state runで再試験する。今回のrunを成功へ書き換えない。

## もう一つの品質上の留保

K1-027に、作者のUnicode転送ミスによる1文と日本語訳の文字化けがcommit後に見つかっている。これは別のreport-only品質問題として明示し、本文・ledgerを上書きしていない。punctuationとして扱われたそのspanに語彙creditはない。したがって機械的coverage PASSは、全本文の言語品質保証やfinal corpus承認を意味しない。
