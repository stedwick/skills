---
name: lets-play-editor
description: "Edit Philip's YouTube Let's Play / gameplay recordings (OBS screen capture + DJI Osmo facecam) into a polished video: sync, transcript-based cut, clean voice audio, Remotion title/callout/end cards, facecam bubble, previews, final 4K, and the YouTube thumbnail (Canva options + real frames + face cutout). Use whenever he asks to edit, cut, preview, fix or render a Let's Play, gameplay video, rough cut, facecam recording or video thumbnail, even if he doesn't say 'Let's Play'."
---

# Let's Play editor

Turns an OBS screen recording and a DJI Osmo Pocket facecam recording into a finished YouTube video.

Work is split across two machines, because each is good at different things:
- **Philip's Mac** (device shell, `~/mnt/Movies` = `/Users/philip/Movies`): all decoding and encoding of the big 4K sources. The files are tens of GB, so they never leave the Mac.
- **Cloud container**: transcription, audio math (numpy/ffmpeg on WAVs), Remotion graphics. Small files move across with stage/commit.

## How Philip wants to work

- **Keep this skill up to date without being asked — once the cut is approved.** Don't add intermediary rules mid-edit (they may change). When he approves a final cut, fold his feedback from that video into this skill: edit `~/src/skills/lets-play-editor/SKILL.md`, commit it in `~/src/skills`, and propose the same full text to his Claude account. Mention it in one line.
- **Preview before doing the whole thing.** This is the most important rule, and he has had to repeat it. For every change, fix or new idea, first send the smallest thing that lets him judge it: a 10–40 s clip of only the changed moment, an audio before/after (same 20 s twice, separated by 1.5 s of silence), or a still frame. Do the full job only after he says yes. The full 4K render happens once, at the end, when he asks for it.
- **Short reels (about 30 s): preview the whole thing.** He prefers one low-resolution render (720×1280) of the full reel over a 10 s excerpt. The final high-resolution render still waits for his yes.
- **Change only what he names.** Make each named fix on the last version he liked and keep everything else (cut, pacing, music, shots, overlays). A question such as "Why did you change X?" is a question: answer it, and ask before rebuilding anything.
- **Vertical reels: use his vertical (9:16) phone recording for backgrounds** whenever it has the shot. Use the 4K capture only to fill gaps. Never add dark bars or fades at the top and bottom.
- **Nothing added appears or disappears instantly.** Every added element eases in and out (scale + opacity on the bubble, fade + small rise and scale on captions and portraits). Hard cuts between shots are fine.
- **Face bubble: center his face.** Check crops on several frames across the range; head about half of the circle.
- **Speech gets breathing room: 0.4 s before and after every line**, his and the game's. Never cut at the moment a word ends: transcript word ends are early. Find the real bounds by audio energy. Keep natural phrasing whole instead of chopping between words.
- **No sound effects in reels** (no whoosh, pop, ding or impact). The music bed runs without interruption: never play game audio that has its own music over it. For a real dialogue take, keep the picture and lay the clean voice recordings in sync with it.
- **Reels: never repeat a scene** (same place or action, such as two ramp jumps). Match backgrounds to what is said (show the character who speaks; the place named). Include at least one real dialogue take from the game. A face bubble appears before his first word, never after.
- When one segment changes, redo only that segment; when only audio changes, remux (never re-render video).
- Report progress with 💻 (doing) ✅ (done) ⏳ (to do) ❌ (blocker) 🙋‍♂️ (needs you). Succinct bullets, simplified technical English.
- All animations eased (`Easing.bezier(0.65,0,0.35,1)`), with ElevenLabs SFX on motion (whoosh on moves, soft pop on text).
- Spell names exactly as he gives them (e.g. his coworker is "Aron"). Ask if a name or URL is uncertain rather than guessing.
- Measure before saying something is done or broken: frame counts, durations, loudness, peaks, still frames. He listens closely; one false "the audio is silent" report cost trust.
- State costs of paid API calls (ElevenLabs) and prefer the free option when quality is close.
- Keep answers short and plain, especially when he is frustrated: what went wrong in one line, the fix, one clear question. No tables of options he didn't ask for.
- Follow this skill's choices even when an old file from an earlier approach is lying around; re-check the voice source before every final render.

## Before starting a new video, collect

