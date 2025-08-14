import pygame
from maze import Maze
from game import Game

def main():
    # Initialize Pygame
    pygame.init()

    # Set the size of the maze
    rows, cols = 21, 21  # Example size (20 rows, 20 columns)

    # Create a maze instance
    maze = Maze(rows, cols)

    # Create a game instance
    game = Game(maze)

    # Start the game loop
    game.run()

if __name__ == "__main__":
    main()