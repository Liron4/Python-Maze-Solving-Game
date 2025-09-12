"""
TimerDisplay - Handles timer display for different simulation phases.
Follows Single Responsibility Principle - only handles timer UI.
"""
import pygame
import time


class TimerDisplay:
    """Displays timers for different maze simulation phases."""
    
    def __init__(self, window_size, ui_font_size=28):
        self.window_size = window_size
        self.ui_font_size = ui_font_size
        self.font = pygame.font.Font(None, ui_font_size)
        
        # Timer states
        self.generation_start_time = None
        self.generation_time = 0
        self.generation_paused_time = 0  # Accumulated paused time
        self.path_solving_start_time = None
        self.path_solving_time = 0
        self.path_solving_paused_time = 0  # Accumulated paused time
        self.right_hand_start_time = None
        self.right_hand_time = 0
        self.right_hand_paused_time = 0  # Accumulated paused time
        
        # Pause state
        self.is_paused = False
        self.pause_start_time = None
        
        # Current phase
        self.current_phase = None
        
    def start_generation_timer(self):
        """Start timing the maze generation phase"""
        self.generation_start_time = time.time()
        self.current_phase = "generation"
        
    def end_generation_timer(self):
        """End timing the maze generation phase"""
        if self.generation_start_time:
            self.generation_time = time.time() - self.generation_start_time - self.generation_paused_time
            self.generation_start_time = None
    
    def start_path_solving_timer(self):
        """Start timing the path solving phase"""
        self.path_solving_start_time = time.time()
        self.current_phase = "path_solving"
        
    def end_path_solving_timer(self):
        """End timing the path solving phase"""
        if self.path_solving_start_time:
            self.path_solving_time = time.time() - self.path_solving_start_time - self.path_solving_paused_time
            self.path_solving_start_time = None
    
    def start_right_hand_timer(self):
        """Start timing the right-hand solving phase"""
        self.right_hand_start_time = time.time()
        self.current_phase = "right_hand"
        
    def end_right_hand_timer(self):
        """End timing the right-hand solving phase"""
        if self.right_hand_start_time:
            self.right_hand_time = time.time() - self.right_hand_start_time - self.right_hand_paused_time
            self.right_hand_start_time = None
    
    def pause_timer(self):
        """Pause the current timer"""
        if not self.is_paused:
            self.is_paused = True
            self.pause_start_time = time.time()
    
    def resume_timer(self):
        """Resume the current timer"""
        if self.is_paused and self.pause_start_time:
            pause_duration = time.time() - self.pause_start_time
            
            # Add pause duration to the appropriate phase
            if self.current_phase == "generation":
                self.generation_paused_time += pause_duration
            elif self.current_phase == "path_solving":
                self.path_solving_paused_time += pause_duration
            elif self.current_phase == "right_hand":
                self.right_hand_paused_time += pause_duration
            
            self.is_paused = False
            self.pause_start_time = None
    
    def get_current_time(self):
        """Get the current elapsed time for the active phase"""
        current_time = time.time()
        current_pause_time = 0
        
        # If currently paused, calculate current pause duration
        if self.is_paused and self.pause_start_time:
            current_pause_time = current_time - self.pause_start_time
        
        if self.current_phase == "generation" and self.generation_start_time:
            return current_time - self.generation_start_time - self.generation_paused_time - current_pause_time
        elif self.current_phase == "path_solving" and self.path_solving_start_time:
            return current_time - self.path_solving_start_time - self.path_solving_paused_time - current_pause_time
        elif self.current_phase == "right_hand" and self.right_hand_start_time:
            return current_time - self.right_hand_start_time - self.right_hand_paused_time - current_pause_time
        
        return 0
    
    def draw_current_timer(self, screen):
        """Draw the timer for the current phase in top right corner"""
        if self.current_phase == "generation" and self.generation_start_time:
            elapsed = self.get_current_time()  # Use the pause-aware method
            text = f"Time: {elapsed:.1f}s"
            color = (255, 255, 255)  # White
        elif self.current_phase == "path_solving" and self.path_solving_start_time:
            elapsed = self.get_current_time()  # Use the pause-aware method
            text = f"Time: {elapsed:.1f}s"
            color = (255, 255, 0)   # Yellow
        elif self.current_phase == "right_hand" and self.right_hand_start_time:
            elapsed = self.get_current_time()  # Use the pause-aware method
            text = f"Time: {elapsed:.1f}s"
            color = (0, 150, 255)   # Blue
        else:
            return  # No timer for complete phase
        
        surface = self.font.render(text, True, color)
        
        # Create semi-transparent background for text readability
        bg_surface = pygame.Surface((surface.get_width() + 20, surface.get_height() + 10))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(180)  # Semi-transparent black background
        
        # Position at top right with background
        rect = surface.get_rect()
        rect.topright = (self.window_size[0] - 20, 10)
        bg_rect = bg_surface.get_rect()
        bg_rect.topright = (self.window_size[0] - 10, 10)
        
        screen.blit(bg_surface, bg_rect)
        screen.blit(surface, rect)
    
    def draw_algorithm_info(self, screen, current_phase):
        """Draw current algorithm information in top left corner"""
        if current_phase == "generation":
            text = "Drilling Maze (DFS Algorithm)"
            color = (255, 255, 255)  # White
        elif current_phase == "path_solving":
            text = "Solving with Path Data"
            color = (255, 255, 0)   # Yellow
        elif current_phase == "right_hand":
            text = "Right-Hand Wall Following"
            color = (0, 150, 255)   # Blue
        else:
            text = "All Simulations Complete"
            color = (0, 255, 0)     # Green
        
        # Create semi-transparent background for text readability
        surface = self.font.render(text, True, color)
        bg_surface = pygame.Surface((surface.get_width() + 20, surface.get_height() + 10))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(180)  # Semi-transparent black background
        
        screen.blit(bg_surface, (10, 10))
        screen.blit(surface, (20, 15))  # Text on top of background
