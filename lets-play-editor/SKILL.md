---
name: lets-play-editor
description: Edit Philip's YouTube Let's Play / gameplay recordings (OBS screen capture + DJI Osmo facecam) into a polished video: sync, transcript-based cut, clean voice audio, Remotion title/callout/end cards, facecam bubble, previews, final 4K, and the YouTube thumbnail (Canva options + real frames + face cutout). Use whenever he asks to edit, cut, preview, fix or render a Let's Play, gameplay video, rough cut, facecam recording or video thumbnail, even if he doesn't say 'Let's Play'.
---

# Let's Play editor

Turns an OBS screen recording and a DJI Osmo Pocket facecam recording into a finished YouTube video.

Work is split across two machines, because each is good at different things:
- **Philip's Mac** (device shell, `~/mnt/Movies` = `/Users/philip/Movies`): all decoding and encoding of the big 4K sources. The files are tens of GB, so they never leave the Mac.
- **Cloud container**: transcription, audio math (numpy/ffmpeg on WAVs), Remotion graphics. Small files move across with stage/commit.

## How Philip wants to work

- **Preview before doing the whole thing.** This is the most important rule, and he has had to repeat it. For every change, fix or new idea, first send the smallest thing that lets him judge it: a 10–40 s clip of only the changed moment, an audio before/after (same 20 s twice, separated by 1.5 s of silence), or a still frame. Do the full job only after he says yes. The full 4K render happens once, at the end, when he asks for it.
- When one segment changes, redo only that segment; when only audio changes, remux (never re-render video).
- Report progress with 💻 (doing) ✅ (done) ⏳ (to do) ❌ (blocker) 🙋‍♂️ (needs you). Succinct bullets, simplified technical English.
- All animations eased (`Easing.bezier(0.65,0,0.35,1)`), with ElevenLabs SFX on motion (whoosh on moves, soft pop on text).
- Spell names exactly as he gives them (e.g. his coworker is "Aron"). Ask if a name or URL is uncertain rather than guessing.
- Measure before saying something is done or broken: frame counts, durations, loudness, peaks, still frames. He listens closely; one false "the audio is silent" report cost trust.
- State costs of paid API calls (ElevenLabs) and prefer the free option when quality is close.

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
- Pieces are `[startFrame, nFrames, layout]`; keep the EDL as JSON so every later step (video pieces, audio, overlay timing) reads the same source of truth.
- Send a short list of timecodes worth checking when sending a rough cut.

### 5. Audio
Voice cleanup "option C" (free; Philip preferred it to ElevenLabs voice isolation, which costs ~$5 per 25 min take):
```
highpass=f=80,afftdn=nr=12:nf=-50:tn=1,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=4000:t=q:w=1:g=2,deesser=i=0.4
```
Then:
- Gate the voice with a mask from the transcript lines (40 ms fades); mute lines with game bleed.
- Game: `dynaudnorm=f=400:g=31:p=0.9:m=6`, about -2 dB, ducked under voice with `sidechaincompress=threshold=0.03:ratio=4:attack=30:release=400`.
- **Keep everything in float (`pcm_f32le`) until the final AAC.** 16-bit intermediates clip silently.
- After the big voice gain (~+13 dB), add a gentle compressor and lookahead limiter, not just gain:
  `volume=13.1dB,acompressor=threshold=0.25:ratio=3:attack=8:release=150:knee=4,alimiter=limit=0.7:attack=4:release=60:level=disabled`
  Why: the voice peaked at -3.6 dBFS, so +13 dB hard-clipped 10% of speech and Philip heard it as distortion in the 4K file.
- **Always `level=disabled` on `alimiter`.** The default auto-level scales the output back up to 0 dBFS, undoing the limiter.
- Loudness: **-16 LUFS** integrated, peaks ≤ -1 dBFS, done as plain gain + `alimiter=limit=0.84:attack=5:release=80:level=disabled`. -14 LUFS forced too much limiting on speech.
- Mix SFX from the overlay webms with `adelay`, `amix=normalize=0`, and map only the labeled output (`-map "[o]"`), or a stray video stream from the webm gets into the AAC.
- Check every audio deliverable: `astats` Peak count / Flat factor (clipping shows as thousands of peak samples and a non-zero flat factor) and `ebur128=peak=true`.

### 6. Graphics (Remotion, container)
- Remotion 4.x project with fonts from @fontsource (Silkscreen for pixel games, Inter, Cormorant Garamond). Load the official remotion skills if present.
- Per video: **title card** (logo, ElevenLabs music `eleven_music_v2_5` ~$0.30/30 s, URL easing in ~1.7 s with a pop, 8 s), **lower-third callouts** when he mentions something ("Made by …", genre, "Play free in your browser – url", "Coming up next"), **end card** (Thanks for watching + play-this card + Watch-next card, ~11 s). Match colors to the game.
- Callouts: transparent VP9 webm (`--codec=vp9 --image-format=png --pixel-format=yuva420p`). ffmpeg must decode them with `-c:v libvpx-vp9` placed before `-i`, or alpha is lost.
- For 4K: `--scale=2` on 1080p comps, `--scale=3` on 720p comps.
- Transition `FaceToBubble` (36 frames = 1.2 s): game fades in while scaling 1.06→1; the facecam box moves from full frame to the bubble while its crop moves from the 16:9 face crop to the 4:3 head crop; corner radius grows; the ring fades in over the last 40%. Feed it two short clips cut from the sources (the last frames of the talk and the first frames of main). Its end frame must match the bubble used in the main pieces exactly, or there is a visible jump.

