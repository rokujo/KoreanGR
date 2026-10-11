# Controlled lexical surface recovery — Phase 3.6c

This version adds an evidence overlay and preserves all raw morphology. Earlier runs and engines remain frozen. Production-lite semantic grammar warnings remain diagnostics, not commit blockers. Phase 3.6b's author prompt is reused unchanged.

All 800 active entries are classified in `controlled_surface_recovery.json`. This registry does not add vocabulary, senses or productive forms. `unique_safe` is a candidate classification, not blanket permission: exact original lemma span, current actual snapshot membership, nominal position, permitted nominal raw parts, contiguous character partition and exclusive unresolved annotation group are all required. Known noun homographs such as 시장/은행/밤/비/해/차/말 remain context_required. Predicate inflections are morphology_required and stay with the frozen morphology hints/specific resolvers. Unimplemented context-required words are deliberately not recovered.

Existing 네/아니요/한국어/우리 modifier/마셔요/걷다/grouping resolvers run first. The new context rule for 우리 requires a contiguous exact 우리 span, immediately attached 는/JX, independent short-scope NP and registered we identity, speaker-group discourse evidence, a human-group verb and no enclosure/spatial noun frame. Current snapshot permission and nonconflicting annotation indices are mandatory. Generated annotations cannot authorize a recovery. Raw NNG is retained in diagnostics. Evidence-poor cases remain REVIEW and may trigger structural STOP.

Scope parity compares planned new words, risky words and every inspected recovery target across sentences, paragraphs and full text. Different registered identities are compared as well as unresolved identities. Safe convergence is recorded separately from unresolved structural mismatch.

The new gate subclasses the frozen atomic gate. Its mechanical, coverage, construction, scheduler and transaction logic is unchanged; analyzer dependency and state input hash additionally include this overlay. The production class inherits the existing retry/stagnation and author approval methods, and dispatches to the new analyzer gate through its shared-base method resolution order.

Before candidate submission, the author invokes one sentence-level lexical preflight on the draft. It creates diagnostics only, never an exposure/state transaction. Future findings can be repaired in prose before formal submission. Preflight findings are reported separately from formal candidate contamination and first-attempt PASS rates so improvement is not hidden by prefiltering. No parser, configuration or prompt changes are permitted after production_start.

For timing, complete the planning command in one tool call, then compose prose in a later call. Preflight CPU time is recorded separately and subtracted from elapsed author-draft time. Draft/repair times still include live model reasoning and file transport, not isolated API inference latency.
