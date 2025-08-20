import pygame
import os

class Game:
    def __init__(self, maze_obj, window_size=(900, 900), animate=True):
        self.maze_obj = maze_obj
        self.maze = maze_obj.get_maze()
        self.window_size = window_size
        self.cell_size = min(window_size[0] // maze_obj.cols, window_size[1] // maze_obj.rows)
        self.screen = None
        self.running = True
        self.animate = animate
        
        # Animation state
        self.generation_started = False
        self.animation_speed = 100  # milliseconds between steps
        self.last_step_time = 0
        self.paused = False  # Add pause state
        
        # Load robot images
        self.robot_images = self._load_robot_images()
        self.current_direction = "down"  # default direction
        
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Maze Generator")

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
                images[direction] = pygame.transform.scale(images[direction], (self.cell_size, self.cell_size))
                
        except pygame.error:
            # Fallback if images can't be loaded
            images = None
            
        return images

    def _get_direction(self, prev_pos, curr_pos):
        """Determine robot direction based on movement"""
        if prev_pos is None or curr_pos is None:
            return "down"
            
        dx = curr_pos[1] - prev_pos[1]  # col difference
        dy = curr_pos[0] - prev_pos[0]  # row difference
        
        if dx > 0: return "right"
        elif dx < 0: return "left"
        elif dy > 0: return "down"
        elif dy < 0: return "up"
        else: return self.current_direction  # no movement

    def draw_maze(self):
        start_pos = self.maze_obj.get_start()
        end_pos = self.maze_obj.get_end()
        
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                x = col * self.cell_size
                y = row * self.cell_size
                
                # Default colors: black for walls (0), white for paths (1)
                if self.maze[row][col] == 0:
                    color = (50, 50, 50)  # Dark gray for walls
                else:
                    color = (255, 255, 255)  # White for paths
                
                # Special colors for start and end
                if (row, col) == start_pos and self.maze_obj.phase != "dfs":
                    color = (0, 255, 0)  # Green for start
                elif (row, col) == end_pos and self.maze_obj.phase == "complete":
                    color = (255, 0, 0)  # Red for end
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                
                # Draw grid lines for better visibility
                pygame.draw.rect(self.screen, (128, 128, 128), (x, y, self.cell_size, self.cell_size), 1)
        
        # Draw robot at current position during generation
        if self.animate and not self.maze_obj.generation_complete and self.maze_obj.current_pos:
            self._draw_robot()

    def _draw_robot(self):
        """Draw the drilling robot at current position"""
        if not self.robot_images or not self.maze_obj.current_pos:
            return
            
        row, col = self.maze_obj.current_pos
        x = col * self.cell_size
        y = row * self.cell_size
        
        robot_image = self.robot_images.get(self.current_direction, self.robot_images["down"])
        self.screen.blit(robot_image, (x, y))

    def run(self):
        clock = pygame.time.Clock()
        prev_pos = None
        
        # Start maze generation
        if self.animate:
            self.maze_obj.start_generation()
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Skip animation, complete instantly
                        if not self.maze_obj.generation_complete:
                            self.maze_obj.create_maze()  # Use instant generation
                            self.maze_obj.generation_complete = True
                    elif event.key == pygame.K_RETURN:
                        # Toggle pause
                        self.paused = not self.paused

            # Animation step (only if not paused)
            if (self.animate and not self.maze_obj.generation_complete and not self.paused and
                current_time - self.last_step_time > self.animation_speed):
                
                prev_pos = self.maze_obj.current_pos
                continuing = self.maze_obj.step_generation()
                
                # Update robot direction
                if self.maze_obj.current_pos:
                    self.current_direction = self._get_direction(prev_pos, self.maze_obj.current_pos)
                
                self.last_step_time = current_time

            # Drawing
            self.screen.fill((30, 30, 30))  # Dark background
            self.draw_maze()
            
            # Show instructions
            font = pygame.font.Font(None, 36)
            
            # Top left instruction (skip)
            if not self.maze_obj.generation_complete:
                text = font.render("Press SPACE to skip animation", True, (255, 255, 255))
                self.screen.blit(text, (10, 10))
            
            # Bottom left instruction (pause/unpause)
            if not self.maze_obj.generation_complete:
                pause_text = "Press ENTER to resume" if self.paused else "Press ENTER to pause"
                pause_surface = font.render(pause_text, True, (255, 255, 255))
                self.screen.blit(pause_surface, (10, self.window_size[1] - 50))
            
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()