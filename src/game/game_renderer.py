"""
GameRenderer - Handles all rendering operations for the maze game.
Follows Single Responsibility Principle - only handles rendering and drawing.
"""
import pygame
import os


class GameRenderer:
    """Handles rendering of the maze, robot, and UI elements."""
    
    def __init__(self, window_size, maze_structure):
        self.window_size = window_size
        self.maze_structure = maze_structure
        
        # Apply zero margins for all resolutions to maximize maze size
        ui_margin_top = 0   # No top margin - maze goes to edge
        ui_margin_sides = 0  # No side margins - full width
        bottom_margin = 0    # No bottom margin - full height
            
        available_width = window_size[0] - (ui_margin_sides * 2)
        available_height = window_size[1] - ui_margin_top - bottom_margin
        
        # Calculate optimal cell size with minimum size constraint
        cell_width = available_width // maze_structure.cols
        cell_height = available_height // maze_structure.rows
        self.cell_size = max(min(cell_width, cell_height), 12)  # Increased minimum to 12px for ultra visibility
        
        # Calculate actual maze size and centering offsets
        self.maze_width = self.cell_size * maze_structure.cols
        self.maze_height = self.cell_size * maze_structure.rows
        self.offset_x = (window_size[0] - self.maze_width) // 2
        self.offset_y = ((window_size[1] - ui_margin_top) - self.maze_height) // 2 + ui_margin_top
        
        # Load robot images
        self.robot_images = self._load_robot_images()
        
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Maze Generator & Solver - Optimized View")
        self.font = pygame.font.Font(None, 36)

    def _load_robot_images(self):
        """Load robot drilling animation images"""
        images = {}
        robot_path = "src/images/maze_gen_robot"
        
        try:
            images["down"] = pygame.image.load(os.path.join(robot_path, "drill_spin_down.gif"))
            images["left"] = pygame.image.load(os.path.join(robot_path, "drill_spin_left.gif"))
            images["right"] = pygame.image.load(os.path.join(robot_path, "drill_spin_right.gif"))
            images["up"] = pygame.image.load(os.path.join(robot_path, "drill_spin_up.gif"))
            
            # Scale images to fit cell size
            for direction in images:
                images[direction] = pygame.transform.scale(images[direction], 
                                                         (self.cell_size, self.cell_size))
                
        except pygame.error:
            # Fallback if images can't be loaded
            images = None
            
        return images

    def draw_maze(self, path_solver_path=None, right_hand_path=None):
        """Draw the complete maze with solution paths"""
        start_pos = self.maze_structure.get_start()
        end_pos = self.maze_structure.get_end()
        rows = self.maze_structure.rows
        cols = self.maze_structure.cols
        
        for row in range(rows):
            for col in range(cols):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                
                # Border override: always dark black unless it's start/end
                is_border = (row == 0 or row == rows - 1 or col == 0 or col == cols - 1)
                if is_border and (row, col) not in (start_pos, end_pos):
                    color = (0, 0, 0)  # dark black border
                else:
                    # Default colors: dark gray for walls (0), white for paths (1)
                    if self.maze_structure.is_wall(row, col):
                        color = (50, 50, 50)
                    else:
                        color = (255, 255, 255)
                    
                    # Blue trail for right-hand solver path (drawn first, lowest priority)
                    if right_hand_path and (row, col) in right_hand_path:
                        color = (0, 100, 255)  # Blue trail
                    
                    # Yellow trail for path solver (higher priority than blue)
                    if path_solver_path and (row, col) in path_solver_path:
                        color = (255, 255, 0)  # Yellow trail
                    
                    # Special colors for start and end (always visible, highest priority)
                    if (row, col) == start_pos:
                        color = (0, 255, 0)  # Green for start
                    elif (row, col) == end_pos:
                        color = (255, 0, 0)  # Red for end
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                # Draw grid lines for better visibility
                pygame.draw.rect(self.screen, (128, 128, 128), (x, y, self.cell_size, self.cell_size), 1)

    def draw_robot(self, position, direction="down"):
        """Draw the drilling robot at the given position"""
        if not self.robot_images or not position:
            return
            
        row, col = position
        x = col * self.cell_size + self.offset_x
        y = row * self.cell_size + self.offset_y
        
        robot_image = self.robot_images.get(direction, self.robot_images["down"])
        self.screen.blit(robot_image, (x, y))

    def draw_status_text(self, phase, paused=False):
        """Draw status text in the bottom left corner"""
        if phase == "generation":
            if paused:
                text = "Generation PAUSED - Press ENTER to resume"
                color = (255, 255, 255)
            else:
                text = "Generating maze... Press SPACE to skip"
                color = (255, 255, 255)
        elif phase == "path_solving":
            if paused:
                text = "Path solving PAUSED - Press ENTER to resume"
                color = (255, 255, 0)
            else:
                text = "Solving with optimal path..."
                color = (255, 255, 0)
        elif phase == "right_hand":
            if paused:
                text = "Right-hand solving PAUSED - Press ENTER to resume"
                color = (0, 100, 255)
            else:
                text = "Solving with right-hand rule..."
                color = (0, 100, 255)
        else:
            text = "All simulations complete!"
            color = (0, 255, 0)
        
        # Draw main status text
        status_surface = self.font.render(text, True, color)
        self.screen.blit(status_surface, (10, self.window_size[1] - 80))
        
        # Draw pause instruction if not complete
        if phase != "complete":
            pause_text = "Press ENTER to pause/resume"
            pause_surface = self.font.render(pause_text, True, (200, 200, 200))
            self.screen.blit(pause_surface, (10, self.window_size[1] - 40))

    def clear_screen(self):
        """Clear the screen with dark background"""
        self.screen.fill((30, 30, 30))

    def update_display(self):
        """Update the pygame display"""
        pygame.display.flip()
        
    def get_screen(self):
        """Get the pygame screen surface"""
        return self.screen
