#!/usr/bin/env python3
"""Make board/contact-sheet.html: one self-contained page of thumbnails (images embedded), one per capture folder.
usage: python3 contact_sheet.py <board-dir>. Uses macOS sips; outside a sandbox it may need a writable system temp."""
import base64, glob, os, subprocess, sys
board = sys.argv[1]; tmp = os.environ.get("TMPDIR", "/tmp")
figs = []
for d in sorted(p for p in os.listdir(board) if os.path.isdir(os.path.join(board, p))):
    c = [os.path.join(board, d, "desktop-fold.png")] + sorted(glob.glob(os.path.join(board, d, "*.jpg")) + glob.glob(os.path.join(board, d, "*.png")) + glob.glob(os.path.join(board, d, "*.webp")))
    c = [x for x in c if os.path.exists(x)]
    if not c: continue
    out = os.path.join(tmp, d + ".jpg")
    r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "60", "-Z", "720", c[0], "--out", out], capture_output=True, text=True)
    if not os.path.exists(out): print("fail", d, r.stderr[:200]); continue
    b = base64.b64encode(open(out, "rb").read()).decode()
    figs.append(f'<figure><img src="data:image/jpeg;base64,{b}"><figcaption>{d}</figcaption></figure>')
html = ('<!doctype html><meta charset=utf-8><title>Reference board</title><style>body{margin:0;padding:16px;background:#111;color:#eee;font:14px system-ui}'
        'main{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}figure{margin:0}img{width:100%;border-radius:6px;display:block}figcaption{padding:6px 0}</style>'
        f'<h1>Reference board ({len(figs)} captures)</h1><main>' + "".join(figs) + "</main>")
open(os.path.join(board, "contact-sheet.html"), "w").write(html); print(len(figs), "figures")
