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
        self.create_maze()

    def create_maze(self):
        # 1) Generate a maze (DFS) from an odd interior cell so walls stay intact
        if self.rows > 2 and self.cols > 2:
            sx = random.randrange(1, self.rows - 1, 2)
            sy = random.randrange(1, self.cols - 1, 2)
        else:
            sx, sy = 0, 0

        self.maze[sx][sy] = 1
        self.dfs(sx, sy)

        # 2) Pick entrance (left edge) and exit (right edge), prefer odd rows to align with corridors
        def rand_edge_row():
            r = random.randint(0, self.rows - 1)
            if self.rows > 2 and r % 2 == 0:
                r = max(1, min(self.rows - 2, r + (1 if r == 0 else -1)))
            return r

        self.start = (rand_edge_row(), 0)
        self.end = (rand_edge_row(), self.cols - 1)

        # Mark entrance/exit cells and force-connect them to the closest DFS branch
        self.maze[self.start[0]][self.start[1]] = 1
        self.maze[self.end[0]][self.end[1]] = 1
        self.force_connect_to_maze(self.start)
        self.force_connect_to_maze(self.end)


    def dfs(self, x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Move by 2 to create walls between paths
        random.shuffle(directions)

        self.visited[x][y] = True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.rows - 1 and 0 < ny < self.cols - 1:
                if not self.visited[nx][ny]:
                    # Create path to the new cell
                    self.maze[x + dx//2][y + dy//2] = 1  # Wall between current and next cell
                    self.maze[nx][ny] = 1  # Next cell
                    self.dfs(nx, ny)

    def force_connect_to_maze(self, pos):
        """
        Force-connect 'pos' (entrance/exit on the border) to the nearest existing corridor (value==1)
        by carving along the shortest 4-neighbor path found with BFS.
        """
        x0, y0 = pos

        # If already adjacent to a corridor, nothing to do
        for dx, dy in ((0,1),(1,0),(0,-1),(-1,0)):
            nx, ny = x0 + dx, y0 + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 1:
                return

        q = deque()
        q.append((x0, y0))
        parents = { (x0, y0): None }

        # BFS until we touch any existing corridor (excluding the start itself)
        while q:
            x, y = q.popleft()

            # Found the closest existing corridor (not the start)
            if (x, y) != (x0, y0) and self.maze[x][y] == 1:
                # Carve the path back to the start
                cur = (x, y)
                while cur is not None:
                    cx, cy = cur
                    self.maze[cx][cy] = 1
                    cur = parents[cur]
                return

            for dx, dy in ((0,1),(1,0),(0,-1),(-1,0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if (nx, ny) not in parents:
                        parents[(nx, ny)] = (x, y)
                        q.append((nx, ny))

        # Fallback (very small grids): carve one step inward
        for dx, dy in ((0,1),(1,0),(0,-1),(-1,0)):
            nx, ny = x0 + dx, y0 + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                self.maze[nx][ny] = 1
                break

    def get_maze(self):
        return self.maze

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end