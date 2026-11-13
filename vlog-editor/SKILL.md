---
name: vlog-editor
description: Edit Philip's vlogs from camera and microphone recordings, including transcripts, scripts, synced cuts, audio, graphics, thumbnails, previews, and final exports. Use for talking-head vlogs or as the shared workflow for gameplay and review videos.
---

# Vlog editor

Use this shared workflow for Philip's video edits. For gameplay or chess, also read [Let's Play editor](../lets-play-editor/SKILL.md). For book, film, game, or other subject reviews, also read [Review vlog editor](../review-vlog-editor/SKILL.md). A specialized skill assumes this parent is already loaded; do not recurse between them. For other vlogs, use this skill alone. The current request and Philip's later feedback override examples and defaults.

## Work with Philip

- Report progress in short, plain bullets with 💻, ✅, ⏳, ❌, and 🙋‍♂️ as useful. Explain a mistake plainly and repair only the requested issue on the last version he liked. Keep originals and the editable project.
- Show the smallest useful preview for a new design, edit, or cleanup (a still, 10–40 second clip, or matched audio comparison) and wait for his approval before applying that change throughout, unless he explicitly directs otherwise. For a short reel, preview the whole reel. A full rough-cut request calls for a watchable complete low-resolution cut; the 4K final waits for his request.
- Honor approvals and choices already given for the task. Philip has preapproved downloading Canva assets needed for authorized work; do not keep asking, subject to actual tool permissions. Do not infer approval to publish or make other external changes. Respect any existing ElevenLabs approval; check the cost of a new paid action and do not treat a task-specific approval as unlimited authorization for future projects.
- With each rough cut, list timestamps for major changes and parts needing review. When feedback arrives during work, continue the authorized job and incorporate it.

## Sources, transcript, and edit

- Inspect actual source files, frame rates, audio tracks, duration, and resolution; do not assume OBS, camera, or mic layout. Preserve originals. Use the explicitly selected microphone source. Claps or other shared sounds help sync; cross-correlate audio and check the beginning, middle, and end for drift. Confirm visual sync against the camera, not audio correlation alone. Make the limits of automated measurements clear.
- If requested, send audio to ElevenLabs Scribe or the specified service; honor existing authorization. Deliver both the uncut transcript and an editable, timecoded script. Keep speaker/source timestamps and stable paragraph identifiers so Philip can move or delete text and the edit can be rebuilt from the original recording. Do not add words he did not say unless he records them or requests another method.
- Select coherent, entertaining, observant material while retaining his voice and the intended meaning. Remove mistakes and repeated starts without removing worthwhile jokes or qualifications. Make one frame-accurate edit decision list (EDL) the source of truth for picture, audio, sections, inserts, and animation; update downstream timings when content moves.
- **Never cut speech mid-word or repair it by grafting a tiny word fragment.** For a clipped word, return to the original recording and use the complete sentence or a longer continuous take. Make joins in genuinely quiet gaps, preferably with about 0.4 seconds of breathing room where available. Inspect the original and rendered waveforms on both sides of every changed join; transcript timestamps alone can be early or wrong. Keep the matching picture in sync. If the available take has no clean boundary, preserve more context and preview it rather than making a jittery splice.
- Check edit points after all processing and encoding, not just the source. Filter latency, AAC priming, seeks, resampling, and timestamp discontinuities can move boundaries; verify the actual rendered timeline and prevent cumulative drift. A quiet waveform is evidence, not proof a sentence sounds natural. If you cannot listen, say so and do not claim an audible check.

## Audio and visuals

- Start with gentle noise reduction. For requested de-reverb or quieter breathing, offer a matched before/after; keep room tone and avoid heavy processing, gated silences, warbling, or audible breathing edits. Preserve the approved processing. Do not use ElevenLabs voice isolation for Philip's voice; it previously sounded garbled. Check pre-encode and final peaks/loudness; avoid clipping.
- Treat an approved Canva design as the original, especially when he says no changes. Use Canva templates and animation when requested; do not replace it with a local imitation, alter the design, add Philip, or change the music without direction. Test actual current export/download capabilities rather than assuming an old network restriction. If a requested export is unavailable, explain the blocker and obtain direction before substituting a redesign.
- Keep designs coherent with the selected visual reference. Animate inserts smoothly at relevant spoken moments; preserve alpha, layers, and timing. Review adjacent frames at every insert boundary and edit, including after inserted material, for stale-image flashes. Never replace chosen art or motion with a different style without approval.
- Build a low-resolution review efficiently, but keep original full-resolution footage, editable/vector artwork, and animation sources. For a 4K delivery, render text, gradients, icons, and animation at delivery resolution from original assets; do **not** enlarge a flattened 480p overlay or call an upscaled asset native 4K. Check each element at 100% in a 4K crop and disclose any artwork whose source resolution limits it. Check the bottom edge of full-frame gradients for video bleed. Verify animation in motion, including seams, idles, and transitions.
- Use the specific thumbnail he selects. A Canva original can be the final thumbnail unchanged; never assume his face must be added. If he requests cutouts, inspect hair/background edges and ensure the subject reaches the intended frame edge. Create alternatives only when requested.

## Deliver and verify

- Keep the approved voice mix when rebuilding visuals; remux it unchanged when practical. Verify duration, dimensions, frame counts and sync, decode, audio stream/copy integrity, clipping, and representative frames at inserts and the ending. Distinguish sampled checks from watching or listening to the entire video. Verify any delivered copy and provide its absolute path.
- Render a full final only after the requested review/approval. If he asks to reclaim space, delete only the old renders he authorizes, retain the requested number (he chose three for the Caves project), and never delete raw media, project files, or the approved current cut.
- When asked for YouTube copy, use the actual final edit and supply accurate chapter timestamps; do not invent links. Recheck facts or precise quotations as appropriate. For future approved videos, update relevant shared or specialized guidance only when the user authorizes that work; follow the source repository's workflow.
