# Phase 3.6b run contract

Only the author guidance changes: see `ko_k1_phase3_6b_author_prompt.md`.

`k1_phase3_6b.ProductionGate` inherits Phase 3.6a's submit, author approval and atomic commit methods without overriding them. Its constructor supplies a new output directory, a new zero-state ledger and the already supported runtime limit `max_text=50`. The existing candidate schema already accepts 001–050. This is range/output bookkeeping, not a new validation, resolver, scheduler or ledger rule.

The CLI uses the same live local author/file callback as Phase 3.6a. Each `begin` obtains a snapshot from actual committed history. `plan` closes scene-planning timing before prose drafting starts. `validate` journals a candidate without exposure credit. `commit` requires explicit post-mechanical author review and a matching final raw analysis. A failed candidate never changes the actual ledger. Each subsequent `begin` requires the previous text's committed state.

Freeze watches all Python engine/test files, active configuration JSON and the author overlay. Production code and prompt changes are prohibited after start. Existing artifact manifests additionally freeze all earlier results. Structural problems stop this run instead of prompting an engine patch.

Pre/post regression are each run once. Candidate checks use the existing gate. Ten-text checkpoints check sealed state, text projections and hashes without running full regression or resetting state. Full zero-state raw ledger replay occurs only after completion or STOP and is outside production timing.

Time is measured with the monotonic clock across controller invocations. Planning, drafting, repair and author review include the live model's reasoning and tool/file transport. Setup, development, full pre/post regression and final reporting/replay are separated. This measures this local production workflow, not isolated external API inference throughput. A 300-text extrapolation is indicative and excludes later-stage workload growth and final human quality review.

The full 300-text production is not authorized by this run. Stop at 050 even on success.
