"""
MazeGenerator - Handles maze generation using DFS algorithm.
Follows Single Responsibility Principle - only responsible for generating mazes.
"""
import random


class MazeGenerator:
    """Generates mazes using recursive backtracking DFS algorithm."""
    
    def __init__(self, maze_structure):
        self.maze_structure = maze_structure
        self.visited = [[False for _ in range(maze_structure.cols)] 
                       for _ in range(maze_structure.rows)]
        
        # Animation state
        self.generation_complete = False
        self.current_pos = None
        self.stack = []
        self.phase = "dfs"  # "dfs", "solving", "right_hand", "complete"
        
        # Path tracking for solving
        self.solution_path = []
        self.found_exit_during_generation = False
        self.solving_complete = False
        self.solving_current_step = 0
    
    def initialize_entry_exit(self):
        """Set up entrance and exit points"""
        def rand_edge_row():
            rows = self.maze_structure.rows
            # If there are only 1 or 2 rows, just pick any valid row.
            if rows <= 2:
                return random.randint(0, rows - 1)
            # Prefer an odd interior row (1 .. rows-2) so paths align with typical maze grids.
            odd_rows = [r for r in range(1, rows - 1) if r % 2 == 1]
            return random.choice(odd_rows)

        start = (rand_edge_row(), 0)
        end = (rand_edge_row(), self.maze_structure.cols - 1)
        
        self.maze_structure.set_start(start)
        self.maze_structure.set_end(end)
        
        # Carve start and end points immediately
        self.maze_structure.carve_path(start[0], start[1])
        self.maze_structure.carve_path(end[0], end[1])
        
        return start, end
    
    def start_generation(self):
        """Initialize the generation process"""
        start, end = self.initialize_entry_exit()
        
        # Start DFS from the entrance (start position)  
        sx, sy = start[0], start[1]
        
        # If starting from border (column 0), carve path to column 1 to connect to interior
        if sy == 0:
            self.maze_structure.carve_path(sx, 1)  # Carve the connecting path from entrance
            sy = 1  # Start DFS from column 1, not column 0
            
        self.maze_structure.carve_path(sx, sy)
        self.visited[sx][sy] = True
        self.current_pos = (sx, sy)
        self.stack = [(sx, sy)]
        
    def step_generation(self):
        """Perform one step of maze generation. Returns True if generation continues, False if complete."""
        if self.generation_complete:
            return False
            
        return self._step_dfs()
    
    def _step_dfs(self):
        """One step of depth-first search maze generation"""
        if not self.stack:
            # DFS complete
            self.generation_complete = True
            return False
            
        x, y = self.stack[-1]
        
        # Check if we've reached a cell adjacent to the exit (peek to the right)
        if not self.found_exit_during_generation:
            # Since exit is always on the right border, only check right neighbor
            nx, ny = x, y + 1
            if (nx, ny) == self.maze_structure.get_end():
                # Found the exit as right neighbor! Store the path
                self.found_exit_during_generation = True
                # Create complete path with intermediate cells filled in, plus the exit
                complete_path = self._create_complete_path(list(self.stack))
                complete_path.append(self.maze_structure.get_end())  # Add the exit cell as final destination
                self.solution_path = complete_path
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        found_unvisited = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.maze_structure.rows - 1 and 0 < ny < self.maze_structure.cols - 1:
                if not self.visited[nx][ny]:
                    # Create path to the new cell
                    self.maze_structure.carve_path(x + dx//2, y + dy//2)
                    self.maze_structure.carve_path(nx, ny)
                    self.visited[nx][ny] = True
                    self.stack.append((nx, ny))
                    # Update robot position to the NEW location immediately
                    self.current_pos = (nx, ny)
                    found_unvisited = True
                    break
        
        if not found_unvisited:
            self.stack.pop()
            # Update robot position when backtracking
            if self.stack:
                self.current_pos = self.stack[-1]
            
        return True

    def _create_complete_path(self, dfs_path):
        """Fill in the gaps between DFS steps to create a continuous path"""
        if len(dfs_path) < 2:
            return dfs_path
            
        complete_path = [dfs_path[0]]  # Start with the first cell
        
        for i in range(1, len(dfs_path)):
            prev_cell = dfs_path[i-1]
            curr_cell = dfs_path[i]
            
            # Add intermediate cell between prev and current
            intermediate_row = (prev_cell[0] + curr_cell[0]) // 2
            intermediate_col = (prev_cell[1] + curr_cell[1]) // 2
            
            # Only add if it's different from previous cell
            if (intermediate_row, intermediate_col) != prev_cell:
                complete_path.append((intermediate_row, intermediate_col))
            
            complete_path.append(curr_cell)
        
        return complete_path

    def create_maze_instantly(self):
        """Complete maze generation instantly (for backward compatibility)"""
        # Initialize if not already started
        if not self.current_pos:
            self.start_generation()
        
        # Complete all steps instantly
        while not self.generation_complete:
            self.step_generation()
            
    def get_solution_path(self):
        """Return the solution path found during generation"""
        return self.solution_path if self.found_exit_during_generation else []
    
    def get_current_position(self):
        """Return the current position of the generator"""
        return self.current_pos
