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
        self.phase = "dfs"  # "dfs", "entrance", "exit", "complete"
    
    def get_maze(self):
        """Return the current maze grid"""
        return self.maze
    
    def get_start(self):
        """Return the start position"""
        return self.start
    
    def get_end(self):
        """Return the end position"""
        return self.end
        
    def start_generation(self):
        """Initialize the generation process"""
        if self.rows > 2 and self.cols > 2:
            sx = random.randrange(1, self.rows - 1, 2)
            sy = random.randrange(1, self.cols - 1, 2)
        else:
            sx, sy = 0, 0
            
        self.maze[sx][sy] = 1
        self.visited[sx][sy] = True
        self.current_pos = (sx, sy)
        self.stack = [(sx, sy)]
        
    def step_generation(self):
        """Perform one step of maze generation. Returns True if generation continues, False if complete."""
        if self.generation_complete:
            return False
            
        if self.phase == "dfs":
            return self._step_dfs()
        elif self.phase == "entrance":
            return self._step_entrance_exit()
        elif self.phase == "exit":
            return self._step_entrance_exit()
        else:
            self.generation_complete = True
            return False
    
    def _step_dfs(self):
        if not self.stack:
            self.phase = "entrance"
            self._setup_entrance_exit()
            return True
            
        x, y = self.stack[-1]
        # Don't set current_pos here yet
        
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
        
    
    def _setup_entrance_exit(self):
        """Set up entrance and exit points"""
        def rand_edge_row():
            r = random.randint(0, self.rows - 1)
            if self.rows > 2 and r % 2 == 0:
                r = max(1, min(self.rows - 2, r + (1 if r == 0 else -1)))
            return r

        self.start = (rand_edge_row(), 0)
        self.end = (rand_edge_row(), self.cols - 1)
        
        self.maze[self.start[0]][self.start[1]] = 1
        self.maze[self.end[0]][self.end[1]] = 1
        
        # Setup BFS for entrance connection
        self.current_pos = self.start
        self.bfs_queue = deque([self.start])
        self.bfs_parents = {self.start: None}
        self.connecting_entrance = True
        
    def _step_entrance_exit(self):
        if self.phase == "entrance" and self.connecting_entrance:
            if self._step_bfs_connection():
                return True
            else:
                # Start exit connection
                self.phase = "exit"
                self.current_pos = self.end
                self.bfs_queue = deque([self.end])
                self.bfs_parents = {self.end: None}
                self.connecting_entrance = False
                return True
        elif self.phase == "exit":
            if self._step_bfs_connection():
                return True
            else:
                self.phase = "complete"
                return False
        return False
    
    def _step_bfs_connection(self):
        if not self.bfs_queue:
            return False
            
        x, y = self.bfs_queue.popleft()
        self.current_pos = (x, y)
        
        # Check if we found an existing corridor (not the start point)
        target = self.start if self.connecting_entrance else self.end
        if (x, y) != target and self.maze[x][y] == 1:
            # Carve path back to start
            self._carve_path_to_start((x, y))
            return False
            
        # Continue BFS
        for dx, dy in ((0,1),(1,0),(0,-1),(-1,0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if (nx, ny) not in self.bfs_parents:
                    self.bfs_parents[(nx, ny)] = (x, y)
                    self.bfs_queue.append((nx, ny))
        
        return True
    
    def _carve_path_to_start(self, end_pos):
        target = self.start if self.connecting_entrance else self.end
        cur = end_pos
        while cur is not None:
            cx, cy = cur
            self.maze[cx][cy] = 1
            cur = self.bfs_parents[cur]

    def create_maze(self):
        """Complete maze generation instantly (for backward compatibility)"""
        # Initialize if not already started
        if not self.current_pos:
            self.start_generation()
        
        # Complete all steps instantly
        while not self.generation_complete:
            self.step_generation()