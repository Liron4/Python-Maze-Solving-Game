# Maze Generator

This project is a Python application that generates and displays a random maze using the Pygame library. The maze is created using a recursive Depth-First Search (DFS) algorithm, ensuring that there is a single path from the entrance to the exit.

## Project Structure

# Python Maze Solving Game

This repository contains a Pygame-based maze generator and solver. The project generates a random maze (DFS) and provides multiple solver algorithms plus a simulation/visualization layer.

Quick highlights
- Maze generation: recursive DFS-based generator
- Solvers: path (DFS) solver and a right-hand wall-following solver
- Visuals: Pygame renderer with adaptive cell sizing and overlay UI (timer, ending screens)
- Multiple configuration profiles for different resolutions/performance

Project structure
```
Python-Maze-Solving-Game/
├── README.md
├── requirements.txt
└── src/
	├── main.py           # Entry point; accepts configuration name or --list
	├── config.py         # Configuration presets (ultra_hd, high_quality, standard, performance)
	├── game/             # Game controller, renderer and UI components
	│   ├── __init__.py
	│   ├── game_controller.py
	│   ├── game_renderer.py
	│   └── timer_display.py
	├── maze/             # Maze generation and structure
	│   ├── __init__.py
	│   ├── maze_generator.py
	│   └── maze_structure.py
	└── solvers/          # Solver implementations
		├── __init__.py
		├── path_solver.py
		└── right_hand_solver.py
    
	assets/
		images/           # sprites and gifs used by the renderer
```

Requirements

Install dependencies with pip:

```powershell
pip install -r requirements.txt
```

Running the game

- List available configurations and current maze sizes:

```powershell
python src/main.py --list
```

- Start the game with a preset configuration (examples):

```powershell
python src/main.py ultra_hd
python src/main.py high_quality
python src/main.py standard
python src/main.py performance
```

Notes about the configuration
- Presets are defined in `src/config.py`. Each preset sets the window resolution and the maze rows/cols to ensure the maze fills the screen and cells remain visually large.
- Use `--list` to see current presets and maze sizes.

Files to be aware of
- `src/main.py` — argument parsing and bootstrapping the GameController
- `src/game/game_controller.py` — game loop, UI, ending screens
- `src/game/game_renderer.py` — draws the maze, robot, and UI overlays
- `src/maze/maze_generator.py` — maze generation algorithm
- `src/solvers/*` — solver implementations

Version control notes
- A `.gitignore` exists to ignore `__pycache__/`, `.pyc` files, virtualenv folders, and common editor artifacts.
- Keep `__init__.py` files tracked in git (they are small and necessary for package imports).

Contributing

If you want to add a solver, tweak UI, or change presets, edit the appropriate module under `src/` and test locally with one of the configuration presets.

That's it — enjoy exploring and improving the maze solver!
