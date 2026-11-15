# Direction B. Medium: "Timberline Trail"

- **Premise:** The page is a trail map down the side of Mt Hood: one continuous trail line connects every section, so the career reads as a hike from the 2007 trailhead to today's summit, with the side projects as viewpoints and the hobbies as wildlife.
- **Keep:** all content and facts, their name, Portland and Mt Hood, the hero art (as the top of the map).
- **Change:** the look and the journey around one idea.
  - A deep forest-green topographic map runs the whole page (SVG contour lines, crafted, subtle); one bright orange trail line winds down it and draws itself as you scroll; a small hiker marker shows where you are.
  - Section headings are routed wooden Forest Service signs (brown wood, carved yellow letters), each with a distance or elevation ("Mile 18 · Cedar Apps").
  - Jobs are campsites along the trail, with real screenshots pinned like trail photos; education is the trailhead; the 11 side projects are viewpoints with a small marker each; hobbies are a "wildlife you may meet" field card (Biscuit: "Canis familiaris, very good").
  - A real menu that is the trail itself: a slim elevation profile at the top that marks each section and scrolls you there.
  - The footer is the trail's end: a ranger-station sign with contact details, the résumé PDF, and a real footer row of links.
- **Fingerprint:** palette forest #133A28 and #1C4D35 (map), contour lines #2E6B4A, glacier white #EAF6FB, trail orange #FF5B1F, sign wood #6B4426 with carved yellow #F2C14E, sky #7FD0F2 at the top; type: a heavy slab for signs (Alfa Slab One or Zilla Slab Bold), Atkinson Hyperlegible for text (a nod to accessibility); layout: one long winding path with sections alternating left and right of the trail; image: topo SVG, their mountain layer at the top, real screenshots; motion: the trail draws with scroll, the hiker moves, signs swing slightly on hover; interaction: the elevation-profile menu, tap a viewpoint to open it.
- **Learns from:** ardia (one landscape art direction, brush edges), Fifty-Nine Parks (park graphic tradition, brightest colour for titles), Brittany Chiang (a menu that is also position), taylor.fyi (the résumé as a place).
- **Risk:** the metaphor could feel forced; the map must stay readable and the facts fast.
- **Spark:** 1 (smallest thing largest: the tiny hiker marker carries the journey; signs as typography with character).


All three directions must obey: static HTML, CSS and a little JS; assets relative (reuse `../../original/parallax/` and `../../original/legacy/`); no audio; no WebGL; nothing animates forever except slow, cheap CSS (window twinkle); reduced motion respected; all true facts kept; contact details, résumé PDF and project links work.
