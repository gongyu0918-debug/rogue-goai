# rogue-go-arena Refactor Plan

This project is stable enough to play, but the codebase has two high-risk growth points:

- `static/index.html` has been acting as the UI shell, WebSocket client, board renderer, i18n layer, and card UI host.
- `server.py` still owns HTTP routes, WebSocket flow, AI move orchestration, Rogue effects, Ultimate effects, scoring helpers, and KataGo sync.

The goal is controlled extraction, not a broad rewrite. Every step should leave the app runnable and covered by smoke tests.

## Workspace Policy

- Primary development workspace: `F:\Workspaces\rogue go project\rogue-go-arena`
- Playground repo path: `F:\Workspaces\Playground\projects\apps\rogue-goai`
- Treat Playground as source/publish/sync history. Do new implementation work in the primary workspace, then sync intentionally.

## Current Frontend Split

Done:

- `static/js/rogue_cards_ui.js`
  - Rogue card offer modal
  - Ultimate card offer modal
  - Rogue/Ultimate card wiki rendering
  - Rogue skill button binding and display state
  - Ultimate status bar rendering
- `static/js/card_catalog.js`
  - Card id lists
  - Card presentation metadata
  - Localized card lookup
  - Safe card icon/meta markup helpers
- `static/js/card_board_marks.js`
  - Rogue seal/blackhole/golden-corner/fog board overlays
  - Ko marker
  - Joseki/puppet/Ultimate target markers
  - AI Rogue seal overlays
- `static/js/card_state.js`
  - Rogue/Ultimate card offer state
  - Active Rogue/AI card state
  - Rogue seal/uses/puppet state
  - Ultimate selection state
  - Card turn timer state
- `static/js/card_turn_timer.js`
  - Rogue Quick Thinking countdown
  - Ultimate Quick Thinking countdown
  - Card turn timer cleanup and UI refresh
- `static/js/board_layout.js`
  - Board canvas element/context ownership
  - Stage preset sizing
  - Canvas DPR sizing and CSS fit variables
  - Board recovery/watchdog helpers
- `static/js/board_assets.js`
  - Board and stone texture loading
  - Board visual cache invalidation
  - Board base texture painting
  - Stone sprite cache and texture painting
- `static/js/board_renderer.js`
  - Board grid, star points, stones, and move numbers
  - Hint and review-hint drawing
  - Territory overlay drawing
  - Main canvas render pass
- `static/js/board_input.js`
  - Board coordinate conversion
  - Pointer/touch hover and placement handling
  - Fine-tune placement state and controls
  - Player move commit and AI response timeout

Still in `static/index.html`:

- WebSocket message dispatch
- i18n bootstrap and generic UI localization
- Review/SGF controls

## Frontend Extraction Roadmap

1. `static/js/i18n.js`
   - Move locale cache, `ui`, `rankLabel`, `applyLanguage` helpers.
   - Keep DOM writes grouped by screen/component.

2. `static/js/board_renderer.js`
   - Add a narrow renderer API and move winrate curve when the shell UI split is ready.
   - Leave only a narrow API: `renderBoard(state)`, `resizeBoard()`, `setBoardOptions(options)`.

3. `static/js/ws_client.js`
   - Move WebSocket connect/reconnect/send and message routing.
   - Replace the current large `handleMessage` function with typed handlers by message type.

4. `static/js/card_state.js`
   - Replace direct shared lexical bindings with a small state API (`getCardState`, `patchCardState`, reset helpers).
   - Do this only after WebSocket handlers and board overlays agree on the same state shape.

5. `static/js/setup_controls.js`
   - Move start-game controls, rank selectors, handicap/time/variant controls.

## Backend Extraction Roadmap

1. `app/gameplay/rogue_effects.py`
   - Move player Rogue effect activation and per-move hooks.
   - Keep functions pure where possible: input `GoGame`, return effect result.

2. `app/gameplay/ultimate_effects.py`
   - Move `_apply_ultimate_effect`, `_ultimate_ai_move`, `_ultimate_force_score`.
   - Avoid adding new Ultimate branches in `server.py`.

3. `app/gameplay/ai_moves.py`
   - Move AI move selection variants: avoid points, no-resign retry, suboptimal, style generation.
   - Keep KataGo calls behind a small engine adapter.

4. `app/runtime/ws_handlers.py`
   - Split the 600+ line `websocket_endpoint` into action handlers.
   - Preserve the current `WebSocketActionContext` direction; expand it instead of passing many globals.

5. `app/services/card_config_service.py`
   - Move live card config reload/save/reset orchestration out of `server.py`.
   - Introduce per-game config snapshots so editing cards affects new games, not active games.

## Anti-Sprawl Rules

- No new feature should add another 100+ lines to `static/index.html` or `server.py` unless it is temporary and immediately followed by extraction.
- New card UI belongs in `static/js/rogue_cards_ui.js` or a narrower card module.
- New board drawing for card effects belongs in `static/js/card_board_marks.js`.
- New Rogue/Ultimate server logic belongs in gameplay modules, not directly in `server.py`.
- Prefer data-driven entries in `app/data/cards.json` and tuning values over hard-coded branches.

## Verification Gates

For frontend card/UI changes:

- `python card_smoke_test.py`
- `python card_editor_effect_smoke.py`
- Browser/Playwright check for card editor and offer modal rendering.

For gameplay or AI changes:

- Real server runtime smoke: `python runtime_smoke_test.py --base-url http://127.0.0.1:<port>`
- Verify the server uses a real KataGo backend when the change touches AI flow.

For releases:

- Build installer.
- Install into `F:\rogue-go-arena`.
- Verify installed server `/status`, `/card-editor`, root page, and installer hash.
