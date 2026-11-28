#!/usr/bin/env python3
"""Gentle DeepFilterNet noise reduction in overlapping 30 s chunks.

Why: running DeepFilterNet on a full 20+ minute 48 kHz recording in one call can stall
or run out of memory, while hard chunk boundaries click. This processes fixed chunks
with linear overlap-add crossfades and a capped attenuation limit (default 18 dB).

Usage:
  denoise_dfn.py IN.wav OUT.wav [--atten 18] [--chunk 30] [--overlap 0.5]

Needs: pip install deepfilternet soundfile torch
"""
import argparse

import numpy as np


def process_channel(m, st, enhance, torch, x, sr, atten, chunk_s, overlap_s):
    chunk = int(chunk_s * sr)
    ov = int(overlap_s * sr)
    out = np.zeros_like(x, dtype=np.float32)
    w = np.zeros_like(x, dtype=np.float32)
    i = 0
    while i < len(x):
        a = max(0, i - ov)
        b = min(len(x), i + chunk + ov)
        e = enhance(m, st, torch.from_numpy(x[a:b].copy())[None], atten_lim_db=atten)[0].numpy()[:b - a]
        win = np.ones(b - a, dtype=np.float32)
        if a > 0 and ov > 0:
            n = min(ov, len(win))
            win[:n] = np.linspace(0.0, 1.0, n, dtype=np.float32)
        if b < len(x) and ov > 0:
            n = min(ov, len(win))
            win[-n:] = np.linspace(1.0, 0.0, n, dtype=np.float32)
        out[a:b] += e * win
        w[a:b] += win
        i += chunk
    return out / np.maximum(w, 1e-6)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='input WAV (typically 48 kHz)')
    ap.add_argument('output', help='output WAV (float32)')
    ap.add_argument('--atten', type=float, default=18.0, help='max attenuation limit in dB (default 18)')
    ap.add_argument('--chunk', type=float, default=30.0, help='chunk duration in seconds (default 30)')
    ap.add_argument('--overlap', type=float, default=0.5, help='overlap-add crossfade in seconds (default 0.5)')
    ap.add_argument('--threads', type=int, default=1, help='torch CPU threads (default 1)')
    args = ap.parse_args()

    import soundfile as sf
    import torch
    from df.enhance import enhance, init_df

    torch.set_num_threads(args.threads)
    m, st, _ = init_df()
    x, sr = sf.read(args.input, dtype='float32')
    if x.ndim == 1:
        y = process_channel(m, st, enhance, torch, x, sr, args.atten, args.chunk, args.overlap)
    else:
        y = np.stack([process_channel(m, st, enhance, torch, x[:, c], sr, args.atten, args.chunk, args.overlap)
                      for c in range(x.shape[1])], axis=1)
    sf.write(args.output, y, sr, subtype='FLOAT')
    print(f'ok {args.output} ({len(x) / sr:.2f}s, {sr} Hz, atten={args.atten:g} dB)')


if __name__ == '__main__':
    main()
