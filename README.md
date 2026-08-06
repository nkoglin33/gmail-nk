# gmail-nk

Configuration files for Regency Centers automated Claude Code agents.

## briefing_prompt.md
Full prompt used by the **News & Intelligence Briefing** scheduled agent.
The trigger fetches this file at runtime, allowing prompt updates without recreating the trigger.

## reit_weekly_prompt.md / reit_weekly_template.html
Full prompt + HTML template used by the **REIT Weekly Universe Report** scheduled agent (Mondays 7am CT).
The trigger fetches `reit_weekly_prompt.md` at runtime and follows it exactly; the prompt in turn reads
`reit_weekly_template.html` during assembly.

**`reit_weekly_APPROVED_REFERENCE.html` is the Nick-signed-off ground truth (2026-08-03).** If you edit the
prompt or template, diff the new output against this file before considering the change done â€” a prior
version of this prompt drifted from the approved format for months (April 2026 â†’ August 2026) because the
approved format only ever lived in a separate session's scratchpad and never made it back into this repo.
Don't repeat that: any format change Nick approves belongs in this repo, and this reference file should be
updated to match whenever he signs off on a new version.

## grocer_weekly_prompt.md / grocer_weekly_template.html
Full prompt + HTML template used by the **Grocer Weekly** scheduled agent (Mondays 7am CT, same cadence
as REIT Weekly). Companion report covering deal/real-estate activity + performance metrics for 6 major
national grocers (Walmart, Kroger, Publix, Whole Foods Market, Trader Joe's, Wegmans; sub-brands rolled
up under the parent). Built 2026-08-06 from a manually-built pilot issue Nick reviewed and approved for
production ("Love it. Please put this into production on the same cadence as REIT Weekly.").

Uses the same Gmail-sanitizer armor rules and carry-forward persistence model as REIT Weekly: `gw_deals.html`
and `gw_performance.html` are the living state the trigger reads/updates each cycle (not reset from scratch
weekly) â€” see the prompt's Step 1 for exactly when to refresh vs. carry forward. Seeded 2026-08-06 with the
approved pilot's research as the initial baseline (4 days old at seed time).

**`grocer_weekly_APPROVED_REFERENCE.html` is the Nick-signed-off ground truth (2026-08-06).** Same diffing
discipline as the REIT Weekly reference file above â€” any approved format change belongs in this repo.
