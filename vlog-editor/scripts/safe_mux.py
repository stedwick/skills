#!/usr/bin/env python3
"""Put the final video and the approved audio together without losing the ending, then verify.

Why: limiting the output by video frame count (-frames:v) while copying or delaying audio
can stop the sound up to a second early and cut off the last words. This muxes by duration
(-t) instead and then checks the result.

Usage:
  safe_mux.py VIDEO AUDIO OUT [--duration SECONDS] [--copy-audio]
      VIDEO may be one file or an ffmpeg concat list (.txt with "file 'x.mp4'" lines).
      Duration defaults to the video's length.
  safe_mux.py --verify OUT [--duration SECONDS]
      Only check an existing file.

Checks: audio and video streams match the expected duration (within 2 frames), and the
file does not end while there is still sound (a cut-off last word).
Exit code 1 when a check fails.
"""
import argparse
import subprocess
import sys

from audio_util import load_audio, probe, rms, speech_level


def verify(path, expected=None, fps=30):
    d = probe(path)
    ok = True
    exp = expected or d.get('video') or d['format']
    tol = 2 / fps
    for kind in ('video', 'audio'):
        if kind not in d:
            print(f'  missing {kind} stream'); ok = False
        elif abs(d[kind] - exp) > tol:
            print(f'  {kind} lasts {d[kind]:.3f}s, expected {exp:.3f}s'); ok = False
    x = load_audio(path, 16000)
    sp = max(speech_level(x, 16000), 1e-4)
    end = len(x) / 16000
    tail = max(rms(x, 16000, end - 0.08), rms(x, 16000, end - 0.04))
    if tail > sp * 0.10:
        print(f'  sound continues to the very end ({tail / sp:.2f} of speaking level): last word may be cut off'); ok = False
    print(('OK ' if ok else 'FAIL ') + f'{path}: ' + ', '.join(f'{k} {v:.3f}s' for k, v in d.items()))
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--verify')
    ap.add_argument('--duration', type=float)
    ap.add_argument('--copy-audio', action='store_true', help='copy the audio stream instead of encoding AAC 192k')
    args = ap.parse_args()

    if args.verify:
        sys.exit(0 if verify(args.verify, args.duration) else 1)
    if len(args.paths) != 3:
        ap.error('need VIDEO AUDIO OUT')
    video, audio, out = args.paths
    vin = ['-f', 'concat', '-safe', '0', '-i', video] if video.endswith('.txt') else ['-i', video]
    dur = args.duration
    if dur is None:
        tmp = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration:format=duration',
                              '-of', 'default=nw=1:nk=1'] + ([] if not video.endswith('.txt') else ['-f', 'concat', '-safe', '0']) + [video],
                             capture_output=True, text=True).stdout.split()
        dur = max(float(v) for v in tmp if v not in ('N/A', ''))
    acodec = ['-c:a', 'copy'] if args.copy_audio else ['-c:a', 'aac', '-b:a', '192k']
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + vin + ['-i', audio, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy']
                   + acodec + ['-t', f'{dur:.3f}', '-movflags', '+faststart', out], check=True)
    sys.exit(0 if verify(out, dur) else 1)


if __name__ == '__main__':
    main()
