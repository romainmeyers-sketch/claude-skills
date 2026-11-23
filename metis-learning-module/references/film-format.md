# The film format

A film is one self-contained HTML file. Sixty to seventy seconds, sixteen by
nine, narrated, captioned, with a transport bar. It opens on its own and it
embeds in the course hub with `?embed=1`.

These films are drawn explanations of ideas. They are not screen recordings.
A screen recording of a working tool is `metis-demo-video`.

---

## The spine

Everything in a film comes from one array.

```js
const SCENES = [
  { name:"The network",
    d:   5,                       // seconds this scene holds
    vo:  "Every day, the network connects customers and communities.",
    upd: (p, t) => { ... },       // p is 0..1 within the scene, t is absolute
    ov:  (p) => { ... } },        // optional DOM or canvas overlay
];
```

The engine computes `t0` for each scene by accumulating `d`, derives the
total length, and derives the captions. You write scenes. You never write a
timeline.

### Two narrated lines in one scene

When a scene needs two lines, split the caption rather than splitting the
scene:

```js
{ name:"Handoffs", d:9,
  vo1:"In a project model, teams form around the work.",
  vo2:"Every handoff adds time, and feedback comes late.",
  vo2At:4.5 }                      // seconds into the scene
```

### Captions

Derived, never hand-written:

```js
const CUES = [];
SCENES.forEach(s => {
  if (s.vo2){ CUES.push({t:s.t0+0.1, text:s.vo1}, {t:s.t0+s.vo2At, text:s.vo2}); }
  else       { CUES.push({t:s.t0+0.1, text:s.vo}); }
});
```

This is why the narration lines live on the scene. One source, so the
caption and the voice can never drift apart.

---

## Writing the narration

The `vo` lines **are** the script. Write them first, before any animation.
If the lines do not explain the idea on their own, no amount of motion will
save the film.

Rules that hold:

- **One claim per scene.** If a line has an "and" joining two ideas, it is
  two scenes.
- **Five to nine seconds each.** Under five feels clipped, over nine and the
  picture has nothing left to do. Ten to twelve scenes makes a minute.
- **Spoken, not written.** Read every line out loud. "Teams persist. Work
  flows to them." survives being spoken. A sentence with a subordinate
  clause in the middle does not.
- **Land the last line.** The closing scene repeats the film's claim in the
  shortest form it has. That line is also the film's `name` in the course
  content file, and it is what the play cover shows.
- **No numbers the learner cannot check.** A film is the worst place for an
  unsourced statistic, because it goes past too fast to question.

---

## The two ways to draw

### 2D, the default

A canvas, or absolutely positioned DOM nodes, moved by `upd(p, t)`. Covers
most subjects: flows, timelines, comparisons, org structures, before and
after. Start here. It is faster to build, it loads instantly, and it reads
better on a phone.

### 3D, when the subject is structure

The POM 101 films use Three.js from an import map:

```html
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js",
            "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/"}}
</script>
```

Worth the cost when the point is spatial: layers stacked above each other,
things moving between places, a structure the learner needs to hold in their
head. Not worth it for a list, a process or a comparison.

Three.js is loaded from a CDN, so a 3D film needs a network connection the
first time. Say so when the course is going somewhere offline.

---

## Sound

**Voice.** Two paths, in this order:

1. Recorded clips, when the course has a budget for them. Supply per-clip
   durations and the engine stretches each scene to fit its clip, so the
   picture never runs ahead of the voice:
   ```js
   let VOC = { d:[4.18, 5.85, 4.97, 5.16] };   // seconds, one per cue
   ```
2. `speechSynthesis`, as the fallback. It is adequate for review and for
   internal courses. It is not adequate for anything a client shows to its
   own staff without saying it is a draft.

**Music.** Synthesized in Web Audio rather than shipped as a file, so the
film stays one document. It ducks under the voice automatically. Mute is a
control on the bar, and the learner's choice is remembered.

**Captions on by default.** The CC button turns them off. It never starts
off.

---

## The shell

Every film has the same chrome, and the learner has the same controls:

```
play / pause   time   scrubber   CC   Voice   Music   fullscreen
```

The cover sits over the stage before first play: a large play button, the
film's one-line claim, and the running time. The controls fade in on hover
and on focus, and they are reachable by keyboard.

`?embed=1` drops the page padding and the outer frame so the film sits
flush inside the hub's iframe. Without it the film renders as a standalone
page, centered, with a maximum width.

---

## Talking to the hub

A film tells its parent what it is doing:

```js
parent.postMessage({type:"film", state:"play",  v:VID}, "*");
parent.postMessage({type:"film", state:"ended", v:VID}, "*");
```

The hub listens for `ended` and marks the film step complete. Without this
the learner has to confirm manually, which they will forget to do.

The hub sends one message back, `{type:"film", cmd:"pause"}`, when the
learner navigates away from the step. A film that keeps playing in a hidden
iframe is the most common complaint about embedded video.

---

## Turning a film into a video file

A film exposes two hooks so a renderer can walk it frame by frame instead of
screen-recording it. This is how you get a clean MP4 at any resolution and
any frame rate, regardless of how fast the machine draws.

```js
window.__FILMRENDER = {
  total,                              // seconds
  canvas,                             // the element to capture
  frame(t){ ... },                    // draw exactly time t, synchronously
  async audio(sampleRate){ ... }      // render the full mix offline, return a buffer
};
```

`frame(t)` must be deterministic. Given the same `t` it draws the same
picture, every time, with no dependence on elapsed real time. Anything
driven by `Date.now()` or by accumulated delta time breaks this, and the
rendered video will not match what the browser showed.

`audio()` renders through an `OfflineAudioContext`, including the music and
the voice track, so the sound lines up with the frames exactly.

A debug hook is worth keeping alongside them:

```js
window.__FILMSTATE = () => ({ total, scenes:SCENES.map(s=>s.d), t, playing });
```

---

## Checks before a film ships

- Every scene's `vo` reads correctly out loud.
- Captions match the narration word for word.
- The transcript in the course content file matches both.
- `frame(t)` called twice with the same `t` draws the same thing.
- It plays to the end and posts `ended`.
- It pauses when the hub tells it to.
- It is watchable at 375px wide.
- With `prefers-reduced-motion`, camera moves are damped and nothing
  flashes.
- Nothing in it asserts a fact that is not in the source material.
