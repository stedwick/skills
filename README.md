# Phil's Skills

Agent skills I made for myself. They work in Claude Code, Codex, Cursor and other coding agents.

Install all of them:

```bash
npx skills add stedwick/skills
```

Or just one:

```bash
npx skills add stedwick/skills --skill creativity
```

Here are my skills so far.

1. "creativity" skill: A cure for beige landing pages.
2. "vlog-editor" skill: Claude does all my video editing now.
3. "functional-programming" skill: I believe functional programming works best with agents.

## "creativity" skill

You've probably noticed how bland AI design can be. This skill is my attempt to fix that.

How it works:

1. It spends 15 minutes researching what others have done before.
2. It shows you a dozen inspiration choices, and you pick your favorites.
3. It uses a random number generator to decide which parts of which inspirations to remix.
4. It does three drafts each of three separate ideas. It asks if you want to steer after the first draft.

It's a great way to brainstorm ideas with your agent!

It won't copy and paste anything. It remixes _ideas_ from your chosen references, and uses your own material, new AI-generated art, or art drawn in code.

To use it, type `/creativity` and say what you want, for example: "/creativity Give me three creative reimaginings of my website: https://example.com."

A full run can take ~1 to 2 hours.

Of course, this isn't real creativity, and it won't one-shot a production design. But it beats another beige-y, orange-y, purplish, generic AI landing page.

Here are some creative reimaginings of my site at https://phils.app

<p><img src="readme/four.jpg" alt="Four reimaginings of my portfolio site: a campfire island at night, a résumé as an ID card, a career as a trail down Mt Hood, and a Portland night footer"></p>

## "functional-programming" skill

Makes your agent write code in a functional style, in any language: small named functions, clear inputs and outputs, side effects kept separate, and fast tests.

## "vlog-editor" skill

I use these three to edit my own videos, so they're built around my setup. Fork them and change them to fit yours.

- **vlog-editor**: turns raw camera and mic recordings into a finished video: transcript, editable script, synced cuts, cleaner audio, graphics, thumbnail and 4K export.
- **review-vlog-editor**: adds structure for book, film and game reviews.
- **lets-play-editor**: adds gameplay: OBS tracks, facecam, game sound and chess puzzles.
