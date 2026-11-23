---
name: ask-gpt
description: Call an OpenAI model (ChatGPT/GPT) from inside a Claude Code session, so a second model can draft, critique, or cross-check work without the user copying text between two apps. Trigger on "ask ChatGPT", "ask GPT", "what would ChatGPT say", "second opinion", "cross-check with OpenAI", "have GPT review this", "compare with GPT", "red team this", or when the user wants two models to disagree on purpose. Also use when the user is about to paste something into ChatGPT by hand. Do NOT use for ordinary work Claude should just do, and do NOT route client data to it without the user saying yes first.
---

# Ask GPT

A local CLI that sends a prompt to an OpenAI model and prints the answer. Use it
when a second model genuinely adds something: a critique, an alternative framing,
a disagreement worth surfacing. Do not use it as a rubber stamp on your own work.

## The command

```
PY="C:/Users/romain/AppData/Local/Programs/Python/Python312/python.exe"
ASKGPT="C:/Users/romain/.claude/tools/askgpt/askgpt.py"
"$PY" "$ASKGPT" [options] "prompt"
```

| Option | What it does |
|---|---|
| `-f PATH` | Attach a file's text. Repeatable. `.pptx` text is extracted slide by slide. |
| `-s TEXT` | System prompt. Set the role before you ask. |
| `-t NAME` | Keep the conversation under a name, so follow-up calls have the earlier turns. |
| `--reset` | Clear that thread first. |
| `--history` | Print the thread and stop. |
| `-m ID` | Model id. `--list-models` shows what the key can use. |
| `--effort` | `minimal` / `low` / `medium` / `high` on reasoning models. |
| `--backend` | `api` (key) or `codex` (ChatGPT plan). Defaults to whichever is set up. |

Answer goes to stdout. A one-line usage note goes to stderr.

## How to use it well

**Give GPT the artifact, not a description of it.** The reason the old
ChatGPT-then-Claude loop was slow is that the critic never saw the output. Attach
the real file with `-f` so the critique is about what exists.

```bash
"$PY" "$ASKGPT" -f "G:/My Drive/Decks/steerco.pptx" \
  -s "You are a skeptical CIO reading this deck cold." \
  "Where does the argument not land? Name slides."
```

**Use a thread when iterating.** Without `-t` every call starts from nothing, which
is the same problem in a new shape.

```bash
"$PY" "$ASKGPT" -t steerco "Now redo slide 4 only, keeping the rest."
```

**Ask for disagreement, not agreement.** A second model that just agrees has cost
money and told you nothing. Prompt for the strongest objection.

## Rules

- Say what you are sending before you send it. The user should know which file
  leaves the machine.
- Do not send client material without an explicit yes in this conversation.
  Lumen, Metis internal, and anything under `G:\My Drive` counts as client
  material. This calls a third party outside the Metis boundary.
- Report GPT's answer as GPT's answer, attributed and separate from your own view.
  If you disagree with it, say so and say why.
- Do not chain calls in a loop on your own. One call, show the result, then decide.
- Never print or echo the API key.

## When it is not set up

If the command exits with code 2, nothing is configured yet. Tell the user which
of the two paths they want and stop:

- **API key**: a line `OPENAI_API_KEY=sk-...` in `C:\Users\romain\.claude\.env`,
  then restart the session. Billed per token, separate from any ChatGPT plan.
- **Codex CLI**: `npm install -g @openai/codex` then `codex login` with the
  ChatGPT account. Needs Node, which is not installed on this machine.
