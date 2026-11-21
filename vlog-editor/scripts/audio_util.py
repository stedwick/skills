"""Small shared helpers: decode audio with ffmpeg and measure loudness in short windows."""
import json
import subprocess

import numpy as np


def load_audio(path, sr=16000, start=None, dur=None):
    """Decode any audio/video file to mono float32 at `sr` Hz using ffmpeg."""
    cmd = ['ffmpeg', '-nostdin', '-v', 'error']
    if start is not None:
        cmd += ['-ss', f'{start:.3f}']
    if dur is not None:
        cmd += ['-t', f'{dur:.3f}']
    cmd += ['-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def rms(x, sr, t, win=0.03):
    """Root-mean-square level of `win` seconds of audio starting at time `t`."""
    a = max(0, int(t * sr))
    seg = x[a:a + int(win * sr)]
    return float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0


def noise_floor(x, sr, win=0.03):
    """Level of the quietest 5% of short windows: the room-tone level of the recording."""
    n = len(x) // int(win * sr)
    if n == 0:
        return 0.0
    frames = x[:n * int(win * sr)].reshape(n, -1)
    return float(np.percentile(np.sqrt((frames ** 2).mean(1)), 5))


def probe(path):
    """Duration of the container and each stream, in seconds."""
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,duration',
                          '-of', 'json', path], capture_output=True, check=True).stdout
    j = json.loads(out)
    res = {'format': float(j['format'].get('duration') or 0)}
    for s in j.get('streams', []):
        if s.get('duration'):
            res[s['codec_type']] = float(s['duration'])
    return res


def speech_level(x, sr, win=0.03):
    """Typical speaking level: the 80th percentile of short-window levels."""
    n = len(x) // int(win * sr)
    if n == 0:
        return 0.0
    frames = x[:n * int(win * sr)].reshape(n, -1)
    return float(np.percentile(np.sqrt((frames ** 2).mean(1)), 80))
