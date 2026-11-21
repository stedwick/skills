#!/usr/bin/env python3
"""Check every edit join in a rendered cut for speech that is cut off.

A clean join sits in a pause: the audio just before the join (the end of the outgoing
clip) should be far below speaking level, and the incoming clip should not start in the
middle of a loud word. Run it on the voice-only mix: music under the voice hides pauses.
This script measures the RENDERED audio, so it also catches problems added by filters,
encoding, or muxing. It cannot hear; treat a pass as evidence, not proof.

Usage:
  check_joins.py RENDERED.mp4 --joins 12.4 30.1 ...          # join times in seconds
  check_joins.py RENDERED.mp4 --edl edl.json [--fps 30]      # pieces with an "out" frame and "n" frames

EDL format: {"pieces": [{"out": 0, "n": 120}, ...]} or {"edl": [...]}; each piece after
the first starts at a join. Pieces with "seg": "title" (or other inserted cards) are
fine to include: a join next to silence simply passes.

Exit code 1 when any join or the ending is flagged.
"""
import argparse
import json
import sys

from audio_util import load_audio, rms, speech_level

SR = 16000


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('media')
    ap.add_argument('--joins', type=float, nargs='*', default=[])
    ap.add_argument('--edl')
    ap.add_argument('--fps', type=float, default=30)
    ap.add_argument('--before', type=float, default=0.10,
                    help='flag when the outgoing tail is above this fraction of speaking level (default 0.10)')
    ap.add_argument('--after', type=float, default=0.5,
                    help='flag when the incoming head is above this fraction of speaking level (default 0.5)')
    args = ap.parse_args()

    joins = list(args.joins)
    if args.edl:
        j = json.load(open(args.edl))
        pieces = j.get('pieces') or j.get('edl') or []
        joins += [p['out'] / args.fps for p in pieces[1:]]
    x = load_audio(args.media, SR)
    dur = len(x) / SR
    sp = max(speech_level(x, SR), 1e-4)
    print(f'audio {dur:.2f}s, speaking level {sp:.4f}')

    bad = 0
    for t in sorted(joins):
        before = max(rms(x, SR, t - 0.06), rms(x, SR, t - 0.03))   # tail of the outgoing clip
        after = max(rms(x, SR, t), rms(x, SR, t + 0.02))           # head of the incoming clip
        issues = []
        if before > sp * args.before:
            issues.append('outgoing clip still has sound (word or breath cut off?)')
        if after > sp * args.after:
            issues.append('incoming clip starts loud (word start clipped?)')
        if issues:
            bad += 1
            m, s = divmod(t, 60)
            print(f'  {int(m)}:{s:05.2f}  tail {before / sp:4.2f}  head {after / sp:4.2f} of speaking level  ' + '; '.join(issues))

    tail = max(rms(x, SR, dur - 0.08), rms(x, SR, dur - 0.04))
    if tail > sp * args.before:
        bad += 1
        print(f'  END    sound continues to the last frame ({tail / sp:.2f} of speaking level): the ending may be cut off')

    print(f'{len(joins)} joins checked, {bad} flagged')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
