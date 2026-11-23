# Filming a Metis hub (Apps Script / single-file HTML tools)

The hubs (Onboarding, Client, Partnership Radar, L&D, EN dashboard) are single HTML files served by Google Apps Script. To film one
without touching real data, run an unmodified copy of the live HTML with a fake backend injected before its own code.

## The pattern

1. Copy the hub HTML into the video project's `assets/` (copy it out of iCloud first; reading from `~/Desktop/Metis` can time out).
   Do not edit it: a clip of the real file is what Rohan asks for ("direct clips from the hub itself").
2. Inject `templates/apps-script-mock-backend.js` through `app.inject`. It defines `window.google.script.run` as a chainable proxy
   (`withSuccessHandler`, `withFailureHandler`, then any server method) answered from an in-memory table. Add a method per backend
   call the hub makes. Find them with a search for `google.script.run` in the HTML.
3. Hubs decide "served by Apps Script" with `typeof google !== "undefined" && google.script && google.script.run`. With the mock
   present the served-only UI appears (the Onboarding Hub's "Find a time" buttons exist only then). Without it the hub falls back to
   localStorage and some features are missing.
4. Make the identity deterministic: `getBootstrap` returns the demo user's email and `state: null` for a first-run wizard, or a
   seeded state for a mid-journey shot. Set `app.fake_date` to a weekday so "this week" and slot days make sense.
5. Capture state changes by clicking the real controls. Seed state in `setup_js` only for things the video does not show happening.
6. Open `assets/hub.html` through the renderer; never film it from a `file://` page in the browser pane (storage is blocked).

## Find selectors fast

Drive the hub in headless Chrome with the mock and print interactive elements per page (data attributes, ids, button text). In the
Onboarding Hub: sidebar `.nav-btn[data-page="..."]`, wizard `#wzStart2`, `[data-wzrole]`, `[data-wzlevel]`, `[data-wzoffice]`,
`#wzRoleNext`, `#wzMetisNext`, `#wzFinish`, Day 1 `.sub-cb`, `.st[data-step]`, roadmap `[data-check]`, `[data-how]`, chats
`[data-avail="<email>"]`, `.avail-slot`, `[data-bookyes]`, `#chatSummary`, `#chatSearch`, tools `[data-tooltab]`, dictionary `[data-dmode]`,
`.fc-card`, FAQ `#faqQ`.

## Gotchas found on the Onboarding Hub

- **Auto-advance:** ticking the last item of a Day 1 step completes it and opens the next. A later click on "Mark step done" lands on
  the next, empty step and triggers "N items unchecked, mark done anyway?". Film the ticks, not the buttons.
- **Embedded sign-in walls:** the wizard's firm-video step and the Home "welcome from leadership" video are Drive embeds that render
  as a Google "Sign in" box. Skip that wizard step with one `js` step that clicks Next twice in the same tick, and do not scroll Home
  past the hero and the jump cards.
- **Hot-linked photos** (metisstrategy.com team photos) load in the render, so the machine needs internet. Initials avatars are the fallback.
- **Popups:** "Find a time" slots are `target=_blank` links. Add a capture-phase listener that prevents their default so no tab opens,
  and show the invite with a `notify` toast instead of a real Google Calendar page.
- **The name** comes from the email, so the wizard greets "Hi <first name>" with no typing.
- **Zoom framing:** the hub's text is small at 1440 px. Use `focus` with scale 1.3 to 1.8 on the element the narration names, then `fit`.
- **Hidden elements have no size:** open the tab or drawer first, or the camera move is skipped (`selector not visible` in the log).
- **Nothing real is recorded:** the mock never writes anywhere; the hub's own localStorage inside the render browser is thrown away.

## After the render

Run `scripts/timeline.py` and read it against the narration; run the contact sheets; confirm no frame shows a sign-in wall, an
error toast, a real person's private note, or a sync badge reading "Offline".
