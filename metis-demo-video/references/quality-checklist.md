# Quality checklist

Open every contact sheet in `out/qa/` (scene sheets and the 1.5 s timeline sheets) and check:

**Story**
- [ ] The hook asks a question or states a pain in under 6 seconds
- [ ] The product name appears in the first 15 seconds
- [ ] Every caption is a claim the next seconds prove
- [ ] Length fits the story (a suggestion, not a target): never padded, never rushed. Pacing and alignment come first

**Frames**
- [ ] No blank frames except the very start and end (a blank "mid" frame = a scene ended early)
- [ ] Text never runs off the frame or under a caption
- [ ] When zoomed in, the important element is centred and fully visible (not cut by the window edge)
- [ ] The captions never cover what the camera is showing (use `cy` to move the target up)
- [ ] The app shows realistic data: names, dates and progress, no lorem ipsum, no "undefined", no errors
- [ ] No real client data or real people's emails unless the user approved it
- [ ] The last card stays on screen and fades out with the music

**Camera**
- [ ] No warnings `selector not visible` in the render log (or each one was intentional)
- [ ] Holds are long enough to read (about 1.2 s minimum after a zoom lands)
- [ ] Not more than one or two tilted shots

**Voiceover (if any)**
- [ ] Captions are word-for-word the narration, shown as each phrase is spoken
- [ ] `timeline.py`: no CLICK before the SAY that describes it; no long run (about 4 s) with no SAY
- [ ] Hook typing, beats, logo, points and cards appear on the words they match
- [ ] Short-sentence runs have pauses (separate lines), nothing sounds rushed
- [ ] Hard words are pronounced right (listen to every line once); the real spelling is on screen
- [ ] The music is clearly lower under speech and returns in the gaps, with no pumping or hard on/off
- [ ] No line starts or stops abruptly; the spacing between lines feels conversational, not like full stops
- [ ] Words that can be said two ways (read, lead, live, close...) were checked with `say` or `ok`
- [ ] The voice is used with that person's consent
- [ ] Two voices: about equal speaking time, handoffs at section breaks, levels matched, every handoff listened to

**Sound**
- [ ] The music drop lands when the app flies in (`music: lift at Xs ... placed at Ys`)
- [ ] Music fades out at the end, no abrupt cut

Then watch the MP4 once at full speed before sending it.
