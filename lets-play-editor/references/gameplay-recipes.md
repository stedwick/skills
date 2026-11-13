# Gameplay recipes

Read this reference for chess-puzzle editing or detailed Let's Play implementation; the parent and current request control shared choices.

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