### 7. Layout
- Talk/intro/outro: facecam full screen (16:9 crop around the face).
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

### 9. Finish
- Keep per-segment files: video-only `<seg>_v.mp4` and `<seg>_audio.m4a` for tease/talk/main, plus title/transition/end card. Mux each, then `-f concat -c copy -movflags +faststart` into `~/Movies/<Game> Let's Play - 4K.mp4`. Because of this layout, an audio fix is a ~2 min remux.
- Verify: every piece's frame count equals the EDL, final duration, overall loudness/peak, still frames at each callout and at the end card. Small (~60 ms) audio padding at segment ends is normal with concat and does not accumulate.

## Thumbnail

Philip wants the thumbnail made "with Canva", but the result must use **real frames from the video and his real face**. What worked:

1. **Confirm which video** if he says "this video" and more than one is in progress (a wrong guess cost a round).
2. **Direction from Canva.** `generate-design` with `design_type: youtube_thumbnail` and a detailed query describing the video's own title card (colors, fonts, layout, tagline) returns 4 candidates. The candidate thumbnail URLs cannot be fetched; to *see* them, `create-design-from-candidate` and then `read-design` with `fields: ["design_content","thumbnails"]` (this also gives element positions, fonts and colors). Send him the candidate links and let him pick; he may combine (e.g. layout from one, glow from another).
3. **Know Canva's limits here.**
   - File uploads (`create-upload-url` → POST) are blocked by the network allowlist (`www.canva.com`) from both the container and the Mac, so real frames can't go into a Canva design unless he allows that domain or drags the files in himself.
   - The edit API cannot add text effects (glow, shadow) or change font family; glow is one click in Canva (Effects → Glow) if he edits there.
   - Cancel any editing transaction you open just to read a design.
4. **Build the final as HTML/CSS → PNG** with Playwright (1280×720 page, `deviceScaleFactor: 2` → 2560×1440), matching the chosen Canva layout:
   - Background: a real gameplay frame from the 4K source (make a contact sheet of candidate moments, pick the most iconic, e.g. Samsara's shipwreck beach at 1:20), darkened: `filter: brightness(.42) saturate(.85) blur(1.5px)` plus a radial vignette.
   - Wordmark glow (from Canva option 4, amber): `color:#ffd79a; text-shadow:0 0 6px #ffb347,0 0 18px rgba(255,150,50,.9),0 0 42px rgba(255,120,30,.75),0 0 90px rgba(255,100,20,.55)`. Fonts via @fontsource (DM Serif Display matched Canva's bold serif; Inter for small caps).
   - Face on the side opposite the text, large, cut off at the bottom edge, with a soft warm light behind it for separation.
5. **Face frame.** Contact sheet of ~8 frames from the talk/intro segment of the Osmo original; pick an expression that fits the game (skeptical for a murder mystery, excited/explaining for a survival game). Extract a 2000×2000 crop at full resolution.
6. **Cutout.** `rembg` with **`isnet-general-use`** on the frame resized to ~1400 px: keeps real hair strands and clean edges around headphones and hands. `u2net_human_seg` flattened the hair and kept a patch of wall; `birefnet-portrait` runs out of memory in the 8 GB container. Where the cutout is cropped at a frame edge, fade the alpha over ~160 px so no hard line shows. Check the cutout on a bright contrasting color before compositing.
7. **Deliver** the PNG to `~/Movies/<video dir>/thumb/` and send a JPG preview in chat; iterate on the preview (version numbers v1, v2…), not on a Canva design.

## Moving files between the container and the Mac
- Container → Mac: put the file under `/mnt/user-data/outputs/`, then commit it. Max ~25 MB per file (26.6 MB was rejected with HTTP 400); re-encode (e.g. AAC 128k for long rough-cut audio) or split bigger files.
- Overwriting a file under the same name can deliver a stale copy. Use a new filename (e.g. `_v2`) for changed files and verify on the Mac by measuring the file (loudness, duration), not by trusting the upload.
- Mac → container: stage files (for stills to look at, short clips to send in chat).
- Deleting files in connected folders is off by default; write new names instead of relying on `rm`, and clean up stale files from lists before concatenating.
- Small sidecar text files: do not rely on `read` for files without a trailing newline; set values directly.

## Deliverables
- `~/Movies/<Game> Let's Play - rough cut (720p).mp4` during review, `… - 4K.mp4` at the end.
- Previews and A/B files sent in chat for each round of feedback, with one line saying what to listen or look for and the timecodes.
- Thumbnail: `~/Movies/<video dir>/thumb/<Game> thumbnail vN.png` (2560×1440).
