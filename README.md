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
| [`executive-slide-builder`](executive-slide-builder/) | Executive storytelling, narrative structure, strategic framing, and translating technical content into C-Suite-ready language. This skill produces content strategy and narrative structure only, not files. Two modes:... |
| [`metis-brand-identity`](metis-brand-identity/) | Metis Strategy brand identity reference and compliance layer. Automatically consulted by metis-pptx, metis-html-slides, metis-pdf-creator, metis-whitepaper, and metis-premier-proposal during output generation. Also... |
| [`metis-build-studio`](metis-build-studio/) | Build the files people request in Metis Build Studio (https://claude.ai/artifact/9zvDDHBE8Zs1QaQxZHNWPq) on this computer, and report progress back to the Studio. The Studio is where a consultant picks what to build... |
| [`metis-capability-map`](metis-capability-map/) | Generate L1-L3 business capability maps aligned to customer/guest/patient journey stages for any industry. Use for capability maps, capability models, value chain mapping, capability heat maps, maturity assessments,... |
| [`metis-claude-help`](metis-claude-help/) | Metis Claude Help, the skill management utility for Claude Code at Metis Strategy. Discover and install skills, publish new skills, search FAQs and tips, share knowledge, and report bugs. Invoke with... |
| [`metis-demo-video`](metis-demo-video/) | Make a polished Metis video as a 1080p MP4 with music (optional AI voiceover in Rohan's or Romain's voice), rendered frame by frame from HTML so it plays smoothly however slow the app is. It asks a few questions... |
| [`metis-html-slides`](metis-html-slides/) | Generate HTML presentations as self-contained single files with sidebar navigation, scrollable sections, and interactive components. Use when the user wants a browser-viewable presentation. Ideal for internal decks,... |
| [`metis-humanizer`](metis-humanizer/) | Rewrite text to sound collaborative and human, not pushy or authoritative, free of AI-generated writing patterns, and lightly in Metis Strategy's brand voice. Builds on the humanizer skill's detection catalog... |
| [`metis-learning-module`](metis-learning-module/) | Build training in the POM 101 format: a self-contained HTML course hub with numbered modules, a step-by-step lesson player, animated one-minute films, knowledge checks, a role explorer, a glossary and saved progress.... |
| [`metis-legal-drafting`](metis-legal-drafting/) | Draft Statements of Work (SOWs) from client templates and Metis proposals, and review/redline Master Services Agreements (MSAs) from the Supplier perspective. Use whenever a consultant asks to draft an SOW, populate... |
| [`metis-narrative-scroll`](metis-narrative-scroll/) | Build a Metis-branded narrative scroll: one self-contained HTML file that a reader scrolls top to bottom, with a fixed masthead, a hero, a contents list whose rows are the navigation, sections that reveal as you... |
| [`metis-pdf-creator`](metis-pdf-creator/) | Creates professional, on-brand PDF documents for Metis Strategy using PDFKit (Node.js). Use for consultant guides, setup documents, reference cards, one-pagers, methodology overviews, CDLC materials, and internal... |
| [`metis-pptx`](metis-pptx/) | Create or edit PowerPoint (.pptx) files. Two modes: (1) template-preserving editing when an existing .pptx is provided, (2) generation when a new Metis-branded deck is needed. Trigger on "slides," "deck,"... |
| [`metis-premier-proposal`](metis-premier-proposal/) | Produce premier client-ready proposals, capability decks, and case studies for Metis Strategy BD work. Use when the user asks to create, build, draft, or iterate on a proposal, capabilities deck, case study, BD... |
| [`metis-steerco`](metis-steerco/) | Build executive Steering Committee (SteerCo) decks that drive leadership decisions. Use this whenever the user mentions a "SteerCo," "steering committee," "steerco update/deck," "exec/leadership update deck,"... |
| [`metis-whitepaper`](metis-whitepaper/) | Produce Metis Strategy whitepapers, thought leadership PDFs with a specific structure, visual style, and editorial voice. Use whenever a user asks to create, draft, or structure a whitepaper, thought leadership... |
| [`pls-fix`](pls-fix/) | Review a deck (.pptx) or document (.docx) where the user has left comments, make the edits the comments ask for, and reply to each comment inside the file, threaded under it, never deleting or resolving any comment... |
| [`presentation-editor`](presentation-editor/) | Edits presentations that already exist. Turns a short informal ask ("add System Demo to the E2E view", "move this after Sprint Review", "add this metric", "make this less crowded", "fix the spacing", "tighten slide... |
| [`spotlight`](spotlight/) | Post something you just made with AI to Spotlight, the EC team showcase. Reads the current session, drafts the card, shows exactly what will post, and posts only after a yes. Invoke with /spotlight, or when the... |
| [`teardown`](teardown/) | Build an interactive 3D simulator of a real machine or mechanism (an engine, a landing gear, a walking linkage, a pump, a gearbox) as one offline HTML page people can take apart, with live panels driven by the same... |

Notes:

- `metis-pptx` needs the Metis master template (`assets/master.pptx`, 25 MB), which is not in this repo. Get it from the Metis skill registry (`metis-claude-help`).
- `teardown` leaves out three large demo GIFs.
