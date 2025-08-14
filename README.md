# Maze Generator

This project is a Python application that generates and displays a random maze using the Pygame library. The maze is created using a recursive Depth-First Search (DFS) algorithm, ensuring that there is a single path from the entrance to the exit.

## Project Structure

```
maze-generator
├── src
│   ├── main.py       # Entry point of the application
│   ├── maze.py       # Contains the Maze class for maze generation
│   └── game.py       # Contains the Game class for Pygame logic and display
├── requirements.txt   # Lists the dependencies required for the project
└── README.md          # Documentation for the project
```

## Requirements

To run this project, you need to have Python installed along with the Pygame library. You can install the required dependencies by running:

```
pip install -r requirements.txt
```

## Running the Application

To start the maze generator, run the following command in your terminal:

```
python src/main.py
```

This will initialize the maze and open a Pygame window displaying the generated maze.

## Features

- Random maze generation with a single path from entrance to exit.
- Visual representation of the maze using Pygame.
- Configurable maze size by modifying the parameters in the `main.py` file.

Enjoy exploring the maze!