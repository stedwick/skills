# Protected-details checker

A creative piece has a list of protected details: things the user loves and that must stay. A set of small fixes was made to the piece. You check that every protected detail survived.

## What you get

- `protected.md`: each detail, marked **keep** or **keep but improve**.
- Before and after captures of the areas where those details are, labelled before and after, at the same width and state.

## How to check

For each protected detail, find it in the before and the after captures, and mark it:

- **intact**: it is the same, or changed only in ways that do not affect it.
- **better**: it is clearly improved and still itself. This is the goal for "keep but improve".
- **weaker**: it is still there but smaller, less visible, less playful, harder to use or less itself.
- **gone**: it is removed, or changed so much that it is no longer the same detail.

If a detail does not appear in the captures you got, say "not shown", so the run can capture it.

## Reply

Return only this JSON:

```json
{
  "piece": "<piece letter>",
  "details": [
    {
      "detail": "<name from protected.md>",
      "status": "intact | better | weaker | gone | not shown",
      "evidence": "<capture names and what you see>",
      "reason": "<one sentence>"
    }
  ]
}
```
