"""
EndingScreenRenderer - Handles the complex ending screen with comparison data.
Follows Single Responsibility Principle - only handles ending screen rendering.
"""
import pygame


class EndingScreenRenderer:
    """Handles rendering of the ending screen with algorithm comparison data."""
    
    def __init__(self, window_size):
        self.window_size = window_size
        
    def render(self, screen, path_solver, right_hand_solver, timer_display):
        """Render the ending screen with comparison data"""
        # Create semi-transparent overlay
        overlay = pygame.Surface(self.window_size)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        
        # Apply overlay
        screen.blit(overlay, (0, 0))
        
        # Get timing data from timer_display
        generation_time = timer_display.generation_time
        path_solving_time = timer_display.path_solving_time
        right_hand_time = timer_display.right_hand_time
        
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
        screen.blit(title, title_rect)
        
        # Maze generation time in center (shared by both algorithms)
        generation_text = f"Maze Generation: {generation_time:.2f}s"
        generation_surface = font_generation.render(generation_text, True, (200, 200, 200))
        generation_rect = generation_surface.get_rect(center=(center_x, 140))
        screen.blit(generation_surface, generation_rect)
        
        # Calculate column positions based on screen size
        left_x, right_x = self._calculate_column_positions()
        start_y = 200
        line_height = 40
        
        # Render algorithm columns
        self._render_algorithm_column(screen, font_header, font_data, 
                                    "Right Wall Algorithm", (0, 150, 255),
                                    left_x, start_y, line_height,
                                    right_hand_time, right_hand_total)
        
        self._render_algorithm_column(screen, font_header, font_data,
                                    "DFS Path Algorithm", (255, 255, 0),
                                    right_x, start_y, line_height,
                                    path_solving_time, dfs_total)
        
        # Render comparison analysis
        self._render_comparison_analysis(screen, font_title, font_data,
                                       center_x, start_y + 280,
                                       dfs_total, right_hand_total)
        
    def _calculate_column_positions(self):
        """Calculate left and right column positions based on screen size"""
        if self.window_size[0] >= 1600:  # Ultra HD and high quality
            left_x = self.window_size[0] // 2 - 250
            right_x = self.window_size[0] // 2 + 250
        elif self.window_size[0] >= 1280:  # Standard HD
            left_x = self.window_size[0] // 2 - 200
            right_x = self.window_size[0] // 2 + 200
        else:  # Performance - smaller spacing for smaller screens
            left_x = self.window_size[0] // 2 - 150
            right_x = self.window_size[0] // 2 + 150
        return left_x, right_x
    
    def _render_algorithm_column(self, screen, font_header, font_data, 
                               algorithm_name, color, x_pos, start_y, line_height,
                               solving_time, total_time):
        """Render a single algorithm column"""
        # Header
        header = font_header.render(algorithm_name, True, color)
        header_rect = header.get_rect(center=(x_pos, start_y))
        screen.blit(header, header_rect)
        
        # Data
        if "Right Wall" in algorithm_name:
            data = [
                f"Right Wall Solving: {solving_time:.2f}s",
                f"Total Time: {total_time:.2f}s",
                "",
                "Time Complexity: O(M×N)",
                "Space Complexity: O(1)"
            ]
        else:  # DFS Path
            data = [
                f"Path Solving: {solving_time:.2f}s",
                f"Total Time: {total_time:.2f}s",
                "",
                "Time Complexity: O(M×N)",
                "Space Complexity: O(V)"
            ]
        
        for i, line in enumerate(data):
            surface = font_data.render(line, True, (255, 255, 255))
            surface_rect = surface.get_rect(center=(x_pos, start_y + 50 + i * line_height))
            screen.blit(surface, surface_rect)
    
    def _render_comparison_analysis(self, screen, font_title, font_data,
                                  center_x, analysis_y, dfs_total, right_hand_total):
        """Render the speed comparison analysis"""
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
        screen.blit(faster_surface, faster_rect)
        
        # Additional analysis centered
        analysis_surface = font_data.render(analysis_text, True, (200, 200, 200))
        analysis_rect = analysis_surface.get_rect(center=(center_x, analysis_y + 40))
        screen.blit(analysis_surface, analysis_rect)
        
        # Exit instruction at bottom center
        exit_text = "Press SPACE to exit"
        exit_surface = font_data.render(exit_text, True, (200, 200, 200))
        exit_rect = exit_surface.get_rect(center=(center_x, analysis_y + 100))
        screen.blit(exit_surface, exit_rect)
