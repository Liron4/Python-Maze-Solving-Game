"""
TimerDisplay - Handles timer display for different simulation phases.
Follows Single Responsibility Principle - only handles timer UI.
"""
import pygame
import time


class TimerDisplay:
    """Displays timers for different maze simulation phases."""
    
    def __init__(self, window_size):
        self.window_size = window_size
        self.font = pygame.font.Font(None, 36)
        
        # Timer states
        self.generation_start_time = None
        self.generation_time = 0
        self.path_solving_start_time = None
        self.path_solving_time = 0
        self.right_hand_start_time = None
        self.right_hand_time = 0
        
        # Current phase
        self.current_phase = None
        
    def start_generation_timer(self):
        """Start timing the maze generation phase"""
        self.generation_start_time = time.time()
        self.current_phase = "generation"
        
    def end_generation_timer(self):
        """End timing the maze generation phase"""
        if self.generation_start_time:
            self.generation_time = time.time() - self.generation_start_time
            self.generation_start_time = None
    
    def start_path_solving_timer(self):
        """Start timing the path solving phase"""
        self.path_solving_start_time = time.time()
        self.current_phase = "path_solving"
        
    def end_path_solving_timer(self):
        """End timing the path solving phase"""
        if self.path_solving_start_time:
            self.path_solving_time = time.time() - self.path_solving_start_time
            self.path_solving_start_time = None
    
    def start_right_hand_timer(self):
        """Start timing the right-hand solving phase"""
        self.right_hand_start_time = time.time()
        self.current_phase = "right_hand"
        
    def end_right_hand_timer(self):
        """End timing the right-hand solving phase"""
        if self.right_hand_start_time:
            self.right_hand_time = time.time() - self.right_hand_start_time
            self.right_hand_start_time = None
    
    def get_current_time(self):
        """Get the current elapsed time for the active phase"""
        current_time = time.time()
        
        if self.current_phase == "generation" and self.generation_start_time:
            return current_time - self.generation_start_time
        elif self.current_phase == "path_solving" and self.path_solving_start_time:
            return current_time - self.path_solving_start_time
        elif self.current_phase == "right_hand" and self.right_hand_start_time:
            return current_time - self.right_hand_start_time
        
        return 0
    
    def draw_timers(self, screen):
        """Draw all timer displays in the top-right corner"""
        x_start = self.window_size[0] - 250  # Right side with some padding
        y_start = 10
        line_height = 40
        
        # Generation timer (White)
        if self.current_phase == "generation":
            current_gen_time = self.get_current_time()
            gen_text = f"Generation: {current_gen_time:.1f}s"
        else:
            gen_text = f"Generation: {self.generation_time:.1f}s"
        
        gen_surface = self.font.render(gen_text, True, (255, 255, 255))  # White
        screen.blit(gen_surface, (x_start, y_start))
        
        # Path solving timer (Yellow)
        if self.path_solving_time > 0 or self.current_phase == "path_solving":
            if self.current_phase == "path_solving":
                current_path_time = self.get_current_time()
                path_text = f"Path Solve: {current_path_time:.1f}s"
            else:
                path_text = f"Path Solve: {self.path_solving_time:.1f}s"
            
            path_surface = self.font.render(path_text, True, (255, 255, 0))  # Yellow
            screen.blit(path_surface, (x_start, y_start + line_height))
        
        # Right-hand timer (Blue)
        if self.right_hand_time > 0 or self.current_phase == "right_hand":
            if self.current_phase == "right_hand":
                current_rh_time = self.get_current_time()
                rh_text = f"Right-Hand: {current_rh_time:.1f}s"
            else:
                rh_text = f"Right-Hand: {self.right_hand_time:.1f}s"
            
            rh_surface = self.font.render(rh_text, True, (0, 100, 255))  # Blue
            screen.blit(rh_surface, (x_start, y_start + 2 * line_height))
