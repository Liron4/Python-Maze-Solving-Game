"""
RightHandSolver - Implements right-hand wall following algorithm.
Follows Single Responsibility Principle - only handles right-hand maze solving.
"""


class RightHandSolver:
    """Solves maze using right-hand wall following algorithm."""
    
    def __init__(self, maze_structure):
        self.maze_structure = maze_structure
        self.current_pos = None
        self.current_direction = 0  # 0=North, 1=East, 2=South, 3=West
        self.path_taken = []
        self.solving_complete = False
        self.visited_positions = set()
        
        # Direction vectors: North, East, South, West
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.direction_names = ["up", "right", "down", "left"]
        
    def start_solving(self):
        """Initialize right-hand solving from start position"""
        self.current_pos = self.maze_structure.get_start()
        self.current_direction = 1  # Start facing East (towards the maze)
        self.path_taken = [self.current_pos]
        self.solving_complete = False
        self.visited_positions = {self.current_pos}
        
    def step_solve(self):
        """Perform one step of right-hand wall following. Returns True if continuing, False if complete."""
        if self.solving_complete:
            return False
            
        if self.current_pos == self.maze_structure.get_end():
            self.solving_complete = True
            return False
            
        # Optimization: Check if exit is directly adjacent and reachable
        if self._is_exit_adjacent():
            exit_pos = self.maze_structure.get_end()
            self.current_pos = exit_pos
            self.path_taken.append(exit_pos)
            self.solving_complete = True
            return False
            
        # Right-hand wall following algorithm
        next_pos, next_direction = self._get_next_move()
        
        if next_pos:
            self.current_pos = next_pos
            self.current_direction = next_direction
            self.path_taken.append(next_pos)
            self.visited_positions.add(next_pos)
        else:
            # This shouldn't happen in a proper maze, but handle it
            self.solving_complete = True
            return False
            
        return True
    
    def _get_next_move(self):
        """Calculate next position using right-hand rule"""
        # Try to turn right first
        right_direction = (self.current_direction + 1) % 4
        right_pos = self._get_position_in_direction(self.current_pos, right_direction)
        
        if right_pos and self._can_move_to(right_pos):
            return right_pos, right_direction
        
        # If can't turn right, try going straight
        straight_pos = self._get_position_in_direction(self.current_pos, self.current_direction)
        if straight_pos and self._can_move_to(straight_pos):
            return straight_pos, self.current_direction
        
        # If can't go straight, try turning left
        left_direction = (self.current_direction - 1) % 4
        left_pos = self._get_position_in_direction(self.current_pos, left_direction)
        
        if left_pos and self._can_move_to(left_pos):
            return left_pos, left_direction
        
        # If can't turn left, turn around
        back_direction = (self.current_direction + 2) % 4
        back_pos = self._get_position_in_direction(self.current_pos, back_direction)
        
        if back_pos and self._can_move_to(back_pos):
            return back_pos, back_direction
            
        return None, self.current_direction
    
    def _get_position_in_direction(self, pos, direction):
        """Get the position in the given direction from current position"""
        if not pos:
            return None
            
        row, col = pos
        dr, dc = self.directions[direction]
        new_row, new_col = row + dr, col + dc
        
        if self.maze_structure.is_valid_position(new_row, new_col):
            return (new_row, new_col)
        return None
    
    def _can_move_to(self, pos):
        """Check if we can move to the given position (not a wall)"""
        if not pos:
            return False
        row, col = pos
        return self.maze_structure.is_path(row, col)
    
    def _is_exit_adjacent(self):
        """Check if the exit is directly adjacent to current position and reachable"""
        if not self.current_pos:
            return False
            
        exit_pos = self.maze_structure.get_end()
        if not exit_pos:
            return False
            
        current_row, current_col = self.current_pos
        exit_row, exit_col = exit_pos
        
        # Check if exit is directly adjacent (Manhattan distance = 1)
        if abs(current_row - exit_row) + abs(current_col - exit_col) == 1:
            return self._can_move_to(exit_pos)
            
        return False
    
    def get_current_path(self):
        """Return the path taken so far"""
        return self.path_taken
    
    def is_complete(self):
        """Check if solving is complete"""
        return self.solving_complete
        
    def get_current_position(self):
        """Get current position of the solver"""
        return self.current_pos
        
    def get_current_direction_name(self):
        """Get current direction as a string for robot orientation"""
        return self.direction_names[self.current_direction]
