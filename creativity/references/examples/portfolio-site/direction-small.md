# Direction A. Small: "One Portland Day"

- **Premise:** The same page, in the same order, but the hero's world no longer stops after the first screen: the visitor travels through one Portland day, from morning at the top to a lit-up night city in the footer, and the template parts become crafted parts of that world.
- **Keep:** the section order, the content (tightened: no repeated paragraphs), the hero art, the dark page, the overall look.
- **Change:**
  - The footer is the same scene again (their own transparent layers, re-lit with CSS to dusk and night: navy sky, warm window lights that twinkle slowly, a moon), so the page begins and ends in Portland. It is still clearly a footer: links, contact, copyright on top of the scene.
  - The light changes continuously as you scroll (page tint and accent shift from morning blue to sunset coral to night navy), never by swapping images.
  - A five-second facts strip under the name (Lead Software Engineer at Cedar Apps · 18 years · Portland · résumé · email).
  - A real sticky menu (Work, Skills, Projects, Life, Contact) that appears after the hero.
  - Template parts replaced: the stock icon chips become a tidy, typographic skill list grouped by craft; blue Bootstrap buttons and pills become buttons in the Mt Hood palette; the three career cards gain the real screenshots inside framed "windows".
  - One signature touch: Biscuit as a small pixel-art dog who appears in the Hobbies section and again in the footer; hover him and he sits on the keyboard ("onkjf ssadkl").
- **Fingerprint (mostly the original's, refined):** palette from the hero (page #0F170A kept; snow #F4F8FB; glacier sky #8ED6F4; pine #1E3B2A; morning cyan #2BB3E6; sunset coral #FF7A59; night navy #0E1A33; window gold #FFC857); type: a characterful serif for headings (Fraunces or Young Serif) in place of Georgia, Open Sans or Atkinson Hyperlegible for text; layout: the original column; image: their own layers, re-lit; motion: scroll-linked light, slow window twinkle, Biscuit's spring; interaction: menu, Biscuit.
- **Learns from:** Josh Comeau (scene header and footer with a character), localghost (one scene, changing light), Mangham (facts strip), Canvas Cycle (glints in one picture).
- **Risk:** too subtle; Biscuit must be good pixel art, not crude.
- **Spark:** none needed for "small"; uses idea 1, 3, 4.


All three directions must obey: static HTML, CSS and a little JS; assets relative (reuse `../../original/parallax/` and `../../original/legacy/`); no audio; no WebGL; nothing animates forever except slow, cheap CSS (window twinkle); reduced motion respected; all true facts kept; contact details, résumé PDF and project links work.
