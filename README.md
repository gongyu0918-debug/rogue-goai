# GoAI Rogue Go Arena - HTML Browser Edition

This branch is the original HTML-first edition of GoAI. It keeps the game UI in
`static/index.html`, serves it with the local FastAPI backend, and opens it in a
browser or Edge app-window. The WebView2 desktop edition is built as a child
branch on top of this branch.

## What This Version Is

GoAI is a local Go game powered by KataGo and a roguelike card layer. You can
play normal Go, Rogue card games, Ultimate card games, AI self-play study games,
and local two-player games from the same HTML interface.

This edition is intentionally simple:

- `server.py` runs the FastAPI HTTP/WebSocket backend.
- `static/index.html` is the complete browser UI.
- `launcher.py` starts the backend and opens the UI in Edge app mode when
  available.
- KataGo remains a separate sidecar engine under `katago/`.

## Features

- Classic AI games with KataGo.
- Rogue mode with 34 card effects.
- Ultimate mode with 25 high-impact cards.
- AI Rogue and local two-player Rogue variants.
- Local SGF export and import helpers.
- Chinese/English UI.
- GPU fallback order: CUDA, OpenCL, then CPU.
- Browser-friendly smoke tests for the HTML UI.

## Recommended Use

Use this branch when you want the most transparent web version:

- Developing the HTML/CSS/JavaScript UI directly.
- Testing backend WebSocket behavior in a normal browser.
- Keeping the desktop shell out of the packaging path.
- Comparing behavior before WebView2 desktop migration changes.

Use `codex/webview2-desktop-migration` when you want the packaged Windows
desktop shell.

## Requirements

- Windows 8.1, 10, or 11.
- Python 3.11 or 3.12.
- A modern browser, preferably Microsoft Edge or Chrome.
- Optional NVIDIA/OpenCL GPU for faster KataGo analysis.

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Prepare or verify KataGo assets:

```bash
python setup.py
```

The installed app normally keeps large KataGo binaries and models in
`C:\Users\<you>\AppData\Local\GoAI\katago`. The repository only tracks config
files and placeholders, not the heavy model/runtime files.

## Run

Start the browser launcher:

```bash
python launcher.py
```

Or start the backend directly:

```bash
python server.py --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

For two-player or pure UI checks without KataGo:

```bash
python server.py --no-katago --host 127.0.0.1 --port 8000
```

## Tests

Compile check:

```bash
python -m compileall app server.py launcher.py card_smoke_test.py runtime_smoke_test.py
```

Card and rules smoke test:

```bash
python card_smoke_test.py
```

Runtime smoke test against a running server:

```bash
python runtime_smoke_test.py --base-url http://127.0.0.1:8000
```

The runtime smoke covers normal AI play, Rogue card flow, Ultimate card flow,
captures, ko, analysis, and SGF output.

## Project Layout

```text
app/
  config/          Game and engine configuration
  data/            Rogue and Ultimate card catalogues
  domain/          Board state and coordinate logic
  runtime/         Engine startup, WebSocket actions, game store
static/
  index.html       Main HTML game client
  assets/          Board, stone, texture, toolbar, and card assets
docs/
  assets/          README images
katago/
  config.cfg       KataGo GPU config
  config_cpu.cfg   KataGo CPU config
server.py          FastAPI backend
launcher.py        Browser / Edge app-window launcher
runtime_smoke_test.py
card_smoke_test.py
```

## Branch Relationship

```text
codex/html-main
  original HTML browser edition

codex/webview2-desktop-migration
  inherits this branch
  adds WebView2 desktop shell packaging
```

Keep shared game, server, card, and HTML fixes in this branch first. Rebase or
merge the WebView2 branch afterward so the desktop shell inherits the same game
behavior.

## Build Notes

The HTML edition can still build the existing Windows launcher and server
executables:

```powershell
python -m PyInstaller --noconfirm GoAI.spec
python -m PyInstaller --noconfirm GoAI_Server.spec
```

The full installer script is:

```powershell
.\build_windows_release.ps1
```

The installer requires Inno Setup 6.

## License

MIT. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.
