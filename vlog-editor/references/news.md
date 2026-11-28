# Tech news and roundup vlogs

Weekly tech news and roundup guidance extending the main vlog workflow—covering research and fact-checking, multi-take talking-head cuts, word-synced 16:9 news graphics, standalone 9:16 category reels, and cross-platform copy. Philip's current instructions override past episode defaults.

## Research, fact-check, and script

- Anchor each episode to a clear date window (for example, the past 7 days). Triage Philip's bookmark export (such as Shiori) and seed links into per-story folders holding verified URLs, screenshots, muted B-roll, and verbatim quotes.
- Fact-check draft scripts before recording and log every catch in a separate notes file. Verify chronology, numbers, specs, speaker attributions, and exact quote boundaries so Philip's commentary never falls inside quotation marks.
- Preserve his voice, jokes, and pacing in the cleaned teleprompter script; batch open editorial questions separately instead of silently changing his opinions.
- A local review and teleprompter app (served via `portless` at `--tld dev`) works well for script reading and side-by-side review of cuts, thumbnails, and recuts.

## Multi-take edit and pacing

- News episodes often span multiple 4K camera and external-mic takes. Sync each take independently at the start, middle, and end before building a single frame-exact EDL that picks the best sentences across takes.
- Skip a standalone title stinger between the cold open and Chapter 1 when a direct cut keeps better momentum, fading the intro music bed to zero right before Chapter 1 speech begins.
- When the cold open needs pacing options, render 2–3 short (~25 s) standalone intro recuts (for example single-take, multi-take hybrid, and tightened pauses) without modifying the main cut until Philip picks one.

## Horizontal visuals and quote hygiene (16:9)

- Framing: a feathered left-half talking head paired with a live Table of Contents or recap panel works well for the cold open and outro; switch to a floating bottom-right rounded PiP during main chapters so visuals get the full canvas without covering Philip's face.
- Enforce 3-state quote timing on every cited passage: keep the card off during pre-quote setup, show it only across the exact spoken quote span with left-to-right sentence highlights synced to word timestamps, and dismiss it the moment Philip's opinion resumes.
- Distinguish verbatim quotes from indirect speech. Never put quotation marks around paraphrased claims and never label a card "Direct Quote"—use an explicit paraphrase/summary badge for indirect claims, and reserve quotation marks (with circular profile avatars for X/social posts) for verbatim quotes.
- Use real market/price data series rather than synthetic curves, time reveals to the exact spoken word (for example wait for "long term" before drawing a multi-decade chart), and keep dense visuals such as stock heatmaps unblurred when he references them.
- Automatically pillarbox non-16:9 screenshots over a blurred matching backdrop, avoid plain-black or empty scene backgrounds, verify every referenced logo or media file exists before rendering (watch for blank icon fallbacks), and embed native `FFMETADATA1` MP4 chapters alongside `chapters.md`.

## Standalone vertical reels (9:16)

- Spin 1–2 minute self-contained vertical reels out of individual news segments (for example Models, Markets, Gaming, Indie Apps, or a single breakout story) using the same source takes and brand kit, closing with a 3-second full-frame end card promoting the main episode.
- Split-screen layout: Remotion top visual canvas over centered bottom facecam, opening with a 1.2 s thumbnail hook card (frame 0 / ~frame 12 doubles as the thumbnail), burned-in uppercase word-highlighted captions (fixing brand spellings and split tokens like `401(K)S?`), and topic/quote cards.
- Prevent a `0:01` facecam double-cut by freezing the bottom facecam under the hook card on the exact decoded first frame of the first speech clip using the identical seek pipeline; similarly hold the closing speech frame under the fading end card.
- Thumbnails: use clean, dark/high-contrast backdrops (not busy bright screenshots behind text), include the subject's official vector icon/logo, and size key stat callouts generously for phone screens. On macOS, Apple Vision (`VNDetectFaceRectanglesRequest`, `VNGeneratePersonSegmentationRequest`) handles face centering and person cutouts cleanly.
- Music arc: brief swell on the 1.2 s hook, smooth duck and fade out by ~4 s, quiet transition ticks (`−25 dB`), and a gentle outro swell under the 3 s end card fading cleanly to silence before EOF.

## Remotion 4K pipeline, QA, and publishing

- For native 4K Remotion delivery from 720p base compositions, pre-bundle once (`remotion bundle` with `stdin=DEVNULL`), render with `--scale=3` (`3840×2160` or `2160×3840`) via headless Chrome, normalize every concat piece to `-video_track_timescale 30000`, and composite native 4K camera footage with `h264_videotoolbox` on Apple Silicon while reusing the approved audio mix unchanged.
- Before sending a rough cut, build and inspect a visual judge packet: labeled contact sheets plus a manifest pairing every scene, pre-quote setup, early/late quote clause, and post-quote opinion frame with the exact spoken words (±3.5 s). For 4K finals, inspect 100% native crops and disclose any raster inserts limited by source resolution.
- For Buffer / cross-platform copy (YouTube Shorts + Instagram Reels): enforce Instagram's hard cap of **5 hashtags** combined across caption and first comment (keep hashtags out of the first comment when the caption already has 5; use the first comment for link/CTA and an engagement question), use **3–5 hashtags** on YouTube (first 3 show above the title), and supply copy-paste blocks plus 2–3 title options.
