# Let's Play and gameplay

Gameplay, Let's Play, and chess-puzzle guidance extending the main vlog workflow. Philip's current instructions and the accepted version take precedence over past game examples; the recipes below are examples to adapt, not a mandate for other videos.

## Inputs and sync

- Inspect the actual OBS tracks and Osmo/facecam recordings. A common OBS layout is track 1 mix, track 2 game, track 3 Blue Yeti; verify rather than assuming. Philip previously chose the raw Yeti as the voice source. Keep game audio separate and preserve the full game window where cropping would hide UI.
- Build proxies at a suitable review resolution. If concatenating proxy chunks, use exact frame/outpoint limits and check the full proxy duration: extra frames per chunk previously caused seconds of drift. Correlate camera and microphone audio at the start, middle, and end; compare proxies against original frames and account for fractional frame rates.

## Edit for gameplay

- Choose entertaining reactions, observations, and successful moments; preserve what he is talking about. If he announces an action, keep the footage through its result, not just the spoken line. Give reactions context. Keep the gameplay synchronized with its original speech when moving a passage.
- A teaser, title, introductory talk, transition to gameplay, main section, and end are useful options, not mandatory cards. Follow his requested sequence and avoid generic template elements he did not choose. Chess puzzles have different cutting and outro rules in Chess puzzle sessions below.
- Keep the whole game area visible; letterbox rather than crop important content. When window size changes, measure the actual content rectangles. Use the chosen facecam size, crop, and placement; do not cover important HUD elements. A prior accepted gameplay layout used a centered 4:3 rounded facecam with a cyan ring, with the ring overlapping the edge to avoid a gap. Treat that as a starting point, not a rule for reviews or new games.
- Keep game audio under the voice, with ducking if useful. Preserve actual dialogue and avoid masking it. For reels, follow the main preview guidance; use the vertical phone footage where available, keep the music bed continuous, avoid sound effects, and do not repeat a scene.

## Visuals, thumbnails, and output

- Match graphics to the selected title art and game. Ease additions and preserve the intended speech duration. If the game title or URL is spoken, time any requested callout to the speech. Verify a face-to-bubble transition lands on exactly the gameplay position and crop.
- Philip's past Let's Play thumbnails generally followed the game's title design and used a real frame plus his face cutout. His explicit selection always wins, including an unmodified Canva original; do not generalize a past face requirement to review videos. Inspect background-removal edges and frame contact.
- Use resumable rendering when environment limits warrant it. Render native-resolution footage and overlays for final output, then check the EDL's frame counts, sync, content rectangles, audio, and the whole exported file as described in the main skill. Do not assume an older Mac/network/Canva limitation or fixed rendering speed still applies.

## Chess puzzle sessions

- Treat several recordings of one sitting as one session with one appropriate intro. Choose entertaining and impressive whole puzzles, especially those with explanation, arrows, reaction, or a milestone. Never cut inside a puzzle or remove thinking time; shorten by choosing fewer puzzles.
- The approved chess example ran from a teaser to a title, an intro over the screen showing the rating, the puzzles, and a fun final reaction. It had no outro or end card. This is a chess-specific preference, not a general vlog rule.
- During a non-puzzle page, show the full page with facecam; switch to the puzzle layout after the board loads. The prior layout cropped the board on the left, kept a right information panel and rating row, and used a large facecam with a cyan ring. Re-measure coordinates for each recording: zoom and window size can change.
- To locate puzzles, sample keyframes and OCR rating/status; detect board motion to find each load and confirm the result on a source frame. Orange arrows can help identify interesting explanations. These are aids for candidate selection, not proof the full puzzle is present.

## Capture and rendering

- A common capture has separate OBS mix/game/mic tracks and a 29.97 fps Osmo HEVC facecam. Confirm the actual files. For mixed 30 and 29.97 fps sources, calculate timestamps and frame/sample counts from actual rational rates; 48 kHz audio is exactly 1600 samples only at true 30 fps.
- In a 4K facecam pipeline, crop the captured game and scale it to the output, preserve the requested content rectangle, make a correctly sized rounded alpha mask for the facecam, and composite the ring over its edge. Start the transition at the actual speaking/action cue and match its end to the main layout.
- For transparent VP9 overlays, retain alpha throughout; ffmpeg may need `-c:v libvpx-vp9` before the input. Keep overlay parameters and the edit list in one source of truth so review and full-resolution renders agree. Render text and artwork at target resolution from source files rather than enlarging a flattened preview.
- Use resumable, frame-exact pieces when execution or resource limits require them. Verify frame counts, timestamps, and audio continuity after concatenation; AAC padding or filter delay must not accumulate. A shell timeout from a past environment is not a universal limit.

## Sound and thumbnail notes

- The OBS microphone track was Philip's preferred voice source in past Let's Plays; a light high-pass/noise-reduction chain with controlled gain and a limiter worked better than strong isolation. Don't mute gaps with a transcript gate. When mixing game sound, retain speech clarity without flattening or erasing natural reaction audio.
- For a requested Let's Play thumbnail, use the chosen title's typography and colors and a relevant real game frame. A face cutout was preferred for past gameplay thumbnails; if he chooses a plain Canva design, use it unchanged. A specifically requested screenshot-only variant can keep the UI and add only a small cutout at the requested edge. Inspect the edge of the cutout at full size.

Past audio reference: `highpass=f=80,afftdn=nr=6:nf=-55` was a light starting point, followed by appropriate gain and a limiter. Use `level=disabled` on ffmpeg's `alimiter`; its automatic level can push peaks back to full scale. Work in float until delivery when practical, check the pre-encode mix for clipping, and measure the final integrated loudness and true peak. Past work targeted about −16 LUFS, but measure and adjust to the current program, not to a blind gain value. Avoid automatic isolation, aggressive EQ/de-essing, and muting between phrases. Preview any processing change against the current approved mix.

The former chess example used chess.com green `#81b64c` and dark `#262421`, an opening question with an animated rating, and a larger facecam on non-puzzle pages. Its 4K facecam and board coordinates were specific to that capture; do not reuse them without measuring. During candidate detection, sample board motion near a result, use rating/status OCR as a guide, and inspect that the complete puzzle from load to outcome is retained.
