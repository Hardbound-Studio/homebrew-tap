# homebrew-tap, session card

The studio's own Homebrew tap, github.com/Hardbound-Studio/homebrew-tap (Affan's MCQ 2026-11-25). One cask per
Mac app, each pointing at the same notarised Developer ID zip its website serves.

1. Owner: Project 12 (channels.tsv row `Homebrew`, card 3, ledger p12dir). App projects hand P12 the new zip URL and
   sha256 on each Mac release; P12 bumps the cask the same day (duty SD93).
2. A tap is our own and is not a listing: it never goes on a site's Listed-on strip (SD32, SD90); the brew line sits
   beside the Mac download (hardbound-site D-W268).
3. Pushed nightly by C:\dev\dev-repos-push.ps1. Plain git in this repo; never rewrite history.
4. The flow it is part of: ESTATE-STANDARD 18.17 (C:\Affan Local Drive\Memory\ESTATE-STANDARD.md).
