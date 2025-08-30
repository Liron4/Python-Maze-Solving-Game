import pygame
from maze import Maze
from game import Game

def main():
    # Initialize Pygame
    pygame.init()

    # Set the size of the maze
    rows, cols = 31, 31  # Example size

    # Create a maze instance (don't generate immediately)
    maze = Maze(rows, cols)

    # Create a game instance with animation enabled
    game = Game(maze, animate=True)

    # Start the game loop
    game.run()

if __name__ == "__main__":
    main()