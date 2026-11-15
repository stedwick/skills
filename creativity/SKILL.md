---
name: creativity
description: A storyboard process for creative work of any kind (visual design, web pages, game levels, stories, illustration, music, video, brands, names, product ideas). Deep research of acclaimed work first, then three very different directions developed through three judged drafts each, with the user as director at two checkpoints, ending in a storyboard of three finished concepts. Use ONLY when the user names this skill ("use the creativity skill", "/creativity", "run creativity on this"). Do not start it for an ordinary design or writing request, because a full run is long and costs nine or more builds.
---

# Creativity

You are good at making things work. Left alone, you are bad at making things that are fresh and beautiful. Your first idea is the average of everything you have seen, and your "three different ideas" are one idea in three colours. In a test of the first version of this skill, all three concepts had the same muted off-white palette, the same small mono labels and almost no imagery; the judge scored them 8 of 10 and the user scored them 0. This process exists to stop that. Read `calibration/` before you start: it holds the user's real judgments.

The five supports:

- **Giants, studied for real.** Long, wide research of the best work in the field, captured as images, text, audio or footage, not as your memory of it.
- **The user as director.** Two checkpoints: the user approves the giants, then the first drafts. Their taste steers the run early, when changes are cheap.
- **Outside randomness.** A script pushes each direction away from your default.
- **A comparative judge.** A fresh-context judge places each draft among the acclaimed examples and the known failures. It does not give friendly absolute numbers.
- **Three directions, three drafts each.** Different in idea and in form. Each draft gets bolder, not emptier.

Keep all work in `creativity-runs/<short-task-slug>/` in the working directory. A run makes hundreds of files (captures, builds, images), and they must never go into version control: if the folder is in a git repository, add `creativity-runs/` to `.gitignore` before you write anything. Use the scratchpad if the project must stay completely clean.

```
creativity-runs/<slug>/
  original/           step 0  (only when improving existing work: an untouched copy)
  brief.md            step 0
  research-log.md     step 1  (searches, sources, timestamps)
  board/              step 1  (captures of every studied example)
  research.md         step 1  (examples, rubric, clichés)
  directions.md       step 2
  a/ b/ c/            step 3  draft-1/ draft-2/ draft-3/, each with score.json
  storyboard.*        step 4
```

## Step 0: Brainstorm with the user

Ask all your questions in one round. Use the question tool if you have one. Find out:

- What is made, for whom, and what the audience must feel or do.
- What they love and what bores them, also from outside the field. Their references are additions to your research, never a replacement for it.
- Ideas they already have. Record their words exactly.
- Hard limits: what must stay, what must not appear. Do not invent extra limits. Read a limit in the way that gives the most creative room (for example, "a single HTML page" still allows images and fonts next to it).
- How bold you may be.
- Practical costs the user cares about (for a web page: CPU, memory, load time; for a game: target hardware; for print: budget).
- Whether they can join the two checkpoints. If not, you make those calls yourself, using the calibration folder and the brief.

Tell them the size of the run. Write `brief.md`.

