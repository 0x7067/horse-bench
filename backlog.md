# Backlog

## In flight
## Queued
## Done
- [x] horse-recordings - Record four horses at 1080p60 (done 2026-10-03)
  Owner: current Codex task. Capture GPT 6.1, Opus 5.5, Luna 6, Muse Spark as MP4 and provide files in chat.
  Four 10-second H.264 MP4s captured at fixed 1/60-second timesteps from original HTML. ffprobe confirms 1920x1080, 60fps, 600 frames each; sampled frames show motion. Files: docs/recordings.
- [x] horse-prefetch - Prefetch neighboring horses (done 2026-10-03)
  Owner: current Codex task. Add versioned prefetch hints for previous and next HTML, verify targets and browser requests, deploy.
  Deployed: all 20 public pages match local HTML. Verified two correctly versioned neighbors per horse and Chrome issued both requests with sec-purpose: prefetch, HTTP 200. Safari not verified.
- [x] horse-mobile-controls - Normalize mobile horse controls (done 2026-10-03)
  Owner: current Codex task. Two generated pages lack viewport metadata, including MiniMax M3 from the screenshot. Normalize published viewport metadata and verify all pages.
  Deployed normalized viewport tags. All 19 pages passed Chrome 390x844 mobile emulation: scale 1, visible 44x44 buttons. Public MiniMax, DeepSeek Pro, and GLM HTML matches local output. Physical Safari not tested.
- [x] horse-overlay-fix - Fix missing horse navigation overlays (done 2026-10-03)
  Owner: current Codex task. Example page overlay is visible in fresh Chrome. GitHub Pages headers advertise max-age=600. Next: check visibility on all live pages and identify whether user browser caching explains missing controls.
  Deployed versioned gallery and overlay links. All 20 public pages match local HTML. Overlay visible on all 19 horses in fresh Chrome; missing controls not reproduced and user cache remains unconfirmed. Evidence: verification.json.
- [x] horse-navigation - Add navigation overlay to horse pages (done 2026-10-03)
  Owner: current Codex task. Completed: all 19 published horse pages have icon-only previous, gallery, and next navigation, with model/effort and run count. Verified browser navigation and wraparound, viewport bounds, all inline JavaScript, and all 20 live URLs matching published files. Evidence: verification.json.
  Navigation overlay deployed at https://0x7067.github.io/horse-bench/; evidence in verification.json.
- [x] horse-runs - Add harness selection and run requested horse models (done 2026-10-03)
  Owner: current Codex task. Completed: all 19 harness/model runs returned HTML; scripts, configurations, logs, and results committed to 0x7067/horse-bench. GitHub Pages deployed at https://0x7067.github.io/horse-bench/. Evidence: verification.json records all 19 JavaScript syntax checks, 19 browser canvases, and 20 live URLs matching local files. Index shows harness, model, effort, provider; filtering checked.
  Published https://0x7067.github.io/horse-bench/ with all 19 results. Verification evidence: verification.json.
