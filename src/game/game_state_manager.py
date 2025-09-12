"""
GameStateManager - Handles game phase transitions and coordination.
Follows Single Responsibility Principle - only handles state management.
"""
import time


class GameStateManager:
    """Manages game phases and coordinates transitions between different simulation stages."""
    
    def __init__(self, maze_generator, path_solver, right_hand_solver, timer_display):
        self.maze_generator = maze_generator
        self.path_solver = path_solver
        self.right_hand_solver = right_hand_solver
        self.timer_display = timer_display
        
        # Game state
        self.current_phase = "generation"  # "generation", "path_solving", "right_hand", "complete"
        self.show_ending_screen = False
        
        # Robot state
        self.current_robot_pos = None
        self.current_robot_direction = "down"
    
    def start_generation_phase(self):
        """Start the maze generation phase"""
        self.current_phase = "generation"
        self.timer_display.start_generation_timer()
        self.maze_generator.start_generation()
        self.current_robot_pos = self.maze_generator.get_current_position()

    def end_generation_phase(self):
        """End the maze generation phase and start path solving"""
        self.timer_display.end_generation_timer()
        
        # Pass the solution path from maze generator to path solver
        solution_path = self.maze_generator.get_solution_path()
        self.path_solver.set_solution_path(solution_path)
        
        self.start_path_solving_phase()

    def start_path_solving_phase(self):
        """Start the path solving phase"""
        self.current_phase = "path_solving"
        self.timer_display.start_path_solving_timer()
        self.path_solver.start_solving()
        self.current_robot_pos = self.path_solver.get_current_position()

    def end_path_solving_phase(self):
        """End the path solving phase and start right-hand solving"""
        self.timer_display.end_path_solving_timer()
        self.start_right_hand_phase()

    def start_right_hand_phase(self):
        """Start the right-hand solving phase"""
        self.current_phase = "right_hand"
        self.timer_display.start_right_hand_timer()
        
        # Clear the yellow trail before starting right-hand solving
        if hasattr(self.path_solver, 'clear_path'):
            self.path_solver.clear_path()
        
        self.right_hand_solver.start_solving()
        self.current_robot_pos = self.right_hand_solver.get_current_position()

    def end_right_hand_phase(self):
        """End the right-hand solving phase"""
        self.timer_display.end_right_hand_timer()
        self.current_phase = "complete"
        self.show_ending_screen = True
    
    def skip_current_phase(self):
        """Skip the current animation phase"""
        if self.current_phase == "generation":
            # Complete maze generation instantly
            self.maze_generator.create_maze_instantly()
            self.end_generation_phase()
        elif self.current_phase == "path_solving":
            # Complete path solving instantly
            while not self.path_solver.is_complete():
                self.path_solver.step_solve()
            self.end_path_solving_phase()
        elif self.current_phase == "right_hand":
            # Complete right-hand solving instantly
            while not self.right_hand_solver.is_complete():
                self.right_hand_solver.step_solve()
            self.end_right_hand_phase()
    
    def update_animation_step(self):
        """Update one animation step and return whether to continue"""
        prev_pos = self.current_robot_pos
        
        if self.current_phase == "generation":
            continuing = self.maze_generator.step_generation()
            self.current_robot_pos = self.maze_generator.get_current_position()
            
            if not continuing:
                self.end_generation_phase()
                
        elif self.current_phase == "path_solving":
            continuing = self.path_solver.step_solve()
            self.current_robot_pos = self.path_solver.get_current_position()
            
            if not continuing:
                self.end_path_solving_phase()
                    
        elif self.current_phase == "right_hand":
            continuing = self.right_hand_solver.step_solve()
            self.current_robot_pos = self.right_hand_solver.get_current_position()
            
            # Update direction for right-hand solver
            if hasattr(self.right_hand_solver, 'get_current_direction_name'):
                self.current_robot_direction = self.right_hand_solver.get_current_direction_name()
            
            if not continuing:
                self.end_right_hand_phase()
        
        return prev_pos
    
    def get_current_paths(self):
        """Get the current solution paths for rendering"""
        # Get current paths for rendering - only yellow path if not in right-hand phase
        if self.current_phase == "right_hand":
            path_solver_path = []  # Clear yellow trail during right-hand solving
        else:
            path_solver_path = self.path_solver.get_current_path() if self.current_phase != "generation" else []
        
        right_hand_path = self.right_hand_solver.get_current_path() if self.current_phase == "right_hand" or self.current_phase == "complete" else []
        
        return path_solver_path, right_hand_path
