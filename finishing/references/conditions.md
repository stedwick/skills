# Conditions of use and function checks

Function checks run **after** the design fixes. They check that the piece works where it will really be used. For each medium: what a capture is, the conditions to test in, and the checks. A check you cannot do in this environment goes on the open list as "cannot check here", never as passed.

## Web pages (tested)

**Capture.** Built-in browser, the agent's own tab. Widths 1440 and 390. At least one frame per section, top to bottom. Every named state: toggles and modes (dark mode, a lamp, a filter), open menus, hover states that carry meaning. Label each capture with width, state and section. For stills, turn transitions off and wait for images to load.

**Conditions.**
- Desktop (1440) and phone (390) widths.
- A visible tab for motion and frame rate (a hidden pane cannot draw frames).
- Reduced motion on.
- Keyboard only.

**Checks.**
- No horizontal scroll at 390. Nothing overlaps or is cut off.
- Every link and button goes where it says. Outside links resolve (200 or a normal redirect).
- Forms submit, or clearly say where the message goes (for example a mail link). A mock form is reported as such.
- Reduced motion gets a still version. Nothing animates forever.
- Frame rate while scrolling is about 60 frames per second (only in a visible tab).
- Image weight: report the total size and megapixels. Flag any image far larger than its shown size.
- Text contrast meets WCAG AA (4.5:1 body, 3:1 large text) in every state, including special modes.
- Keyboard focus is visible on links, buttons and form fields.
- Touch targets are at least 44 px at 390 width.
- No console errors, and no 404s in the network log.

## Story or other writing (untested)

**Capture.** The full text, and the opening, a middle passage and the ending as excerpts.
**Conditions.** Read aloud. Read on a phone screen.
**Checks.** Names, dates and places stay the same. Every set-up pays off. Nothing trips the voice when read aloud.

## Music or audio (untested)

**Capture.** The structure (sections and times) and a description of the mix.
**Conditions.** Small speakers, mono, low volume, earbuds.
**Checks.** The vocal or melody is clear on small speakers. Nothing disappears in mono. Loudness is in line with two reference tracks.

## Game level (untested)

**Capture.** Map screenshots and a short playthrough of the main route.
**Conditions.** 30 frames per second, a controller, a first-time player.
**Checks.** The route is readable without a guide. Effects never hide the player, enemies or the path. Collision matches what is drawn.