**Improving existing work** (the user's own site, story, logo, level). Never change the original. Make a copy in `original/` (for a live site: save the pages and their assets, and serve the copy locally) and build every draft from a copy of that copy. Before step 1, study the original as closely as you study a giant: capture it, list what it is (content, voice, structure, colours, type, images) and what its owner clearly cares about. Its content and identity are hard limits unless the user says otherwise: the result must still be their work, made more creative, not a stranger's work with their name on it. Ask how much change they want; if they do not say, use the three sizes in step 2.

## Step 1: Research the giants (at least 15 minutes, before you make anything)

This step is where the quality comes from. Do not rush it and do not make anything yet: no ideas list, no sketches, no code. Run `date` at the start and write the time in `research-log.md`. Do not leave this step until at least 15 minutes have passed and the checks below are met. More time is better.

**Search wide.** You are not helpless and the user should never have to find examples for you. Use every route you have: web search, juried awards and their winner archives, curated galleries, "best of the year" and "best of all time" lists, practitioner blogs and newsletters, interviews and talks with the makers, postmortems and breakdowns, forums where practitioners argue about what is good, and the user's references. `references/media.md` lists starting sources per medium; go beyond them. Log every search and every source in `research-log.md`. If you have subagents, split the search by source family (juried awards, curated galleries and practitioner writing, neighbouring fields), one researcher each, in parallel; each writes its notes and captures to files.

**Collect, then choose.** Find at least 20 candidates. From them, choose 8 to 12 to study closely, plus 2 or 3 from neighbouring fields (a museum, a film title sequence, a board game, a record sleeve), which are often where fresh ideas come from. Prefer work that is recent and acclaimed by juries or practitioners, and work that is surprising. Study **only small, independent creators**: individuals, small studios, indie developers, personal sites, indie games, zines, self-published art, one-person projects. Never take examples from large companies, corporate brands or B2B SaaS, even when a jury awarded them: their work is made by committee, and it pulls you to the safe average. Personal work takes the risks; it is where creative ideas appear first. Avoid the obvious famous five that every model already knows; they pull you to the average.

**Study the real thing.** Open it. Take captures and save them in `board/`: for visual and interactive work, screenshots at several scroll positions and a few frames of motion; for writing, the opening and a key passage (short excerpts only); for games, map screenshots, footage frames and designer commentary; for music, the structure and what critics point at. For web pages and HTML builds, use the browser your environment already gives you (for example a built-in browser pane): each agent opens its own tab, takes screenshots at desktop and phone size and at scroll positions from top to bottom, and copies the saved screenshot files into the capture folder. Do not launch extra browsers (a separate Chrome, a browser-automation CLI) that the user sees appear on their computer. Only if no browser tool exists, `node scripts/capture.mjs <url-or-file> <outdir> name='js'...` takes the same screenshots with headless Chrome (it may need to run outside a command sandbox; it always closes Chrome). The images matter more than your notes: a builder or judge who reads "bold use of colour" learns nothing, but one who sees the capture does.

**Think.** For each example, answer: what is the one thing it does that others do not? How is it built? What does it feel like in the first five seconds? What would it look like if a machine had made it badly, and why does it not look like that?

**Write `research.md`.** It is the judge's and the builders' knowledge of quality, so write it for a reader with no other context.

1. **Examples.** For each: name, link, the capture files, why it is praised (cite the jury or critic), how it is built, how it looks, sounds or reads, how it behaves, and its one unique move. Be concrete.
2. **Rubric.** Six to nine principles shared by the great examples, each with a description of a 3, a 6 and a 9. The rubric must cover the **sensory craft** of the medium, not only the idea and the words. `references/media.md` lists the craft areas per medium (for visual work: colour, typography, imagery, composition, motion, interaction; for writing: voice, imagery, rhythm, structure). Include one principle for **impact**: does it stop the audience, would they show it to a friend? And one for **coherence**: do all the parts serve one idea? Give principles as transferable qualities, so a draft can meet them without copying.
3. **Clichés and machine tells.** The look of the average, forgettable version, and the signs of machine-made work in this medium. Start from the list in `references/media.md` and from `calibration/`.

**Look at every capture before you use it.** Remove or redo blank, error or loading-screen captures (WebGL sites often capture black); a judge given a blank capture wastes effort ranking it.

**Checks before you leave step 1:** at least 15 minutes since the start time; at least 20 candidates and 8 studied examples in the log; captures in `board/` for each studied example; the rubric covers sensory craft and impact.

### Checkpoint 1: the user approves the giants

Show the user the board: the studied examples as a contact sheet of captures with one line each (name, why it is here) and a clickable link to the live work. Also list the links in your chat message, numbered, so the user can open each one and answer by number. Ask a plain question ("Which numbers do you not like? Any other site you love?"). Give it in the most direct way your environment has (a page you publish or open, inline images). Ask them to strike what they dislike and to add anything they love. Update `research.md` from their answer. If they cannot join, continue.

## Step 2: Three directions

1. Run `python3 scripts/spark.py` (in this skill's folder) three times, one per direction. Each run prints a seed, a lens, a far domain and a form constraint. Do not show the seed in the work.
2. Write at least 15 one-line ideas. Go broad. Include ideas that seem wrong, and the user's own ideas.
3. Choose three that differ in **premise**: describe each in one sentence without colours, fonts or mood words; if two sentences are similar, replace one.
4. Then give each direction a **form fingerprint** that differs from the other two in every row. For visual work: palette (name the actual colours), type family, layout system, image method (photography, generated image, 3D, illustration style, pure type, data), motion. For writing: point of view, tense, form, voice, length of sentences. For games: core mechanic, space, pacing, camera. The fingerprint rows for each medium are in `references/media.md`. No fingerprint may be the machine default listed in `calibration/` (muted off-white or charcoal page, small mono labels, condensed headings, no images).
5. Usually one direction is the closest to what the user asked, done very well, and two take more risk. All three obey the hard limits.
6. **For existing work, the three directions are three sizes of change.** Small: keep the structure and the look, and add one or two creative moves that make it memorable (a signature interaction, a header and footer with character, a real illustration). Medium: keep the content and the identity, and redesign the look and the journey around one idea. Large: keep only the content and the owner's voice, and rethink the whole form. Each size still needs its own premise and its own spark; "large" is not "medium with more", and "small" is not a colour change. The fingerprint rule applies to medium and large; small may keep the original's fingerprint in most rows.

Write `directions.md`: name, premise, fingerprint, the research examples it learns from, what it risks, and its spark.

## Step 3: Three drafts of each direction

Run the three directions in parallel if you have subagents: one builder per direction, started from the top-level session (not nested), with `brief.md`, `research.md`, the `board/` captures, `calibration/`, its own direction only, and this step. A builder that sees the other directions drifts toward them.

**Every draft is a real build** that a person can open, play, read or hear. Use real material at the quality of the giants: real or generated photography and illustration (use an image-generation tool if you have one; test once before step 3 that it gives full-size files you can save, because some tools return only small previews, and tell each builder what works; with Canva, placing the generated image in a design and exporting the design gives the full size, but it saves designs in the user's account, so ask the user in step 0 before any builder does it), real fonts, real sound. Do not hand-draw pictures in code unless crude drawing is the concept; the calibration shows what happens.

**Craft rules from the user's judgments** (see the middle of `calibration/`):

- **The journey develops.** A strong first screen is not enough. Something new must happen as the audience goes on: a change of scale, a new event, a new rhythm, a payoff at the end. The same scene from top to bottom is monotonous, however good it looks.
- **Parts join.** Sections flow into one another (a shared horizon, an overlap, a transition, one continuous scene). Never stack separate pictures with different light or style and cut hard between them.
- **Show change inside one scene.** To show time, weather or state, change the light, colour and a few parts of one scene. Do not swap in a different generated image; the images never match and it looks bad.
- **Conventions still work.** A menu is a real menu that takes you somewhere, a footer looks like a footer, a button looks like a button. Be creative inside them, not instead of them.
- **One art direction, everywhere.** Pick one idea and make every part serve it: colours, type, images, textures, motion, even the shape of section edges (ardia.dev: a painted landscape from morning to night, with brush-shaped edges and warm paper). Coherence is what makes a page memorable.
- **Texture.** Paper, grain, paint, print or pixels, so it does not look like flat software panels.
- **Clear type hierarchy.** One big, bold headline voice and one smaller supporting voice, both scaled to the screen.
- **Put the real thing inside the art.** Real screenshots, real work and real numbers sit on or in the artwork, not in grey boxes beside it.
- **Short copy, room to breathe,** on a page that is still full of things to see.
- **Light by construction.** Static files; heavy parts (a canvas, a large image) show a matching still image first; reduced motion gets the still; prepare image crops for phone and wide screens.

For each draft:

1. **Build** it into `draft-N/`.
2. **Capture** it as a person experiences it: screenshots at desktop and phone size and at several scroll positions, frames of motion, the text, a playthrough. In a hidden or background browser tab, animation frames and CSS transitions may stall: turn transitions off for the shots (and say so in the captions), wait for images to paint, and close your tab when the draft is done, because browser panes have a tab limit. Measure frame rate only in a visible tab.
3. **Look at your own capture** next to two board captures. If it is plainly worse, or it looks like a calibration failure, fix it before scoring.
4. **Score** it with a fresh judge (see below). Save the reply as `draft-N/score.json`.
5. **Revise** from the score.

What each draft is for:

- **Draft 1, rough.** The whole idea, committed fully, with real material. A timid first draft cannot be rescued.
- **Draft 2, deepen.** Fix the judge's largest gaps, and add one new strong thing at the same time. Before you change anything, write down the draft's strongest thing (from the judge) and keep it untouched. In run 2, drafts that only fixed gaps scored a little lower than draft 1, because fixing made them safer; drafts that also added something scored higher. If freshness is low, change the idea, not the paint.
- **Draft 3, amplify.** Find the strongest thing in the draft and push it further: more vivid, more surprising, more crafted. Cut only what is noise or a cliché. Do not "refine" by removing content; emptiness is not restraint.

**The judge.** A subagent in a fresh context, given exactly: `agents/scorer.md`, `research.md`, the `board/` captures, `calibration/`, and the draft's capture. Nothing else: not the builder's notes, not the draft number, not earlier scores, not the target. Use the strongest model you can for it and the same prompt every time.

**Keep the best.** A direction's final is its highest-scoring draft, not always draft 3.

### Checkpoint 2: the user reviews the first drafts

After all three draft 1s are scored, show the user the three side by side with one line each, and open each live build where the user can click through it (for web builds, serve the folder with a small local web server, because a browser opened on a local file may not load the images). Ask: keep, redirect, or kill each one. Replace a killed direction now (back to the ideas list or a new spark), before more builds are spent. If they cannot join, continue.

**After draft 3.** If the best draft scores 8 or more, the direction is done. If it is below 6.5, replace the direction once with a new premise of the same kind and run it again; present the better of the two, with the other linked. Between 6.5 and 8, keep the direction and present it with its true score and its gaps. (In run 3, all three replacements of directions scoring 6.4 to 7.1 finished lower than the originals, and they cost an hour; a new premise starts again from about 6.) Never raise a score by arguing with the judge or re-scoring until it changes. An honest 6 is more useful than a false 8.

Before you present, put the three finals side by side. If two share a look or an idea, say so plainly.

## Step 4: Present the storyboard

One page (or document) with the three finals side by side, given to the user in the most direct way your environment has. Label them A, B, C (or 1, 2, 3, or small, medium, large) in the order they appear on the page, with the name printed on each card, and give a working link to each live build: the user will refer to them by position. For each:

- Name and one-sentence premise.
- The thing itself: captures, and how to open the full build.
- Score, its parts, and the path from draft 1 to the final.
- **What is good**, **what is weak** (include anything not verified), and **where it could go next** (two or three directions).

Then your recommendation in one or two sentences, and what was replaced or killed. Ask the user to score each final themselves, and add their scores and words to `calibration/` (small copies of the captures, the score, their words, the lesson) so the next run is calibrated better. If their words do not match the label they used, check the captures and say which one you think they meant.
