"""
GameController - Main game loop and state management.
Follows Single Responsibility Principle - only handles game flow control.
"""
import pygame
import time
from maze.maze_generator import MazeGenerator
from maze.maze_structure import MazeStructure
from solvers.path_solver import PathSolver
from solvers.right_hand_solver import RightHandSolver
from game.game_renderer import GameRenderer
from game.timer_display import TimerDisplay


class GameController:
    """Controls the main game loop and coordinates different game phases."""
    
    def __init__(self, rows, cols, window_size=(1600, 900), animation_speed=25, animate=True):  # Upgraded to 1600x900 for better detail
        self.rows = rows
        self.cols = cols
        self.window_size = window_size
        self.animate = animate
        self.running = True
        self.paused = False
        
        # Initialize components
        self.maze_structure = MazeStructure(rows, cols)
        self.maze_generator = MazeGenerator(self.maze_structure)
        self.path_solver = PathSolver(self.maze_structure)
        self.right_hand_solver = RightHandSolver(self.maze_structure)
        
        # Initialize rendering and UI
        self.renderer = GameRenderer(window_size, self.maze_structure)
        self.timer_display = TimerDisplay(window_size)
        
        # Game state
        self.current_phase = "generation"  # "generation", "path_solving", "right_hand", "complete"
        self.animation_speed = animation_speed  # Use configurable animation speed
        self.last_step_time = 0
        
        # Robot state
        self.current_robot_pos = None
        self.current_robot_direction = "down"
        
        # Timing data
        self.generation_start_time = None
        self.generation_end_time = None
        self.path_solving_start_time = None
        self.path_solving_end_time = None
        self.right_hand_start_time = None
        self.right_hand_end_time = None
        
        # UI state
        self.show_ending_screen = False
        
        pygame.init()
        
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
        else: return self.current_robot_direction  # no movement

    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.show_ending_screen:
                        self.running = False  # Exit on space when showing ending screen
                    else:
                        self._skip_current_phase()
                elif event.key == pygame.K_RETURN:
                    if not self.show_ending_screen:
                        self.paused = not self.paused

    def _skip_current_phase(self):
        """Skip the current animation phase"""
        if self.current_phase == "generation":
            # Complete maze generation instantly
            self.maze_generator.create_maze_instantly()
            self._end_generation_phase()
        elif self.current_phase == "path_solving":
            # Complete path solving instantly
            while not self.path_solver.is_complete():
                self.path_solver.step_solve()
            self._end_path_solving_phase()
        elif self.current_phase == "right_hand":
            # Complete right-hand solving instantly
            while not self.right_hand_solver.is_complete():
                self.right_hand_solver.step_solve()
            self._end_right_hand_phase()

    def _start_generation_phase(self):
        """Start the maze generation phase"""
        self.current_phase = "generation"
        self.generation_start_time = time.time()
        self.timer_display.start_generation_timer()
        self.maze_generator.start_generation()
        self.current_robot_pos = self.maze_generator.get_current_position()

    def _end_generation_phase(self):
        """End the maze generation phase and start path solving"""
        self.generation_end_time = time.time()
        self.timer_display.end_generation_timer()
        
        # Pass the solution path from maze generator to path solver
        solution_path = self.maze_generator.get_solution_path()
        self.path_solver.set_solution_path(solution_path)
        
        self._start_path_solving_phase()

    def _start_path_solving_phase(self):
        """Start the path solving phase"""
        self.current_phase = "path_solving"
        self.path_solving_start_time = time.time()
        self.timer_display.start_path_solving_timer()
        self.path_solver.start_solving()
        self.current_robot_pos = self.path_solver.get_current_position()

    def _end_path_solving_phase(self):
        """End the path solving phase and start right-hand solving"""
        self.path_solving_end_time = time.time()
        self.timer_display.end_path_solving_timer()
        self._start_right_hand_phase()

    def _start_right_hand_phase(self):
        """Start the right-hand solving phase"""
        self.current_phase = "right_hand"
        self.right_hand_start_time = time.time()
        self.timer_display.start_right_hand_timer()
        
        # Clear the yellow trail before starting right-hand solving
        if hasattr(self.path_solver, 'clear_path'):
            self.path_solver.clear_path()
        
        self.right_hand_solver.start_solving()
        self.current_robot_pos = self.right_hand_solver.get_current_position()

    def _end_right_hand_phase(self):
        """End the right-hand solving phase"""
        self.right_hand_end_time = time.time()
        self.timer_display.end_right_hand_timer()
        self.current_phase = "complete"
        self.show_ending_screen = True

    def _update_animation(self, current_time):
        """Update animation step"""
        if (not self.animate or self.paused or self.show_ending_screen or 
            current_time - self.last_step_time < self.animation_speed):
            return
            
        prev_pos = self.current_robot_pos
        
        if self.current_phase == "generation":
            continuing = self.maze_generator.step_generation()
            self.current_robot_pos = self.maze_generator.get_current_position()
            
            if not continuing:
                self._end_generation_phase()
                
        elif self.current_phase == "path_solving":
            continuing = self.path_solver.step_solve()
            self.current_robot_pos = self.path_solver.get_current_position()
            
            if not continuing:
                self._end_path_solving_phase()
                    
        elif self.current_phase == "right_hand":
            continuing = self.right_hand_solver.step_solve()
            self.current_robot_pos = self.right_hand_solver.get_current_position()
            
            # Update direction for right-hand solver
            if hasattr(self.right_hand_solver, 'get_current_direction_name'):
                self.current_robot_direction = self.right_hand_solver.get_current_direction_name()
            
            if not continuing:
                self._end_right_hand_phase()
        
        # Update robot direction for generation and path solving
        if self.current_phase in ["generation", "path_solving"]:
            if self.current_robot_pos and prev_pos:
                new_direction = self._get_direction(prev_pos, self.current_robot_pos)
                if self.current_robot_pos == self.maze_structure.get_end():
                    self.current_robot_direction = "right"
                else:
                    self.current_robot_direction = new_direction
        
        self.last_step_time = current_time

    def _render_frame(self):
        """Render one frame of the game"""
        self.renderer.clear_screen()
        
        if self.show_ending_screen:
            self._render_ending_screen()
        else:
            # Get current paths for rendering - only yellow path if not in right-hand phase
            if self.current_phase == "right_hand":
                path_solver_path = []  # Clear yellow trail during right-hand solving
            else:
                path_solver_path = self.path_solver.get_current_path() if self.current_phase != "generation" else []
            
            right_hand_path = self.right_hand_solver.get_current_path() if self.current_phase == "right_hand" or self.current_phase == "complete" else []
            
            # Draw maze with paths
            self.renderer.draw_maze(path_solver_path, right_hand_path)
            
            # Draw robot if we have a position and not complete
            if self.current_robot_pos and self.current_phase != "complete":
                self.renderer.draw_robot(self.current_robot_pos, self.current_robot_direction)
            elif self.current_phase == "complete" and self.current_robot_pos == self.maze_structure.get_end():
                # Keep robot at exit when complete
                self.renderer.draw_robot(self.current_robot_pos, "right")
            
            # Draw UI elements
            self._draw_ui_elements()
        
        self.renderer.update_display()

    def _draw_ui_elements(self):
        """Draw UI elements based on current phase"""
        # Algorithm info (top left)
        self._draw_algorithm_info()
        
        # Timer (top right)
        self._draw_current_timer()

    def _draw_algorithm_info(self):
        """Draw current algorithm information"""
        font = pygame.font.Font(None, 28)  # Slightly larger font
        
        if self.current_phase == "generation":
            text = "Drilling Maze (DFS Algorithm)"
            color = (255, 255, 255)  # White
        elif self.current_phase == "path_solving":
            text = "Solving with Path Data"
            color = (255, 255, 0)   # Yellow
        elif self.current_phase == "right_hand":
            text = "Right-Hand Wall Following"
            color = (0, 150, 255)   # Blue
        else:
            text = "All Simulations Complete"
            color = (0, 255, 0)     # Green
        
        # Create semi-transparent background for text readability
        surface = font.render(text, True, color)
        bg_surface = pygame.Surface((surface.get_width() + 20, surface.get_height() + 10))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(180)  # Semi-transparent black background
        
        self.renderer.get_screen().blit(bg_surface, (10, 10))
        self.renderer.get_screen().blit(surface, (20, 15))  # Text on top of background

    def _draw_current_timer(self):
        """Draw the timer for the current phase"""
        font = pygame.font.Font(None, 28)  # Slightly larger font
        
        if self.current_phase == "generation":
            elapsed = time.time() - self.generation_start_time
            text = f"Time: {elapsed:.1f}s"
            color = (255, 255, 255)  # White
        elif self.current_phase == "path_solving":
            elapsed = time.time() - self.path_solving_start_time
            text = f"Time: {elapsed:.1f}s"
            color = (255, 255, 0)   # Yellow
        elif self.current_phase == "right_hand":
            elapsed = time.time() - self.right_hand_start_time
            text = f"Time: {elapsed:.1f}s"
            color = (0, 150, 255)   # Blue
        else:
            return  # No timer for complete phase
        
        surface = font.render(text, True, color)
        
        # Create semi-transparent background for text readability
        bg_surface = pygame.Surface((surface.get_width() + 20, surface.get_height() + 10))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(180)  # Semi-transparent black background
        
        # Position at top right with background
        rect = surface.get_rect()
        rect.topright = (self.window_size[0] - 20, 10)
        bg_rect = bg_surface.get_rect()
        bg_rect.topright = (self.window_size[0] - 10, 10)
        
        self.renderer.get_screen().blit(bg_surface, bg_rect)
        self.renderer.get_screen().blit(surface, rect)

    def _render_ending_screen(self):
        """Render the ending screen with comparison data"""
        # Create semi-transparent overlay
        overlay = pygame.Surface(self.window_size)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        
        # Draw blurred background (maze)
        path_solver_path = self.path_solver.get_current_path()
        right_hand_path = self.right_hand_solver.get_current_path()
        self.renderer.draw_maze(path_solver_path, right_hand_path)
        
        # Apply overlay
        self.renderer.get_screen().blit(overlay, (0, 0))
        
        # Calculate timings
        generation_time = self.generation_end_time - self.generation_start_time
        path_solving_time = self.path_solving_end_time - self.path_solving_start_time
        right_hand_time = self.right_hand_end_time - self.right_hand_start_time
        
        dfs_total = generation_time + path_solving_time
        right_hand_total = generation_time + right_hand_time
        
        # Font definitions
        font_title = pygame.font.Font(None, 48)
        font_data = pygame.font.Font(None, 32)
        font_header = pygame.font.Font(None, 36)
        font_generation = pygame.font.Font(None, 34)
        
        center_x = self.window_size[0] // 2
        
        # Title at top center
        title = font_title.render("Maze Solving Comparison", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 80))
        self.renderer.get_screen().blit(title, title_rect)
        
        # Maze generation time in center (shared by both algorithms)
        generation_text = f"Maze Generation: {generation_time:.2f}s"
        generation_surface = font_generation.render(generation_text, True, (200, 200, 200))
        generation_rect = generation_surface.get_rect(center=(center_x, 140))
        self.renderer.get_screen().blit(generation_surface, generation_rect)
        
        # Two column layout for algorithm-specific data
        # Apply centered columns for all resolutions for better visual balance
        if self.window_size[0] >= 1600:  # Ultra HD and high quality
            left_x = self.window_size[0] // 2 - 250  # Closer to center
            right_x = self.window_size[0] // 2 + 250  # Closer to center
        elif self.window_size[0] >= 1280:  # Standard HD
            left_x = self.window_size[0] // 2 - 200  # Centered for standard
            right_x = self.window_size[0] // 2 + 200  # Centered for standard
        else:  # Performance - smaller spacing for smaller screens
            left_x = self.window_size[0] // 2 - 150  # Centered for small screens
            right_x = self.window_size[0] // 2 + 150  # Centered for small screens
        start_y = 200
        line_height = 40
        
        # Left column - Right Wall Algorithm
        left_header = font_header.render("Right Wall Algorithm", True, (0, 150, 255))
        left_header_rect = left_header.get_rect(center=(left_x, start_y))
        self.renderer.get_screen().blit(left_header, left_header_rect)
        
        # Left column data (only algorithm-specific info)
        left_data = [
            f"Right Wall Solving: {right_hand_time:.2f}s",
            f"Total Time: {right_hand_total:.2f}s",
            "",
            "Time Complexity: O(M×N)",
            "Space Complexity: O(1)"
        ]
        
        for i, line in enumerate(left_data):
            surface = font_data.render(line, True, (255, 255, 255))
            surface_rect = surface.get_rect(center=(left_x, start_y + 50 + i * line_height))
            self.renderer.get_screen().blit(surface, surface_rect)
        
        # Right column - DFS Path Algorithm
        right_header = font_header.render("DFS Path Algorithm", True, (255, 255, 0))
        right_header_rect = right_header.get_rect(center=(right_x, start_y))
        self.renderer.get_screen().blit(right_header, right_header_rect)
        
        # Right column data (only algorithm-specific info)
        right_data = [
            f"Path Solving: {path_solving_time:.2f}s",
            f"Total Time: {dfs_total:.2f}s",
            "",
            "Time Complexity: O(M×N)",
            "Space Complexity: O(V)"
        ]
        
        for i, line in enumerate(right_data):
            surface = font_data.render(line, True, (255, 255, 255))
            surface_rect = surface.get_rect(center=(right_x, start_y + 50 + i * line_height))
            self.renderer.get_screen().blit(surface, surface_rect)
        
        # Speed comparison in center
        analysis_y = start_y + 280
        time_difference = abs(right_hand_total - dfs_total)
        
        if right_hand_total < dfs_total:
            faster_text = f"Right Wall Algorithm is faster by {time_difference:.2f}s"
            faster_color = (0, 150, 255)
            analysis_text = f"({time_difference/dfs_total*100:.1f}% improvement)"
        elif dfs_total < right_hand_total:
            faster_text = f"DFS Path Algorithm is faster by {time_difference:.2f}s"
            faster_color = (255, 255, 0)
            analysis_text = f"({time_difference/right_hand_total*100:.1f}% improvement)"
        else:
            faster_text = "Both algorithms completed in equal time!"
            faster_color = (255, 255, 255)
            analysis_text = "Perfect tie - remarkable!"
        
        # Main comparison text centered
        faster_surface = font_title.render(faster_text, True, faster_color)
        faster_rect = faster_surface.get_rect(center=(center_x, analysis_y))
        self.renderer.get_screen().blit(faster_surface, faster_rect)
        
        # Additional analysis centered
        analysis_surface = font_data.render(analysis_text, True, (200, 200, 200))
        analysis_rect = analysis_surface.get_rect(center=(center_x, analysis_y + 40))
        self.renderer.get_screen().blit(analysis_surface, analysis_rect)
        
        # Exit instruction at bottom center
        exit_text = "Press SPACE to exit"
        exit_surface = font_data.render(exit_text, True, (200, 200, 200))
        exit_rect = exit_surface.get_rect(center=(center_x, analysis_y + 100))
        self.renderer.get_screen().blit(exit_surface, exit_rect)

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        # Start the first phase
        self._start_generation_phase()
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            self._handle_events()
            
            # Update animation
            self._update_animation(current_time)
            
            # Render frame
            self._render_frame()
            
            clock.tick(60)

        pygame.quit()
