# Claude skills

The Claude skills we built and use at Metis on the Lumen project.

## Install one skill

1. Click **Code**, then **Download ZIP** (or clone the repo).
2. Copy the skill folder you want (for example `pls-fix`) into your `.claude/skills` folder:
   - Windows: `C:\Users\<you>\.claude\skills`
   - Mac: `~/.claude/skills`
3. Start a new Claude Code session. The skill loads on its own.

## The skills

| Skill | What it does |
|---|---|
| [`ask-gpt`](ask-gpt/) | Call an OpenAI model (ChatGPT/GPT) from inside a Claude Code session, so a second model can draft, critique, or cross-check work without the user copying text between two apps. Trigger on "ask ChatGPT", "ask GPT",... |
| [`metis-build-studio`](metis-build-studio/) | Build the files people request in Metis Build Studio (https://claude.ai/artifact/9zvDDHBE8Zs1QaQxZHNWPq) on this computer, and report progress back to the Studio. The Studio is where a consultant picks what to build... |
| [`metis-demo-video`](metis-demo-video/) | Make a polished Metis video as a 1080p MP4 with music (optional AI voiceover in Rohan's or Romain's voice), rendered frame by frame from HTML so it plays smoothly however slow the app is. It asks a few questions... |
| [`metis-learning-module`](metis-learning-module/) | Build training in the POM 101 format: a self-contained HTML course hub with numbered modules, a step-by-step lesson player, animated one-minute films, knowledge checks, a role explorer, a glossary and saved progress.... |
| [`metis-narrative-scroll`](metis-narrative-scroll/) | Build a Metis-branded narrative scroll: one self-contained HTML file that a reader scrolls top to bottom, with a fixed masthead, a hero, a contents list whose rows are the navigation, sections that reveal as you... |
| [`metis-steerco`](metis-steerco/) | Build executive Steering Committee (SteerCo) decks that drive leadership decisions. Use this whenever the user mentions a "SteerCo," "steering committee," "steerco update/deck," "exec/leadership update deck,"... |
| [`pls-fix`](pls-fix/) | Review a deck (.pptx) or document (.docx) where the user has left comments, make the edits the comments ask for, and reply to each comment inside the file, threaded under it, never deleting or resolving any comment... |
| [`presentation-editor`](presentation-editor/) | Edits presentations that already exist. Turns a short informal ask ("add System Demo to the E2E view", "move this after Sprint Review", "add this metric", "make this less crowded", "fix the spacing", "tighten slide... |
| [`spotlight`](spotlight/) | Post something you just made with AI to Spotlight, the EC team showcase. Reads the current session, drafts the card, shows exactly what will post, and posts only after a yes. Invoke with /spotlight, or when the... |
| [`teardown`](teardown/) | Build an interactive 3D simulator of a real machine or mechanism (an engine, a landing gear, a walking linkage, a pump, a gearbox) as one offline HTML page people can take apart, with live panels driven by the same... |

Notes:

- `teardown` leaves out three large demo GIFs.
