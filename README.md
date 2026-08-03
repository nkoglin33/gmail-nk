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
