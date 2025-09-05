"""
MazeStructure - Represents the physical maze structure and provides basic operations.
Follows Single Responsibility Principle - only handles maze data structure.
"""


class MazeStructure:
    """Handles the maze grid structure and basic queries."""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (0, 0)
    
    def get_grid(self):
        """Return the current maze grid"""
        return self.grid
    
    def get_start(self):
        """Return the start position"""
        return self.start
    
    def get_end(self):
        """Return the end position"""
        return self.end
    
    def set_start(self, position):
        """Set the start position"""
        self.start = position
    
    def set_end(self, position):
        """Set the end position"""
        self.end = position
    
    def is_valid_position(self, row, col):
        """Check if position is within maze bounds"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_wall(self, row, col):
        """Check if position is a wall (0)"""
        if not self.is_valid_position(row, col):
            return True
        return self.grid[row][col] == 0
    
    def is_path(self, row, col):
        """Check if position is a path (1)"""
        if not self.is_valid_position(row, col):
            return False
        return self.grid[row][col] == 1
    
    def set_cell(self, row, col, value):
        """Set a cell to path (1) or wall (0)"""
        if self.is_valid_position(row, col):
            self.grid[row][col] = value
    
    def carve_path(self, row, col):
        """Carve a path at the given position"""
        self.set_cell(row, col, 1)
    
    def get_neighbors(self, row, col):
        """Get valid neighboring positions (up, right, down, left)"""
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def copy(self):
        """Create a copy of the maze structure"""
        new_maze = MazeStructure(self.rows, self.cols)
        new_maze.grid = [row[:] for row in self.grid]
        new_maze.start = self.start
        new_maze.end = self.end
        return new_maze
