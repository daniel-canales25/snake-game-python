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
      game.py          — Game orchestrator (update, draw, collision)
      snake.py         — Snake movement, growth, rendering
      food.py          — Food spawning (avoids snake body), rendering
    utils/
      constants.py     — Grid 20×20 of 30px cells, colors, FPS=10
assets/                — empty (no assets used yet)
tests/                 — empty (no tests yet)
```

## Architecture notes

- All variables and constants use **camelCase** naming convention.
- Grid-based: `gridSize=20`, `cellSize=30`, positions are `(col, row)` tuples.
- FPS is locked to 10 — snake moves one cell per tick.
- Snake direction change prevents 180° reversal (checked in `Snake.changeDirection`).
- Food respawn avoids current snake body positions.
- No keyboard input implemented — game loop only handles `pygame.QUIT`. `Snake.changeDirection()` exists but is never called.

## Missing infrastructure

Tests, assets, CI, linter, formatter, typechecker, and README are all absent/unconfigured.
