#!/usr/bin/env python3
"""Print outside randomness for one creative direction: a seed, a lens, a far domain.

A model cannot produce real randomness by itself. Run this once per direction
and let the three lines push the idea away from the default.
"""
import secrets
import string

LENSES = [
    "Take away the element everyone expects to be there.",
    "Make the smallest thing the largest thing.",
    "Design it for one specific person, not an audience.",
    "It has only one screen, one room, or one sentence to work with.",
    "Tell it backwards: start with the ending.",
    "Make it feel hand-made by a person with a strong opinion.",
    "It is a place you walk through, not a thing you look at.",
    "Use one material only, and use it to its limit.",
    "The audience must do something before they get anything.",
    "Treat it as a game with a rule the audience finds by accident.",
    "Make it quiet. Almost nothing moves, so one thing can.",
    "Make it loud. Maximum density, strict order.",
    "It was made 60 years ago with the tools of that time.",
    "It was made 60 years from now and found today.",
    "Swap the roles: the background is the subject.",
    "Everything is a single continuous line, shot, or thread.",
    "Explain it to a child, then keep the child's version.",
    "It has a secret that only a second visit shows.",
    "Borrow the structure of a ritual or ceremony.",
    "Make the constraint the main feature.",
    "Start from a physical object you can hold.",
    "It changes with time of day, weather, or the visitor.",
    "Use humour where the field is always serious (or the reverse).",
    "Build it around one number, one word, or one sound.",
]

DOMAINS = [
    "a night train timetable", "a botanical field guide", "a lighthouse log book",
    "brutalist architecture", "a jazz lead sheet", "a deep-sea survey chart",
    "a street food market", "a watchmaker's bench", "a 1970s science textbook",
    "a mountain rescue hut", "woodblock printing", "a chess endgame study",
    "a railway signal box", "a theatre stage plan", "a seed catalogue",
    "an observatory at 3 a.m.", "a letterpress type case", "a tide table",
    "a pinball machine", "a museum of small things", "a weather station",
    "a cartographer's draft", "a puppet workshop", "a ship's flag code",
    "origami crease patterns", "a hotel front desk at midnight",
    "a radio drama script", "a quilt pattern", "a climbing route topo",
    "a perfumer's notebook",
]


FORMS = [
    "Saturated colour: at least one colour at full strength covers much of the work.",
    "Real photography or generated photographic images carry the work.",
    "One extreme of scale: something enormous next to something tiny.",
    "The audience can touch, drag, play or change something.",
    "Texture and material: grain, paper, paint, metal, cloth, light.",
    "Pure typography as image, with a typeface that has character.",
    "A strict system (grid, rule, rhyme, loop) broken once on purpose.",
    "Dense with real information, beautifully ordered.",
    "Night, darkness or contrast as the main material.",
    "Humour leads.",
    "Motion or time is the main material.",
    "Collage: pieces from different worlds put together.",
]


def main() -> None:
    alphabet = string.ascii_letters + string.digits
    seed = "".join(secrets.choice(alphabet) for _ in range(48))
    print(f"seed:   {seed}")
    print(f"lens:   {secrets.choice(LENSES)}")
    print(f"domain: {secrets.choice(DOMAINS)}")
    print(f"form:   {secrets.choice(FORMS)}")
    print("Use these as a push, not a theme. Do not show the seed in the work.")


if __name__ == "__main__":
    main()
