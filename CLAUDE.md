# Postdoc Radar – how this project fits together

Read this before changing the app. The owner asks Claude for changes in plain words; keep both copies in step.

## The three pieces
1. **claude.ai page (source of truth for the app code):** https://claude.ai/artifact/2FnyExuMsWGiBPdFg2JHWM
   - Read it with the Artifact tool (`action: "read"`), edit, and republish to the same URL.
   - Its database holds the posting list (`jobs` collection, `meta/info`); each signed-in viewer's tracker lives under `data/users/<id>`.
   - Capabilities: `db` (rules: `jobs` and `meta` write `admin`), `user`, `downloads`.
2. **This repo / website:** https://mockingchicken.github.io/Postdoc-radar/ (capital P – Pages paths are case-sensitive).
   - `index.html` is NOT hand-edited. It is generated from the claude.ai page: the page's `buildStandalone()` function packages the page's own markup, styles and script plus a snapshot of current postings. Build it by loading the page code with the current postings (e.g. headless Chromium with a mock `window.claude` whose db serves `jobs.json`) and saving `buildStandalone()`'s output as `index.html`.
   - `jobs.json` is the live list. The app (website and downloaded copies) fetches `FEED` = `https://mockingchicken.github.io/Postdoc-radar/jobs.json` on open and falls back to its built-in snapshot offline.
   - `tools/build_feed.py` builds `jobs.json` from an ArtifactData export (`list` with `out_dir`) plus `meta/info`.
3. **Daily scheduled task "Postdoc Radar daily search" (06:33 Europe/London):** searches for new roles, writes them to the claude.ai database, then rebuilds and pushes `jobs.json` only.

## Rules when changing the app
- Edit the claude.ai page first, republish it, then regenerate `index.html` from it and push. Never let the two drift.
- Keep the local tracker storage key `postdocRadar.applications.v1` and the tracker document shape (`listed, status, check[], appliedOn, interviewOn, note, log[], custom, updated`) backwards compatible, or people lose their saved applications.
- New posting fields must also be added to the daily task's prompt so new postings carry them.
- Test before pushing: page loads with no console errors, filters work, the tracker survives a reload, backup/restore works, and the live list loads (route `FEED` to a test list).
- Commit as MockingChicken <MockingChicken@users.noreply.github.com>.
