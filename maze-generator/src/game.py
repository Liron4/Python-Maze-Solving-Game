import pygame

class Game:
    def __init__(self, maze_obj, window_size=(900, 900)):
        self.maze_obj = maze_obj
        self.maze = maze_obj.get_maze()
        self.window_size = window_size
        self.cell_size = min(window_size[0] // maze_obj.cols, window_size[1] // maze_obj.rows)
        self.screen = None
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Maze Generator")

    def draw_maze(self):
        start_pos = self.maze_obj.get_start()
        end_pos = self.maze_obj.get_end()
        
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                x = col * self.cell_size
                y = row * self.cell_size
                
                # Default colors: black for walls (0), white for paths (1)
                if self.maze[row][col] == 0:
                    color = (0, 0, 0)  # Black for walls
                else:
                    color = (255, 255, 255)  # White for paths
                
                # Special colors for start and end
                if (row, col) == start_pos:
                    color = (0, 255, 0)  # Green for start
                elif (row, col) == end_pos:
                    color = (255, 0, 0)  # Red for end
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                # Draw border
                pygame.draw.rect(self.screen, (128, 128, 128), (x, y, self.cell_size, self.cell_size), 1)

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.draw_maze()
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()