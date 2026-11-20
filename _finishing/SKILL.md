---
name: finishing
description: Finish the last 20% of a strong creative draft in any medium (web page, illustration, story, game level, music, video, brand). A panel of seven specialist design editors finds where the draft goes too far or falls short (the concept is overused, details do not line up, the art looks cheap, parts have no meaning, dead space, effects that hurt readability, lost specific detail). A referee merges their findings into one short list, the user approves it once, a builder fixes it in about an hour per piece, function checks run under real conditions, and a blind judge compares before and after. Use when the user asks to finish, polish, tighten, refine or "do the last 20%" of a draft, including the finals of the creativity skill.
metadata:
  internal: true
---

# Finishing

The first 80% of creative work is easy. The last 20% is many small decisions, and most drafts fail there by going too far: the concept is on everything, the art is cheap in places, details do not line up, and effects hurt reading. The user's rule: "The best designs are ones with constraints." The goal of this skill is a piece that is cohesive, restrained and readable, and still creative. It is not a bug hunt. Design editing comes first; function checks come second.

Read `calibration/README.md` before you start. It holds the user's own examples of the faults this skill exists to find.

The supports:

- **Seven specialist editors.** Each one looks for one kind of fault only, so no kind is missed.
- **A referee.** It merges, ranks and caps the findings, and settles conflicts between editors.
- **The user approves once.** One page, all pieces, before any fix.
- **An hour per piece.** A fix that does not fit is not started.
- **A blind judge and a protected-details checker.** They decide which fixes stay.

## The run folder

Keep all work in `finishing-runs/<short-slug>/` in the working directory. Runs make many captures and copies, and they must never go into version control: if the folder is in a git repository, add `finishing-runs/` to `.gitignore` before you write anything.

```
finishing-runs/<slug>/
  original/            copies of shared folders the drafts link to
  input/<piece>/       untouched copy of each draft
  work/<piece>/        the copy the builder edits
  patches/<piece>/     one diff per fix group
  protected.md
  shots/<piece>/before/  shots/<piece>/after/
  findings/<piece>/<kind>.json
  list.json  approval.html
  verdicts/<piece>.json
  handover.html
```

## Rules for the whole run

- **Never change the original** or the live work. Work only on copies.
- **Use the browser your environment gives you** (for example a built-in browser pane), one tab per agent, and close your tab when you are done. Do not launch extra browsers. Serve web pieces with a small local server; use portless if the project uses it.
- **Light work:** no audio, no heavy background processes.
- **Talk to the user in short, plain bullets.** Simple English, no jargon, no file dumps.

## Step 1: Copy and name the pieces

1. The user names the drafts to finish. Give each a short letter (A, B, C) in the order they named them. If the drafts come from a `creativity` run, the finals are named on its storyboard; use those folders.
2. Copy each draft into `input/<piece>/` and `work/<piece>/`.
3. **Copy what the drafts link to.** Search each draft for relative links (`../`, `../../`). Copy each shared folder to the same relative position under `finishing-runs/<slug>/`, so that every link still works and no draft needs an edit. Serve `finishing-runs/<slug>/` as the web root.
4. Open each copy and check: no broken images, no missing files, and it looks like the draft the user scored. Fix the copy step until it does.
5. Note the **graft sources**: the other drafts and the replaced directions in the same run. Work that does not come from `creativity` has no graft sources unless the user names some; say so.

## Step 2: Capture the before state

Capture each piece as a person experiences it, under the same conditions you will use again after the fixes:

- For web: widths 1440 and 390, the same scroll positions (at least one frame per section), the same theme.
- **Every named state:** each toggle or mode (for example a UV lamp, dark mode), open menus, hover states that carry meaning. Label each capture with its state.
- In a hidden or background tab, animations and transitions can stall. Turn transitions off for still captures, wait for images to load, and say so in the labels.
- For other media, see `references/conditions.md` for what a capture is (a passage, a playthrough, a mix on small speakers).

Save the captures to `shots/<piece>/before/`. Look at each one. Redo blank or broken captures.

## Step 3: Write the protected list

Write `protected.md`: the details this piece must keep. Take them from:

- the user's own praise (scores, words, calibration);
- the draft's strongest thing, if a judge named one;
- details the user loved in other drafts that will be grafted in later.

Mark each one **keep** or **keep but improve**. "Keep but improve" is for a detail the user loves that is also faulty (for example a UV lamp that hurts readability, or a dog icon that looks goofy). A fix may make it better. A fix may not remove it or make it weaker.

## Step 4: The editor panel

Start seven editors in parallel, each a fresh agent, one for each fault kind in `references/fault-kinds.md`:

1. Concept overused
2. Details do not line up
3. Cheap art
4. Parts with no meaning
5. Dead space and poor balance
6. Effect over readability
7. Lost specifics

Give each editor exactly: `agents/editor.md`, its one section of `references/fault-kinds.md`, `calibration/README.md`, the piece's captures (all states) and text, and `protected.md`. Nothing else: not the other editors' findings, not your notes.

