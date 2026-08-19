# AGENTS.md — snake-game

## Setup

- Python 3.12 required (`.python-version`).
- Dependency manager: **uv** (`uv sync` to install, `uv add <pkg>` to add).
- Only dependency: `pygame>=2.6.1` (already in `.venv/`).

## Run the game

```sh
uv run snake-game
```

## Project layout

```
src/
  snake_game/
    __init__.py        — re-exports main()
    main.py            — entrypoint (Pygame init + state machine)
    core/
      game.py          — Game orchestrator (update, draw, collision)
      snake.py         — Snake movement, growth, direction change, rendering
      food.py          — Food spawning (avoids snake body), rendering
      start_screen.py  — Start screen with leaderboard + PLAY button
      name_input.py    — Name input screen after game over
    utils/
      constants.py     — Grid 30×30 of 33px cells, colors, FPS=7, initial state
      score_manager.py — Load/save scores to scores.json (top 10)
assets/                — empty (no assets used yet)
tests/                 — empty (no tests yet)
scores.json            — auto-generated, persists player scores
```

## Application flow

### State machine (`main.py`)

The game uses a **3-state machine**:

```
START_SCREEN → PLAYING → NAME_INPUT → START_SCREEN (loop)
                     ↑         │
                     └─────────┘  (K_SPACE reinicia el juego)
```

| State | Renders | Keyboard |
|---|---|---|
| `START_SCREEN` | Leaderboard table + PLAY button | Click PLAY → `PLAYING`, `SPACE` → `PLAYING` |
| `PLAYING` | Snake game (current loop) | Arrows move, game over → `NAME_INPUT` |
| `NAME_INPUT` | Score + name input field | `ENTER` saves + `START_SCREEN`, `SPACE` restarts + `PLAYING`, `ESC` exits |

### Entry point (`main.py`)

1. `pygame.init()` — initializes Pygame.
2. Creates a `990×990` window (`windowWidth × windowHeight`).
3. Starts in `START_SCREEN` state with `StartScreen(screen)`.
4. Main loop runs at **7 FPS** (`clock.tick(fps)`).

### Game loop iteration (`main.py:21-76`)

Each tick:

1. **Events** — processes all queued Pygame events based on current state:
   - `START_SCREEN`: click PLAY or `SPACE` → transition to `PLAYING`.
   - `PLAYING`: arrow keys → `snake.change_direction()`, game over → transition to `NAME_INPUT`.
   - `NAME_INPUT`: `ENTER` → save score + `START_SCREEN`, `SPACE` → new game + `PLAYING`, `ESC` → exit.
2. **Draw** — renders current state:
   - `START_SCREEN`: `start_screen.draw()` — leaderboard table + PLAY button.
   - `PLAYING`: `game.update()` + `game.draw()` — snake game.
   - `NAME_INPUT`: `name_input.draw()` — score + name field + instructions.
3. `pygame.display.flip()` → `clock.tick(7)`.

### Start screen (`core/start_screen.py`)

