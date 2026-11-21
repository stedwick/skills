#!/usr/bin/env python3
"""Find stutters and restarts that a clean transcript hides.

Some speech-to-text models (Parakeet, for example) tidy up speech, so "I didn't even
install the, I didn't even install the desktop app" can come back as one clean sentence.
This runs a second, word-for-word pass with Whisper, prompted to keep disfluencies, over
the parts you plan to keep, and lists phrases that repeat within a few seconds.

Usage:
  find_flubs.py SOURCE_AUDIO --ranges 14.6:18.0 37.4:40.7 ...
  find_flubs.py SOURCE_AUDIO --edl edl.json [--fps 30]   # pieces with source "start" and "n" frames

Times are in the SOURCE recording. Needs: pip install faster-whisper (downloads a model once).
Review every hit by ear or waveform; repeated words can be intentional.
"""
import argparse
import json
import re

from audio_util import load_audio

PROMPT = 'Um, uh, so, I I I mean, the the, like, you know.'
COMMON = {'the', 'a', 'and', 'it', 'is', 'you', 'to', 'i', 'of', 'that', 'this', 'so', 'its', 'in'}


def norm(w):
    return re.sub(r"[^a-z0-9']", '', w.lower())


def repeats(words, window=6.0):
    """Yield (t1, t2, context) for n-grams (4..1 words) that repeat within `window` seconds."""
    spans = []   # word-index spans already reported, so one flub is listed once
    for n in range(4, 0, -1):
        for i in range(len(words) - n):
            for j in range(i + n, min(len(words) - n + 1, i + n + 8)):
                a = [w[0] for w in words[i:i + n]]
                if not all(a) or a != [w[0] for w in words[j:j + n]] or words[j][1] - words[i][1] > window:
                    continue
                if n == 1 and (a[0] not in COMMON or j != i + 1):
                    continue   # single words: only immediate repeats of filler words ("the the")
                if any(s <= i < e for s, e in spans):
                    continue
                spans.append((i, j + n))
                yield words[i][1], words[j][1], ' '.join(w[2] for w in words[max(0, i - 3):j + n + 2])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source')
    ap.add_argument('--ranges', nargs='*', default=[])
    ap.add_argument('--edl')
    ap.add_argument('--fps', type=float, default=30)
    ap.add_argument('--model', default='small.en')
    args = ap.parse_args()

    ranges = [tuple(map(float, r.split(':'))) for r in args.ranges]
    if args.edl:
        j = json.load(open(args.edl))
        for p in j.get('pieces') or j.get('edl') or []:
            if p.get('seg', 'main') == 'main' and 'start' in p:
                ranges.append((p['start'] / args.fps, (p['start'] + p['n']) / args.fps))

    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, compute_type='int8')
    total = 0
    for a, b in ranges:
        x = load_audio(args.source, 16000, start=a, dur=b - a)
        segs, _ = model.transcribe(x, word_timestamps=True, initial_prompt=PROMPT, vad_filter=False)
        words = [(norm(w.word), w.start + a, w.word.strip()) for s in segs for w in s.words]
        for t1, t2, ctx in repeats(words):
            total += 1
            print(f'{a:8.2f}-{b:<8.2f} repeat at {t1:.2f} -> {t2:.2f} | {ctx}')
    print(f'{len(ranges)} ranges checked, {total} possible flubs')


if __name__ == '__main__':
    main()
