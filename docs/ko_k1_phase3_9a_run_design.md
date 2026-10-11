# Phase 3.9a author contract retry

The only self-check schema source is
`config/languages/ko/k1/author_selfcheck.schema.json`. The six names and true
constants migrate the existing Phase 3.9 controller contract; optional notes
remain a string. No invented decisions/enums are added. Tests, controller and
template generator all read the same schema. Unknown properties are rejected.

Malformed JSON or schema errors create contract journals and timing only, not
candidate attempts or actual exposure state. Three failed schema submissions
at a text exhaust the contract budget; a first error followed by correct JSON
continues. `author_contract_retry_count` counts failed contract submissions;
initial valid output is zero. Recovered failures are separately counted.
Formal max5 remains independent. Korean, Japanese and title are bound by a
digest during retry. Content changes are refused until the original body is
restored; ordinary prose repairs follow successful contract validation.

The production controller is a new run/path adapter. Mechanical evaluate and
atomic commit are byte-identical to Phase 3.9 / 3.8. Old run artifacts are hash-
frozen. Existing 100-ID schemas, analyzers, senses and grammar are unchanged.
Planner health/proposals/debt functions are imported unchanged. Added observed
wind/message patterns are author warnings only; they never become hard gates.

Each draft uses actual allowed snapshot and at most three debt bundles. Natural
scene fit overrides urgency. Credits require actual canonical occurrences.
No future review, no quota-driven side events, no silent payment. Checkpoints
025/050/075/100 use capped six-exposure progress and required future rate to 300.
Expired debt alone does not stop the run. Only mathematical infeasibility does.

After production start, code/config/schema/prompt/planner are frozen. Author
prose repairs and self-check JSON repairs alone are allowed. Fresh zero-state
run ends at 100. No automatic continuation to 101..300.

Benchmark uses live file-based LLM author wall time including reasoning and
tool transport. Pre/post full tests, report-only historical audit and ledger
replay are engineering/verification, not production time. Formal first pass
is after self-check/preflight; it is not raw first-writing compliance.
