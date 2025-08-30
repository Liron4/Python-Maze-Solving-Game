import random
from collections import deque

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (0, 0)
        
        # Animation state
        self.generation_complete = False
        self.current_pos = None
        self.stack = []
        self.phase = "dfs"  # "dfs", "solving", "complete"
        
        # Path tracking for solving
        self.solution_path = []
        self.found_exit_during_generation = False
        self.solving_complete = False
        self.solving_current_step = 0
    
    def get_maze(self):
        """Return the current maze grid"""
        return self.maze
    
    def get_start(self):
        """Return the start position"""
        return self.start
    
    def get_end(self):
        """Return the end position"""
        return self.end
    
    def get_solution_path(self):
        """Return the current solution path for visualization"""
        if self.phase == "solving" and self.solving_current_step > 0:
            return self.solution_path[:self.solving_current_step]
        elif self.solving_complete:
            return self.solution_path
        return []
    
    def is_solving_phase(self):
        """Check if we're in the solving phase"""
        return self.phase == "solving"
    
    def is_solving_complete(self):
        """Check if solving is complete"""
        return self.solving_complete
        
    def start_generation(self):
        """Initialize the generation process"""
        # Set up entrance and exit points FIRST (already carved and colored)
        def rand_edge_row():
            r = random.randint(0, self.rows - 1)
            if self.rows > 2 and r % 2 == 0:
                r = max(1, min(self.rows - 2, r + (1 if r == 0 else -1)))
            return r

        self.start = (rand_edge_row(), 0)
        self.end = (rand_edge_row(), self.cols - 1)
        
        # Carve start and end points immediately
        self.maze[self.start[0]][self.start[1]] = 1
        self.maze[self.end[0]][self.end[1]] = 1
        
        # Start DFS from the entrance (start position)  
        sx, sy = self.start[0], self.start[1]
        
        # If starting from border (column 0), carve path to column 1 to connect to interior
        if sy == 0:
            self.maze[sx][1] = 1  # Carve the connecting path from entrance
            sy = 1  # Start DFS from column 1, not column 0
            
        self.maze[sx][sy] = 1
        self.visited[sx][sy] = True
        self.current_pos = (sx, sy)
        self.stack = [(sx, sy)]
        
    def step_generation(self):
        """Perform one step of maze generation. Returns True if generation continues, False if complete."""
        if self.generation_complete and self.solving_complete:
            return False
            
        if self.phase == "dfs":
            return self._step_dfs()
        elif self.phase == "solving":
            return self._step_solving()
        else:
            return False
    
    def _step_dfs(self):
        if not self.stack:
            # DFS complete, start solving phase if we found the exit during generation
            self.generation_complete = True
            if self.found_exit_during_generation:
                self._start_solving()
                return True
            else:
                self.phase = "complete"
                self.solving_complete = True
                return False
            
        x, y = self.stack[-1]
        
        # Check if we've reached a cell adjacent to the exit (peek to the right)
        if not self.found_exit_during_generation:
            # Since exit is always on the right border, only check right neighbor
            nx, ny = x, y + 1
            if (nx, ny) == self.end:
                # Found the exit as right neighbor! Store the path
                self.found_exit_during_generation = True
                # Create complete path with intermediate cells filled in, plus the exit
                complete_path = self._create_complete_path(list(self.stack))
                complete_path.append(self.end)  # Add the exit cell as final destination
                self.solution_path = complete_path
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        found_unvisited = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.rows - 1 and 0 < ny < self.cols - 1:
                if not self.visited[nx][ny]:
                    # Create path to the new cell
                    self.maze[x + dx//2][y + dy//2] = 1
                    self.maze[nx][ny] = 1
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

    def _start_solving(self):
        """Initialize the solving phase"""
        self.phase = "solving"
        self.solving_current_step = 0
        # Set robot position to start for solving animation
        self.current_pos = self.start

    def _step_solving(self):
        """Perform one step of solving animation"""
        if self.solving_current_step >= len(self.solution_path):
            self.solving_complete = True
            self.phase = "complete"
            return False
        
        # Move robot along the solution path
        self.current_pos = self.solution_path[self.solving_current_step]
        self.solving_current_step += 1
        
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

    def create_maze(self):
        """Complete maze generation instantly (for backward compatibility)"""
        # Initialize if not already started
        if not self.current_pos:
            self.start_generation()
        
        # Complete all steps instantly
        while not self.generation_complete:
            self.step_generation()