- Source files: OBS `.mov` and Osmo `.MP4` (ask if not given; they are in `~/Movies`).
- Game name, URL, who made it, logo/title art (screenshot the game's title screen if needed), and what the end card's "Watch next" should point to.
- Anything special: redone intro takes, window resized mid-recording, moments to keep ("oh shit" reactions are fine to keep).

## Inputs

- OBS: 4K30, Hybrid MOV, 40 Mbps. Tracks: 1 = mix, 2 = game (macOS screen capture), 3 = mic (Blue Yeti). Use track 3 for voice, track 2 for game, track 1 only for quick previews.
- Osmo: 4K HEVC 10-bit, 29.97 fps, keyframe every 1 s. Decodes at only ~0.7x realtime on the Mac, so seek straight into the original for each piece instead of decoding the whole file.
- Window/browser captures: show the **whole game area**, letterboxed to 16:9 (black bars are fine; Philip prefers this to cropping off parts of the game). Measure the content rectangle in still frames, per layout (edge detection on row/column differences works). If the window was resized, there are two layouts with a switch time. A game UI panel appearing is not a window move — check before adding a layout switch.

## Pipeline

### 1. Proxies (Mac)
720p proxies, built in chunks that fit a ≤180 s shell call. When joining chunks with the concat demuxer, write `outpoint <chunk seconds>` for each chunk. Without it, chunks overrun by 1–2 frames and the facecam drifts ~2.5 s out of sync over 25 min (this happened on two videos). Check: proxy duration must equal the original's duration.

### 2. Sync
Cross-correlate the Osmo audio with the mic track (envelope correlation, then refine at full sample rate) to get one offset OFF (Osmo time = OBS time + OFF). Check at start, middle and end; if it changes, there is drift — find out why before cutting. Then verify the proxy against the original by PSNR of a frame at ±3 frames (pick a moment with motion); a well-built proxy has zero lag, but one proxy needed a 2-frame correction.

### 3. Transcript
ElevenLabs Scribe (`eleven_scribe_v1`) through Executor (`tools["elevenlabs-mcp"]`): ~$1.70–1.85 per 25 min. Upload flow: `creative_create_asset_upload` → HTTP PUT from the Mac → `creative_finalize_asset_upload`. Free fallback: local sherpa-onnx Parakeet TDT + Silero VAD (no word-level confidence, but good enough to cut).

### 4. Cut (EDL)
- Frame-quantized at 30 fps; audio cut at 1600 samples/frame (48 kHz) so audio and video match exactly. Short (10 ms) fades at each audio join prevent clicks.
- Structure: **tease** (best 6–10 s hook from the gameplay) → **title card** → **talk** (full-screen facecam intro, best take) → **transition** (facecam eases into bubble) → **main** (gameplay + bubble) → **end card**.
- Remove ums, stutters, false starts, dead air, lines garbled by game-voice bleed. Keep genuine reactions and the natural ending. Pick the best of repeated intro takes.
- **Don't cut only around his voice — keep the action he talks about.** When he announces or describes something ("I'm going to cut down this pine tree", "let's go to the police station"), keep the footage until the action is visibly done (the tree falls, the new level loads), even if he is silent. Likewise keep a beat of lead-in before a reaction so viewers see what he reacts to. Typical padding: 0.5–1 s before a line, and after an action line 3–10 s or until the screen shows the result. Check the gameplay (scene changes, game audio, motion between frames), not just the transcript, before cutting a gap.
- Pieces are `[startFrame, nFrames, layout]`; keep the EDL as JSON so every later step (video pieces, audio, overlay timing) reads the same source of truth.
- Send a short list of timecodes worth checking when sending a rough cut.
- **Moving a speech** (e.g. a spoiler warning to ~11:00): move the whole speech piece, not just its callout. Insert it at a natural pause (end of a sentence/scene), and merge tiny neighbouring fragments (<2 s) into one continuous piece so there are no jump cuts around it. The speech brings its own gameplay with it; mention that.
- **Ending music:** let the game's ending music play ~3 s after the credits, then fade it out (~0.6 s) before the closing talk. Not the whole track.

### 5. Audio
**Voice source: the raw Blue Yeti track (OBS track 3) — always.** Philip compared it side by side and chose it.
- **Never use ElevenLabs voice isolation.** It makes his voice garbled/warbly; a whole 4K video had to be redone because of it. Do not reuse an old isolated file "because it exists".
- When comparing voice options, compare **voice to voice, untouched** (raw Yeti vs raw Osmo, same moment, 15 s each). Never add game audio or processing to only one side of a comparison; say exactly what each clip contains.

**Minimal processing (approved):**
```
highpass=f=80, afftdn=nr=6:nf=-55            # rumble + light noise reduction only
volume=+16..22dB (match speech level), acompressor=threshold=0.12:ratio=2:attack=10:release=200:knee=6,
alimiter=limit=0.8:attack=5:release=80:level=disabled
```
- **No transcript gate / no muting between phrases.** Muting the gaps made his talk sound choppy and awkward (chess vlog, Nov 2026); the room tone stays. Remove a garbled or bleed line by cutting it from the EDL, not by muting.
- No EQ and no de-esser by default. The older "option C" (`afftdn=nr=12:tn=1` adaptive, EQ −2 dB @250 Hz / +2 dB @4 kHz, de-esser, 3:1 compression) was "better but not perfect" — the strong adaptive noise reduction thins the voice.
- Game: `dynaudnorm=f=400:g=31:p=0.9:m=6`, about −2 to −4 dB, ducked under voice with `sidechaincompress=threshold=0.03:ratio=4:attack=30:release=400`.
- **Keep everything in float (`pcm_f32le`) until the final AAC.** 16-bit intermediates clip silently. Lesson: +13 dB on a voice peaking at −3.6 dBFS hard-clipped 10% of speech.
- **Always `level=disabled` on `alimiter`** — the default auto-level pushes peaks back to 0 dBFS.
- Loudness: **−16 LUFS** per segment, as plain gain + `alimiter=limit=0.75:attack=5:release=80:level=disabled` (AAC encoding overshoots ~1.3 dB, so 0.84 gave +0.4 dBFS peaks).
- Mix SFX from the overlay webms with `adelay`, `amix=normalize=0`, and map only the labeled output (`-map "[o]"`).
- Check every deliverable: `astats` Peak count / Flat factor (clipping) and `ebur128=peak=true`. A clean final file does **not** prove the mix wasn't clipped earlier — check the pre-normalization mix too.
- **Any change to voice processing gets a preview first:** the intro (talking head) with the new audio, as a short video. Apply to the whole video only after he approves, then swap audio only (remux).

### 6. Graphics (Remotion, container)
- Remotion 4.x project with fonts from @fontsource (Silkscreen for pixel games, Inter, Cormorant Garamond). Load the official remotion skills if present.
- Per video: **title card** (logo, ElevenLabs music `eleven_music_v2_5` ~$0.30/30 s, URL easing in ~1.7 s with a pop, 8 s), **lower-third callouts** when he mentions something ("Made by …", genre, "Play free in your browser – url", "Coming up next"), **end card** (Thanks for watching + play-this card + Watch-next card, ~11 s). Match colors to the game.
- Callouts: transparent VP9 webm (`--codec=vp9 --image-format=png --pixel-format=yuva420p`). ffmpeg must decode them with `-c:v libvpx-vp9` placed before `-i`, or alpha is lost.
- For 4K: `--scale=2` on 1080p comps, `--scale=3` on 720p comps.
- Keep every callout's props (label, text, logo, duration) in one render script, so the 4K versions match the previews exactly.
- A card that goes with a speech stays on screen for the whole speech (at least 10 s). Ease it in smoothly — no flicker (a flickering neon effect was rejected as "weird").
- **URL cards:** when he says a URL (e.g. quillgamemaker.com, pdxpunkgame.com in the closing talk), show it at that word and keep it up until he stops talking; add a second row when he says the second URL.
- When a Canva design can't be exported (blocked download), rebuild it in Remotion from the `read-design` thumbnail and animate it.
- Transition `FaceToBubble` (36 frames = 1.2 s): game fades in while scaling 1.06→1; the facecam box moves from full frame to the bubble while its crop moves from the 16:9 face crop to the 4:3 head crop; corner radius grows; the ring fades in over the last 40%. Feed it two short clips cut from the sources (the last frames of the talk and the first frames of main). Its end frame must match the bubble used in the main pieces exactly, or there is a visible jump.

### 7. Layout
- Talk/intro/outro: facecam full screen (16:9 crop around the face) — unless he is showing something on screen while talking (title screen, character select, a website): then show the gameplay with a **bigger facecam box** (PDX Punk: 320×240 at 720p, 960×720 at 4K) for the intro and the closing talk.
- Gameplay: rounded facecam bubble (4:3 head crop) with a cyan ring (`rgb(62,231,255)`), placed where the game has no HUD. Ask Philip or look at stills. Samsara: middle-right, low enough that the minimap stays visible; pop-ups may be slightly covered.
- Ring must overlap the video edge by a few pixels, so no gap shows at the rounded corners.

### 8. Rendering on the Mac (previews and 4K)
The device shell kills background jobs and each call is limited to ~180 s, so:
- Render pieces in a resumable script: loop over the piece list, skip pieces listed in a `done.txt`, run each piece under `timeout`, append to `done.txt` on success, stop with `PAUSED` after a time budget (~100 s), print `ALL_DONE` at the end. Re-run until ALL_DONE.
- Each piece: `-ss <start> -i OBS -ss <start+OFF> -i Osmo`, filters, `-frames:v <n>`. Add callout webms only to the pieces they overlap (with `-itsoffset` or `-ss` into the webm).
- 4K main piece filter (example values from Samsara):
  ```
  [0:v]crop=<content rect>,scale=3840:2160:flags=lanczos,setsar=1[g];
  [1:v]fps=30,crop=1600:1200:1260:400,scale=720:540[f];[2:v]format=gray[m];[f][m]alphamerge[fb];
  [g][fb]overlay=3036:840[g1];[g1][3:v]overlay=3024:828[b]   (2=mask PNG, 3=ring PNG)
  ```
  For letterboxing, replace the crop/scale with `crop=<content rect>,scale=<W>:<H>,pad=<out W>:<out H>:<x>:<y>:black`.
  Encode `libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 30 -g 60 -an`. Speed: ~1.3 s per second of video; a 15 min video takes ~20 min.
- Previews: same pipeline from proxies at 720p, `crf 24`. For quick sync/framing previews, cut 8 s clips straight from the sources with OBS track 1 audio.
- Before the full 4K, render one 10 s test piece and send it for a sharpness and lip-sync check.
- **Split pieces longer than ~40 s (1200 frames)** into consecutive sub-pieces for 4K (`007a`, `007b`, …); a 109 s piece blew the 170 s per-piece timeout. Splitting at exact frames is seamless.

### 9. Finish
- Keep per-segment files: video-only `<seg>_v.mp4` and `<seg>_audio.m4a` for tease/talk/main, plus title/transition/end card. Mux each, then `-f concat -c copy -movflags +faststart` into `~/Movies/<Game> Let's Play - 4K.mp4`. Because of this layout, an audio fix is a ~2 min remux.
- Verify: every piece's frame count equals the EDL, final duration, overall loudness/peak, still frames at each callout and at the end card. Small (~60 ms) audio padding at segment ends is normal with concat and does not accumulate.

## Chess puzzle vlogs (chess.com Puzzles; approved cut, Nov 2026)

What he wants:
- **Several recordings of one sitting = one continuous session**, one intro. Use the intro take whose goal the video actually reaches ("puzzle rating's 1917, let's get to 2000" — not the 2100 one). Ratings/scores on screen don't need to stay consistent; jump around freely.
- **Content: the most entertaining and most impressive puzzles he solved.** Prefer puzzles where he drew arrows, talked through the idea, reacted ("whoa", "that's a clever one"), or gained more rating (harder puzzle). Always include the milestone ("Oh we made it, 2006!").
- **Never cut inside a puzzle, not even long silent thinking** — "chess is a thinking man's game". Each puzzle runs whole, from the new position loading to the "Solved" message. Shorten the video by picking fewer puzzles.
- **Intro over the screen** so the rating is visible — not full-screen facecam. While he is on another page (his chess.com profile), show the **full screen scaled to 16:9 with the facecam box on top** (same size/place/ring as the puzzle layout) — never the board/panel crop, which splits a non-puzzle page. Switch to the puzzle layout when the puzzle page has loaded (board-wide motion spike).
- Structure: tease (milestone moment, ~9 s) → title card → intro (runs to the end of the first puzzle) → puzzles → end on a fun last reaction ("…that was fun"). **No outro, no end card.** ~20 min = ~30 puzzles.
- **Title card** (Remotion, 8 s, Inter from @fontsource, chess.com colours #81b64c / #262421): faint tilted checkerboard easing in square by square, "CHESS PUZZLES" label, big "Can I hit 2000?", and a rating pill whose number counts 1917 → 2006 and pops green.

Layout (approved): crop the board square on the left (1000×1000 at 40,40 in 1920×1080 design); right column 800 wide = panel top (header, status bubble, score bar; panel y 34–610 at 4K) + the rating row (panel y 1785–1865) scaled ×1.6 on the panel colour + big facecam filling the rest (800×449, 4K crop 2900×1628 at 650,266, rounded 28 px, cyan ring). Measure board/panel per recording (window zoom changed between recordings: board x 912–2171 vs 499–2581).

How to find puzzles (no game audio was captured, so use the screen):
- Keyframes only (`-skip_frame nokey`, every ~1.9 s, very fast) at 960×540 → OCR with tesseract: rating digits, status bubble ("White/Black to move", "Incorrect", "Solved"). A rating change = end of a puzzle; its sign = solved/failed.
- Board motion at 5 fps (192×108 gray, mean abs diff of the board area, ~14× realtime on the Mac): a new puzzle loading is a board-wide jump (mean > 10; fallback the biggest spike > 5 within 8 s after the result message). Span = load → next load − 0.2 s. Check a few span ends on a 4K frame: "Solved" must be visible.
- Arrows: orange pixels on the board (R > G+18, 145 < G < 210, B < 115, R > 180); last-move highlights are yellow-green (G ≥ R) and don't match.
- Name rendered pieces by content (`seg_src_start_n`) so a changed cut reuses unchanged pieces.

## Thumbnail

Philip's standing rules for every thumbnail (he had to repeat them):
- **Base it on the video's own title card** (the Remotion intro made for that video): same logo/wordmark, fonts, colors, tagline and tag. Do not invent a new style or headline ("WHO KILLED HIM?") — that was rejected.
- **Background: a darkened real frame from the video** (an iconic, clean moment without dialogue boxes or UI).
- **He must be in it: his face cut out** from the facecam, large, on the side opposite the text.
- "Make it in Canva" means use Canva for layout/style options of *that* title card; the final is built with the real frame and cutout (see limits below).

**Simple variant (when he hands over game screenshots and says "don't do the whole artwork"):** use his screenshot as is, UI included, with no title, text or darkening. Center-crop it to 16:9, upscale it with Lanczos to 2560×1440, and add only his face cutout, small (~560 px tall at 1440), flush in the bottom-right corner, with a faint cyan (`rgb(62,231,255)`) glow behind it. Fade the cutout's left edge where the shirt is cropped. Keep the cut edges flush with the frame: a drop shadow with padding left a gap, so don't use one. The PDX Punk cutout is saved at `~/Movies/lp2/thumb/face5_cutout.png`. Locally, rembg runs in a scratch `uv` venv (`rembg[cpu,cli]`, with `UV_CACHE_DIR` and `U2NET_HOME` inside the scratchpad).

What worked:

1. **Confirm which video** if he says "this video" and more than one is in progress (a wrong guess cost a round).
2. **Render a still of the title card** (`npx remotion still … <Intro comp> --frame=<after the animation settles>`) and copy its layout. For Samsara that was LET'S PLAY / samsara / line / KEEP THE FIRE ALIVE; for PDX Punk the neon PDXPUNK logo PNG, "A PORTLAND NOIR MURDER MYSTERY" in Silkscreen and the lime "LET'S PLAY · HALLOWEEN" pill.
3. **Options from Canva** (optional, when he asks for Canva). `generate-design` with `design_type: youtube_thumbnail` and a detailed query describing the video's own title card (colors, fonts, layout, tagline) returns 4 candidates. The candidate thumbnail URLs cannot be fetched; to *see* them, `create-design-from-candidate` and then `read-design` with `fields: ["design_content","thumbnails"]` (this also gives element positions, fonts and colors). Send him the candidate links and let him pick; he may combine (e.g. layout from one, glow from another).
4. **Know Canva's limits here.**
   - File uploads (`create-upload-url` → POST) and export downloads are blocked by the network allowlist (`www.canva.com`, `export-download.canva.com`) from both the container and the Mac, so real frames can't go into a Canva design unless he allows that domain or drags the files in himself.
   - The edit API cannot add text effects (glow, shadow) or change font family; glow is one click in Canva (Effects → Glow) if he edits there.
   - Cancel any editing transaction you open just to read a design.
5. **Build the final as HTML/CSS → PNG** with Playwright (1280×720 page, `deviceScaleFactor: 2` → 2560×1440), matching the title card (and any Canva variant he picked):
   - Background: a real gameplay frame from the 4K source (make a contact sheet of candidate moments, pick the most iconic, e.g. Samsara's shipwreck beach at 1:20). Darken it only if it is bright (`filter: brightness(.42) saturate(.85) blur(1.5px)` plus a radial vignette for Samsara's daytime beach). **A night scene stays at full brightness** (PDX Punk: just `blur(1px)`, no vignette).
   - Wordmark glow (Samsara, amber, the look he liked from a Canva option): `color:#ffd79a; text-shadow:0 0 6px #ffb347,0 0 18px rgba(255,150,50,.9),0 0 42px rgba(255,120,30,.75),0 0 90px rgba(255,100,20,.55)`. Fonts via @fontsource (DM Serif Display matched Canva's bold serif; Inter for small caps). For a logo PNG, glow with `filter: drop-shadow(...)` in the game's colors.
   - Face on the side opposite the text, large, cut off at the bottom edge, with a soft warm light behind it for separation.
6. **Face frame.** Contact sheet of ~8 frames from the talk/intro segment of the Osmo original; pick an expression that fits the game (skeptical for a murder mystery, excited/explaining for a survival game). Extract a 2000×2000 crop at full resolution.
7. **Cutout.** `rembg` with **`isnet-general-use`** on the frame resized to ~1400 px: keeps real hair strands and clean edges around headphones and hands. `u2net_human_seg` flattened the hair and kept a patch of wall; `birefnet-portrait` runs out of memory in the 8 GB container. Where the cutout is cropped at a frame edge, fade the alpha over ~160 px so no hard line shows. Check the cutout on a bright contrasting color before compositing.
8. **Deliver** the PNG to `~/Movies/<video dir>/thumb/` and send a JPG preview in chat; iterate on the preview (version numbers v1, v2…), not on a Canva design.

## Moving files between the container and the Mac
- Container → Mac: put the file under `/mnt/user-data/outputs/`, then commit it. Max ~25 MB per file (26.6 MB was rejected with HTTP 400).
- **The transfer rewrites media files** (an .m4a arrived ~6 KB bigger with a changed header). **Gzip media before committing** and gunzip on the Mac; then the bytes arrive exactly. Verify with `md5sum` on both sides.
- For files over 25 MB: encode **one** file, gzip it, `split -b 17000000` the .gz, commit the parts, `cat parts | gunzip` on the Mac. **Never split audio into separately encoded halves** — the second half's encoder padding inserted a 10.7 ms glitch at the join and shifted everything after it.
- Overwriting a file under the same name can deliver a stale copy. Use a new filename (e.g. `_v2`) for changed files and verify on the Mac (md5, duration, loudness).
- Mac → container: stage files (for stills to look at, short clips to send in chat).
- Deleting files in connected folders is off by default; write new names instead of relying on `rm`, and clean up stale files from lists before concatenating.
- Small sidecar text files: do not rely on `read` for files without a trailing newline; set values directly.

## Git and the sandbox
- The device shell is a Linux sandbox, not his Mac's shell: it can't run GitButler (`but`) or push over SSH. For commits/landing in his repos (he uses GitButler), make the change and give him the exact command to run (e.g. `but commit -m "…"`). Plain `git` works only in repos that don't use GitButler (e.g. `~/src/skills`), and needs delete permission for git's lock files — request it before committing, or lock files are left behind.
- Files sent with SendUserFile can land in a `Claude outputs/` folder inside his repos; make sure repos ignore it (`/Claude outputs/` in `.gitignore`).

## Deliverables
- `~/Movies/<Game> Let's Play - rough cut (720p).mp4` during review, `… - 4K.mp4` at the end.
- Previews and A/B files sent in chat for each round of feedback, with one line saying what to listen or look for and the timecodes.
- Thumbnail: `~/Movies/<video dir>/thumb/<Game> thumbnail vN.png` (2560×1440).
