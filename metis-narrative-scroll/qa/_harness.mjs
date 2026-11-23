/* Shared real-time CDP harness for the narrative QA suites.
 *
 * Why real time rather than headless Chrome's --virtual-time-budget: that flag
 * does not advance CSS transitions the way wall clock does, so a page whose
 * entrances are transitions captures on its start frame and reads as totally
 * broken when it is fine. On the Build Note it reported 53 stranded-hidden
 * elements and a blank hero while every real-time check passed. It cost a full
 * diagnostic cycle. Never verify a narrative scroll with virtual time.
 *
 * Also: --window-size below 500px is silently clamped to 500 and the shot
 * cropped, which fakes a horizontal-overflow bug that does not exist. Mobile
 * widths must come from Emulation.setDeviceMetricsOverride, as they do here.
 */
import { spawn } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { tmpdir, platform } from "node:os";
import { join, resolve } from "node:path";

/* Chrome lives somewhere different on every OS, and this skill has to run on
   whatever machine a consultant is on. */
const CANDIDATES = {
  darwin: [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  ],
  win32: [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    join(process.env.LOCALAPPDATA || "", "Google\\Chrome\\Application\\chrome.exe"),
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  ],
  linux: [
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium", "/usr/bin/chromium-browser",
  ],
};

export function findChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }
  for (const p of CANDIDATES[platform()] || []) {
    if (p && existsSync(p)) return p;
  }
  throw new Error(
    "Could not find Chrome. Install Google Chrome, or set CHROME_PATH to its " +
    "executable:\n  CHROME_PATH=/path/to/chrome node qa/qa-render.mjs <file>");
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* Scratch lives in the OS temp dir, never in the project folder. Build inputs
   have been deleted before by a cleanup of a scratch folder sitting next to
   them; keeping captures outside the project makes that impossible. */
export function scratchDir(name) {
  const d = join(tmpdir(), "metis-narrative-qa", name);
  mkdirSync(d, { recursive: true });
  return d;
}

/** Boot Chrome, attach to a fresh target, and return a small driver. */
export async function open(file, port) {
  const url = "file://" + encodeURI(resolve(file));
  const chrome = spawn(findChrome(), [
    "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
    "--remote-debugging-port=" + port,
    "--user-data-dir=" + join(tmpdir(), "metis-narrative-chrome-" + port),
    "--no-first-run", "--no-default-browser-check", "about:blank",
  ], { stdio: ["ignore", "ignore", "ignore"] });

  let ws, nextId = 1, sessionId;
  const pending = new Map();

  for (let i = 0; i < 80; i++) {
    try {
      const t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      if (t.length) break;
    } catch { /* not up yet */ }
    await sleep(150);
  }
  const info = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  ws = new WebSocket(info.webSocketDebuggerUrl);
  await new Promise((r, j) => {
    ws.addEventListener("open", r);
    ws.addEventListener("error", () => j(new Error("could not attach to Chrome")));
  });
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) {
      const { res, rej } = pending.get(m.id);
      pending.delete(m.id);
      m.error ? rej(new Error(m.error.message)) : res(m.result);
    }
  });

  const send = (method, params = {}, sid) => new Promise((res, rej) => {
    const id = nextId++;
    pending.set(id, { res, rej });
    ws.send(JSON.stringify({ id, method, params, sessionId: sid }));
  });

  const { targetId } = await send("Target.createTarget", { url: "about:blank" });
  ({ sessionId } = await send("Target.attachToTarget", { targetId, flatten: true }));
  const cmd = (m, p) => send(m, p, sessionId);
  await cmd("Page.enable");
  await cmd("Runtime.enable");

  const evaluate = async (expression) => {
    const r = await cmd("Runtime.evaluate",
      { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) {
      throw new Error("page threw: " +
        (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    }
    return r.result.value;
  };

  return {
    url, cmd, evaluate,
    /** Emulate a viewport and load the page fresh. */
    async view(w, h, mobile = false) {
      await cmd("Emulation.setDeviceMetricsOverride", {
        width: w, height: h, deviceScaleFactor: 1,
        mobile, screenWidth: w, screenHeight: h,
      });
      await cmd("Page.navigate", { url });
      await sleep(2600);                 // fonts, images, first sweep
    },
    /** Walk the page so every scroll-armed entrance and counter has fired. */
    async walk(stops = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9]) {
      const H = await evaluate("document.documentElement.scrollHeight");
      for (const f of stops) {
        await evaluate(`window.scrollTo({top:${Math.round(H * f)},behavior:"instant"})`);
        await sleep(700);
      }
      await sleep(900);
    },
    async scrollTo(y) {
      await evaluate(`window.scrollTo({top:${Math.round(y)},behavior:"instant"})`);
      await sleep(900);
    },
    /** clip is in ABSOLUTE page coordinates, not viewport coordinates. */
    async shot(path, clip) {
      const p = { format: "png", captureBeyondViewport: false };
      if (clip) p.clip = { ...clip, scale: 2 };
      const r = await cmd("Page.captureScreenshot", p);
      const { writeFileSync } = await import("node:fs");
      writeFileSync(path, Buffer.from(r.data, "base64"));
      return path;
    },
    async close() {
      try { await send("Target.closeTarget", { targetId }); } catch {}
      try { ws.close(); } catch {}
      chrome.kill();
    },
  };
}

export const VIEWS = [
  { name: "desktop", w: 1440, h: 900 },
  { name: "laptop", w: 1180, h: 800 },
  { name: "mobile", w: 390, h: 844, mobile: true },
];
