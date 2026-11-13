---
name: lets-play-editor
description: Edit Philip's gameplay, Let's Play, and chess-puzzle vlogs, including OBS capture, facecam, game sound, gameplay-aware cuts, and game-specific graphics. Use with vlog-editor; do not route ordinary talking-head reviews here merely because they use a facecam.
---

# Let's Play editor

First read the shared [vlog editor](../vlog-editor/SKILL.md). This skill adds gameplay-specific guidance; Philip's current instructions and the accepted version take precedence over past game examples. For chess puzzle sessions, also read [chess and production recipes](references/gameplay-recipes.md).

## Inputs and sync

- Inspect the actual OBS tracks and Osmo/facecam recordings. A common OBS layout is track 1 mix, track 2 game, track 3 Blue Yeti; verify rather than assuming. Philip previously chose the raw Yeti as the voice source. Keep game audio separate and preserve the full game window where cropping would hide UI.
- Build proxies at a suitable review resolution. If concatenating proxy chunks, use exact frame/outpoint limits and check the full proxy duration: extra frames per chunk previously caused seconds of drift. Correlate camera and microphone audio at the start, middle, and end; compare proxies against original frames and account for fractional frame rates.

## Edit for gameplay

- Choose entertaining reactions, observations, and successful moments; preserve what he is talking about. If he announces an action, keep the footage through its result, not just the spoken line. Give reactions context. Keep the gameplay synchronized with its original speech when moving a passage.
- A teaser, title, introductory talk, transition to gameplay, main section, and end are useful options, not mandatory cards. Follow his requested sequence and avoid generic template elements he did not choose. Chess puzzles have different cutting and outro rules in the reference.
- Keep the whole game area visible; letterbox rather than crop important content. When window size changes, measure the actual content rectangles. Use the chosen facecam size, crop, and placement; do not cover important HUD elements. A prior accepted gameplay layout used a centered 4:3 rounded facecam with a cyan ring, with the ring overlapping the edge to avoid a gap. Treat that as a starting point, not a rule for reviews or new games.
- Keep game audio under the voice, with ducking if useful. Preserve actual dialogue and avoid masking it. For reels, follow the parent preview guidance; use the vertical phone footage where available, keep the music bed continuous, avoid sound effects, and do not repeat a scene.

## Visuals, thumbnails, and output

- Match graphics to the selected title art and game. Ease additions and preserve the intended speech duration. If the game title or URL is spoken, time any requested callout to the speech. Verify a face-to-bubble transition lands on exactly the gameplay position and crop.
- Philip's past Let's Play thumbnails generally followed the game's title design and used a real frame plus his face cutout. His explicit selection always wins, including an unmodified Canva original; do not generalize a past face requirement to review videos. Inspect background-removal edges and frame contact.
- Use resumable rendering when environment limits warrant it. Render native-resolution footage and overlays for final output, then check the EDL's frame counts, sync, content rectangles, audio, and the whole exported file as described in the parent. Do not assume an older Mac/network/Canva limitation or fixed rendering speed still applies.
- See [gameplay recipes](references/gameplay-recipes.md) for chess-puzzle selection/layout and tested capture, audio, and transparency details. They are examples to adapt, not a mandate for other videos.