Each editor writes `findings/<piece>/<kind>.json`. With several pieces, one editor per kind may review all of them, one piece at a time, writing one file per piece: seven agents in all, not seven per piece. Zero findings is a valid reply. If an editor fails, run it once more; if it fails again, continue and say which kind is missing.

## Step 5: The referee and the approval page

Start one fresh agent with `agents/referee.md`, all the findings for all pieces, `protected.md`, the graft sources and the calibration. The referee:

- merges duplicates and groups related findings into one **fix group**;
- settles conflicts between editors, with one line of reason (restraint wins ties);
- labels any fix group that removes or calms a distinctive concept element as **calms the concept**;
- ranks by visible impact, then cost, and cuts each piece at about **45 minutes** of estimated work, leaving time for checks;
- puts items below the cut on the list as "next time", and items too big for the hour on the open list with a next step;
- offers at most three grafts per piece, each with a note on how to re-make it in this piece's own art direction.

It writes `list.json`. Then make `approval.html` from `assets/approval-template.html`. Open it in the browser and check it has no broken images.

If the editors or the referee failed for one piece, show that piece as "not ready" with the reason. The other pieces can still be approved.

### The one approval

Give the user the link to the approval page and a very short summary in chat (number of fixes per piece, and the top fix for each). Ask them to reply with item numbers, for example:

- `ok all`
- `ok A1 A2; drop B3; edit C2: keep the stamp border`

Then echo what you understood, per piece: approved, removed, edited (with their words). **Items the user did not mention count as removed.** If an edit makes an item bigger, re-size it and say which items now drop below the cut. Start only after one confirming word. That word is part of the same approval, not a second one. A plain "ok all" leaves nothing to misread: start at once, with no echo.

## Step 6: Fix

One builder per piece. Pieces can run in parallel. The builder:

1. Fixes only the approved items, one fix group at a time, in rank order.
2. Before each group, records its change as a unified diff in `patches/<piece>/<group>.diff` (use `diff -ru` on a copy of the state before the group). This lets one group be undone later without touching the others.
3. Keeps each fix small. Grafts are re-made in this piece's art direction, never pasted.
4. Stops at **about one hour** of work per piece. A group not finished is reverted with its patch and goes to the open list.
5. Never removes or weakens a protected detail.

## Step 7: Function checks

After the design fixes, run the function checks for the medium in `references/conditions.md`. For web: widths, a visible tab for motion and frame rate, links, forms, reduced motion, nothing that animates forever, image weight, contrast in every state, keyboard focus, touch targets. Fix what is small. Put the rest on the open list. A check you cannot do here (for example on a real phone) goes on the open list as "cannot check here", never as passed.

## Step 8: Judge and undo

Capture the after state exactly as in step 2, into `shots/<piece>/after/`.

**The blind judge.** For each fix group, crop the same area before and after. Give a fresh agent `agents/blind-judge.md` and the pair, labelled X and Y in random order, with no file names, notes or list. Then run it again with the order swapped. After all groups, judge the whole piece once the same way (both orders).

- If the judge prefers before in **both** orders, undo that fix group.
- If the two orders disagree, keep the fix and mark it **judge unsure**. Expect this often: judges show a strong position bias, which is why both orders are needed.
- If one group's pairs disagree with each other (one part wins in both orders, another loses in both), undo only the losing part when it can be separated; otherwise keep the group and put the losing part on the open list for the user.
- Otherwise keep it.

Use one fixed format for the secret key that maps pairs to groups, so the tally is simple: `{"p1": {"group": "A1", "capture": "<file>", "after_in_order1": "X", "after_in_order2": "Y"}}`. Give each judge only its order folder.

**The protected checker.** Give a separate fresh agent `agents/protect-check.md`, `protected.md` and the before/after crops. If it marks a protected detail **weaker** or **gone**, undo the fix group that caused it.

**Undo.** Reverse the group's patch with `patch -R`. If the reverse does not apply cleanly, also reverse the later groups that touch the same file, re-apply them, and note this on the open list. After any undo, capture again and judge the whole piece once more, so the user never gets a state no judge saw.

Save the verdicts to `verdicts/<piece>.json`. Never re-run a judge to change its answer.

## Step 9: Hand over

Make `handover.html` from `assets/handover-template.html`. Per piece:

1. The link to the finished piece and a one-line verdict.
2. A ledger keyed to the approval numbers: kept, kept but judge unsure, undone (with the plain reason and its before/after crop), or not done.
3. The open list, sorted: approved but not done, then judge unsure, then cannot check here, then next time. Each item has a severity and a reason.
4. Three to six before/after pairs, in the approved list's order.

Open it in the browser and check it. Before you hand over, prove the originals are unchanged by comparing each one with its untouched copy (`diff -rq <original> input/<piece>`). Give the user the link and two or three lines in chat.

## Step 10: Learn

Ask the user to score each finished piece and to say what is still wrong. Add their scores and words to `calibration/README.md`, with small copies of the before and after captures. If they name a fault no editor found, add it as an example under its kind in `references/fault-kinds.md`.
