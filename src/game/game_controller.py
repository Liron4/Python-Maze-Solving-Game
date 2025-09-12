"""
GameController - Main game loop and event handling.
Follows Single Responsibility Principle - only handles game loop and input.
"""
import pygame
import time
from maze.maze_generator import MazeGenerator
from maze.maze_structure import MazeStructure
from solvers.path_solver import PathSolver
from solvers.right_hand_solver import RightHandSolver
from game.game_renderer import GameRenderer
from game.timer_display import TimerDisplay
from game.game_state_manager import GameStateManager


class GameController:
    """Controls the main game loop and handles user input."""
    
    def __init__(self, rows, cols, window_size=(1600, 900), animation_speed=25, ui_font_size=28, animate=True):
        self.rows = rows
        self.cols = cols
        self.window_size = window_size
        self.animate = animate
        self.running = True
        self.paused = False
        self.animation_speed = animation_speed
        self.last_step_time = 0
        
        # Initialize components
        self.maze_structure = MazeStructure(rows, cols)
        self.maze_generator = MazeGenerator(self.maze_structure)
        self.path_solver = PathSolver(self.maze_structure)
        self.right_hand_solver = RightHandSolver(self.maze_structure)
        
        # Initialize rendering and UI
        self.renderer = GameRenderer(window_size, self.maze_structure, ui_font_size)
        self.timer_display = TimerDisplay(window_size, ui_font_size)
        
        # Initialize state manager
        self.state_manager = GameStateManager(
            self.maze_generator, self.path_solver, 
            self.right_hand_solver, self.timer_display
        )
        
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
        else: return self.state_manager.current_robot_direction  # no movement

    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state_manager.show_ending_screen:
                        self.running = False  # Exit on space when showing ending screen
                    else:
                        self.state_manager.skip_current_phase()
                elif event.key == pygame.K_RETURN:
                    if not self.state_manager.show_ending_screen:
                        self.paused = not self.paused
                        # Pause/resume timer as well
                        if self.paused:
                            self.timer_display.pause_timer()
                        else:
                            self.timer_display.resume_timer()

    def _update_animation(self, current_time):
        """Update animation step"""
        if (not self.animate or self.paused or self.state_manager.show_ending_screen or 
            current_time - self.last_step_time < self.animation_speed):
            return
            
        prev_pos = self.state_manager.update_animation_step()
        
        # Update robot direction for generation and path solving
        if self.state_manager.current_phase in ["generation", "path_solving"]:
            if self.state_manager.current_robot_pos and prev_pos:
                new_direction = self._get_direction(prev_pos, self.state_manager.current_robot_pos)
                if self.state_manager.current_robot_pos == self.maze_structure.get_end():
                    self.state_manager.current_robot_direction = "right"
                else:
                    self.state_manager.current_robot_direction = new_direction
        
        self.last_step_time = current_time

    def _render_frame(self):
        """Render one frame of the game"""
        self.renderer.clear_screen()
        
        if self.state_manager.show_ending_screen:
            self.renderer.render_ending_screen(
                self.path_solver, self.right_hand_solver, self.timer_display
            )
        else:
            # Get current paths for rendering
            path_solver_path, right_hand_path = self.state_manager.get_current_paths()
            
            # Draw maze with paths
            self.renderer.draw_maze(path_solver_path, right_hand_path)
            
            # Draw robot if we have a position and not complete
            if self.state_manager.current_robot_pos and self.state_manager.current_phase != "complete":
                self.renderer.draw_robot(self.state_manager.current_robot_pos, self.state_manager.current_robot_direction)
            elif self.state_manager.current_phase == "complete" and self.state_manager.current_robot_pos == self.maze_structure.get_end():
                # Keep robot at exit when complete
                self.renderer.draw_robot(self.state_manager.current_robot_pos, "right")
            
            # Draw UI elements using the timer display
            self.renderer.draw_ui_elements(self.timer_display, self.state_manager.current_phase)
        
        self.renderer.update_display()

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        # Start the first phase
        self.state_manager.start_generation_phase()
        
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
