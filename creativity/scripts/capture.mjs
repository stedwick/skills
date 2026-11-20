#!/usr/bin/env node
// Capture what a visitor sees of one static HTML page, with headless Chrome over CDP.
// usage: node capture.mjs <index.html | https://url> <outdir> [name=js ...]
// Always writes: desktop-fold.png (1440x900), desktop-full.png, phone-fold.png (390x844 @2x), phone-full.png
// Each extra "name=js" argument: reload, run the JS (may be async), wait 900 ms,
// then write state-<name>-desktop.png and state-<name>-phone.png (viewport only).
// Use states for scroll positions and interactions, e.g.  mid='window.scrollTo(0,1200)'
import { spawn } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir, homedir } from 'node:os';
import { join, resolve } from 'node:path';

const [file, outdir, ...stateArgs] = process.argv.slice(2);
if (!file || !outdir) { console.error('usage: capture.mjs <index.html> <outdir> [name=js ...]'); process.exit(2); }
const url = /^https?:/.test(file) ? file : 'file://' + resolve(file);
mkdirSync(outdir, { recursive: true });
const profile = mkdtempSync(join(tmpdir(), 'cap-'));
const port = 9300 + Math.floor(Math.random() * 600);
// Prefer Google's headless-only Chrome (no Dock icon on macOS); fall back to the installed Chrome.
const SHELL = join(homedir(), '.cache/chrome-headless-shell/chrome-headless-shell-mac-arm64/chrome-headless-shell');
const CHROME = process.env.CHROME_PATH || (existsSync(SHELL) ? SHELL : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, 'about:blank',
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// Never leave Chrome running: kill it on any exit, signal, or after a hard time limit.
const killChrome = () => { try { chrome.kill('SIGKILL'); } catch {} };
process.on('exit', killChrome);
for (const sig of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(sig, () => { killChrome(); process.exit(130); });
setTimeout(() => { console.error('CAPTURE TIMEOUT: stopping Chrome'); killChrome(); process.exit(1); }, 110000).unref();

async function target() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error('Chrome did not start');
}

let id = 0; const pending = new Map();
let ws;
function send(method, params = {}) {
  return new Promise((res, rej) => { const n = ++id; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, method, params })); });
}
async function shot(path, full) {
  const { data } = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: !!full });
  writeFileSync(path, Buffer.from(data, 'base64')); console.log('ok', path);
}
async function fullShot(path) {
  const { result } = await send('Runtime.evaluate', { expression: 'Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)', returnByValue: true });
  const { result: w } = await send('Runtime.evaluate', { expression: 'window.innerWidth', returnByValue: true });
  const { result: d } = await send('Runtime.evaluate', { expression: 'devicePixelRatio', returnByValue: true });
  const h = Math.min(result.value, Math.floor(12000 / d.value)); // keep the image under ~12,000 device pixels
  // Very tall pages at 2x can exceed the GPU limit (headless shell fails on them): retry at a smaller scale.
  let data;
  for (const scale of [1, 0.5, 0.25]) {
    try { ({ data } = await Promise.race([send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: w.value, height: h, scale } }),
      new Promise((_, rej) => setTimeout(() => rej(new Error('full-page shot timed out')), 25000))])); break; }
    catch (e) { if (scale === 0.25) throw e; }
  }
  writeFileSync(path, Buffer.from(data, 'base64')); console.log('ok', path, `(${h}px tall)`);
}
async function view(w, h, dpr, mobile) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
}
async function load() { await send('Page.navigate', { url }); await sleep(1800); }

try {
  ws = new WebSocket(await target());
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); const p = pending.get(d.id); if (p) { pending.delete(d.id); d.error ? p.rej(new Error(d.error.message)) : p.res(d.result); } };
  await send('Page.enable');
  const views = [['desktop', 1440, 900, 1, false], ['phone', 390, 844, 2, true]];
  for (const [name, w, h, dpr, mobile] of views) {
    await view(w, h, dpr, mobile); await load();
    await shot(join(outdir, `${name}-fold.png`));
    try { await fullShot(join(outdir, `${name}-full.png`)); } catch (e) { console.log('SKIPPED', `${name}-full.png:`, e.message); }
    for (const s of stateArgs) {
      const eq = s.indexOf('='); const sn = s.slice(0, eq); const js = s.slice(eq + 1);
      await load();
      const r = await send('Runtime.evaluate', { expression: `(async()=>{${js}})()`, awaitPromise: true });
      if (r.exceptionDetails) console.log('JS ERROR in state', sn, r.exceptionDetails.exception?.description || r.exceptionDetails.text);
      await sleep(900);
      await shot(join(outdir, `state-${sn}-${name}.png`));
    }
  }
  // console errors check
  const r = await send('Runtime.evaluate', { expression: 'document.title', returnByValue: true });
  console.log('title:', r.result.value);
} catch (e) { console.error('CAPTURE FAILED', e.message); process.exitCode = 1; }
finally { try { ws?.close(); } catch {} chrome.kill(); await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
