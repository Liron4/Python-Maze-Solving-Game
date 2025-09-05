"""
PathSolver - Uses pre-computed optimal path to solve the maze.
Follows Single Responsibility Principle - only handles path-based solving.
"""


class PathSolver:
    """Solves maze using a pre-computed optimal path (from DFS generation)."""
    
    def __init__(self, maze_structure):
        self.maze_structure = maze_structure
        self.solution_path = []
        self.current_step = 0
        self.solving_complete = False
        self.current_pos = None
        
    def set_solution_path(self, path):
        """Set the solution path to follow"""
        self.solution_path = path
        self.current_step = 0
        self.solving_complete = False
        
    def start_solving(self):
        """Initialize solving phase"""
        self.current_step = 0
        self.solving_complete = False
        self.current_pos = self.maze_structure.get_start()
        
    def step_solve(self):
        """Perform one step of path following. Returns True if continuing, False if complete."""
        if not self.solution_path:
            # No solution path available
            self.solving_complete = True
            return False
            
        if self.current_step >= len(self.solution_path):
            self.solving_complete = True
            return False
        
        # Move robot along the solution path
        self.current_pos = self.solution_path[self.current_step]
        self.current_step += 1
        
        return True
    
    def get_current_path(self):
        """Return the path traced so far"""
        if self.current_step > 0:
            return self.solution_path[:self.current_step]
        return []
    
    def clear_path(self):
        """Clear the current path display"""
        self.current_step = 0
    
    def is_complete(self):
        """Check if solving is complete"""
        return self.solving_complete
        
    def get_current_position(self):
        """Return current position"""
        return self.current_pos