- `StartScreen(screen)`: loads scores, creates PLAY button, initializes `showNotQualified=False`.
- `refresh(qualified=True)`: reloads scores from disk. If `qualified=False`, sets `showNotQualified=True` to display warning.
- `clear_message()`: sets `showNotQualified = False`.
- `draw()`: renders title "SNAKE", "MEJORES PUNTUACIONES" header, table with columns (#, NOMBRE, PUNTAJE), empty-state message, "not qualified" warning (yellow), PLAY button with hover effect, hint text.
- `handle_event(event)`: returns `True` if click on PLAY button **or** `K_SPACE` press.

### Name input screen (`core/name_input.py`)

- `NameInput(screen, score)`: initializes empty name field, stores final score.
- `draw()`: renders "FIN DEL JUEGO" (red), score, input label, text field with blinking cursor, char counter, hints (ENTER/SPACE/ESC), default name hint if empty.
- `handle_event(event)`: handles KEYDOWN — letters/numbers (max 5 chars, uppercase), BACKSPACE, ENTER → returns `("confirm", name)`.
- `update_cursor()`: toggles cursor visibility every 30 frames.

### Keyboard in NAME_INPUT

| Key | Action |
|---|---|
| Letters/Numbers | Write to field (max 5, uppercase) |
| `BACKSPACE` | Delete last character |
| `ENTER` | Save score (default "Gamer" if empty) → `START_SCREEN` |
| `SPACE` | Restart game → `PLAYING` with new `Game()` |
| `ESC` | Exit game |

### Score persistence (`utils/score_manager.py`)

- `load_scores()`: reads `scores.json`, returns sorted list of `{"name": str, "score": int}` (top 10). Returns `[]` if file missing.
- `save_score(name, score)`: appends record, sorts by score desc, keeps top 10, writes to `scores.json`. Returns `True` if saved, `False` if score too low to qualify.
- `get_top_scores()`: returns top 10 sorted scores.
- `scores.json` is auto-created in project root on first save.

### Snake (`core/snake.py`)

- **Initial state**: body `[(5,8), (4,8), (3,8)]`, direction `(1,0)` (right).
- `move()`: computes new head position by adding direction to current head. Clamps Y to `>= scoreAreaHeight` (3). Inserts new head; pops tail unless growing.
- `grow()`: sets `isGrowing=True` so next `move()` skips the pop.
- `change_direction(newDirection)`: rejects 180° reversal (opposite direction). Stores in `nextDirection`, applied on next `move()`.
- `draw()`: iterates body; draws each cell as a `cellSize×cellSize` rect. Head gets `darkGreen`, rest gets `green`. Black 1px outline on each.
- `head` property: returns `body[0]`.

### Food (`core/food.py`)

- `__init__`: calls `respawn()` with no snake body — picks random position in grid.
- `respawn(snakeBody)`: loops random `(col, row)` in valid range until position is not in `snakeBody`. Row range is `[scoreAreaHeight, gridSize-1]`.
- `draw()`: renders a red circle at cell center, radius `cellSize//2 - 2`.

### Collision logic (`game.py:48-58`)

1. **Food collision**: if `snake.head == food.position` → `snake.grow()`, score += 10, `food.respawn(snake.body)`.
2. **Wall collision**: head outside `[0, gridSize)` on X or `< scoreAreaHeight` / `>= gridSize` on Y → game over.
3. **Self collision**: head in `snake.body[1:]` → game over.

### Game state (`game.py`)

- `score` — increments by 10 per food eaten.
- `isGameOver` — boolean flag; when `True`, update loop is skipped.
- `display_title()` — renders "SNAKE" centered at top of game area using `gameTitleText`, `titleFontSize`, `titleColor`.
- `display_score()` — renders "Puntuacion: {score}" at top-left during gameplay.
- `draw_grid()` — draws grid lines from row 3..29, col 0..29.
- `restart()` — re-creates `Snake` and `Food`, resets score to 0, sets `isGameOver=False` (**dead code: never called**).
- `draw_game_over()` — renders "FIN DEL JUEGO" centered (**dead code: never called**).

### Grid & constants (`utils/constants.py`)

| Constant | Value | Notes |
|---|---|---|
| `windowWidth` | 990 | |
| `windowHeight` | 990 | |
| `gameTitle` | "Snake Game" | Window title bar |
| `fps` | 7 | Ticks per second |
| `gridSize` | 30 | 30×30 cells |
| `cellSize` | 33 | `990 // 30` |
| `scoreAreaHeight` | 3 | Top 3 rows reserved for score/title |
| `initialSnake` | `[(5,8),(4,8),(3,8)]` | Head at (5,8), tail at (3,8) |
| `initialDirection` | `(1,0)` | Moving right |
| `foodCount` | 1 | Defined but unused |
| `maxNameLength` | 5 | Max characters for player name |
| `defaultName` | "Gamer" | Default name if input is empty |
| `gameTitleText` | "SNAKE" | Title rendered during gameplay |
| `titleFontSize` | 72 | Font size for title |
| `titleColor` | (200, 200, 200) | Light gray color for title |
| Colors | black, white, green, red, blue (unused), darkGreen, gridColor | |

## Naming convention

All variables and constants use **camelCase** (e.g., `windowWidth`, `scoreAreaHeight`, `isGrowing`).

## Missing infrastructure

Tests, assets, CI, linter, formatter, typechecker, and README are all absent/unconfigured.
