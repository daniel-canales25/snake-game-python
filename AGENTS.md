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
    main.py            — entrypoint (Pygame init + game loop)
    core/
      game.py          — Game orchestrator (update, draw, collision, restart)
      snake.py         — Snake movement, growth, direction change, rendering
      food.py          — Food spawning (avoids snake body), rendering
    utils/
      constants.py     — Grid 30×30 of 33px cells, colors, FPS=7, initial state
assets/                — empty (no assets used yet)
tests/                 — empty (no tests yet)
```

## Application flow

### Entry point (`main.py`)

1. `pygame.init()` — initializes Pygame.
2. Creates a `990×990` window (`windowWidth × windowHeight`).
3. Instantiates `Game(screen)` which creates `Snake` and `Food`.
4. Main loop runs at **7 FPS** (`clock.tick(fps)`).

### Game loop iteration (`main.py:13-41`)

Each tick:

1. **Events** — processes all queued Pygame events:
   - `QUIT` → exits.
   - `KEYDOWN`:
     - If **game over**: `SPACE` → `game.restart()`, `ESC` → exit.
     - If **playing**: Arrow keys → `game.snake.change_direction()`.
2. **Update** (`game.update()`) — only if not game over:
   - `snake.move()` — advances snake one cell in current direction.
   - `game.check_collisions()` — checks food pickup and wall/self collisions.
3. **Draw** (`game.draw()`):
   - Fills screen black.
   - Draws grid lines (gray, rows 3–29 only).
   - Draws snake (green body, dark green head, black outline per cell).
   - Draws food (red circle).
   - Displays score ("Puntuación: N") at top-left.
   - Displays title ("SNAKE") centered in top area.
4. If game over → `game.draw_game_over()` — black screen with "GAME OVER" and instructions ("ESPACIO - Reiniciar", "ESC - Salir").
5. `pygame.display.flip()` → `clock.tick(7)`.

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
- `isGameOver` — boolean flag; when `True`, update loop is skipped and game over screen is drawn.
- `restart()` — re-creates `Snake` and `Food`, resets score to 0, sets `isGameOver=False`.

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
| Colors | black, white, green, red, blue, darkGreen, gridColor, titleColor | |

## Naming convention

All variables and constants use **camelCase** (e.g., `windowWidth`, `scoreAreaHeight`, `isGrowing`).

## Missing infrastructure

Tests, assets, CI, linter, formatter, typechecker, and README are all absent/unconfigured.
