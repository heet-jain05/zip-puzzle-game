import sys, random, sqlite3, uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.setrecursionlimit(10000)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "data.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, time TEXT, grid TEXT, backtracks INTEGER, timestamp TEXT
            )
        """)
        conn.commit()
init_db()

class Generator:
    def __init__(self, n):
        self.n = n

    def generate(self, k, mode="normal"):
        for _ in range(300):
            grid = [[0]*self.n for _ in range(self.n)]
            blockades = []
            walls = []
            
            # Hard Mode: Block random whole cells
            if mode == "hard":
                for _ in range(random.randint(3, 6)):
                    r, c = random.randint(0, self.n-1), random.randint(0, self.n-1)
                    if grid[r][c] == 0:
                        grid[r][c] = -1
                        blockades.append([r, c])
            
            start = (random.randint(0, self.n-1), random.randint(0, self.n-1))
            while grid[start[0]][start[1]] == -1:
                start = (random.randint(0, self.n-1), random.randint(0, self.n-1))
            
            path = []
            target = (self.n * self.n) - len(blockades)
            
            if self.solve(grid, path, start, target):
                # Elite Mode: Add edge walls after finding path
                if mode == "elite":
                    used = set()
                    for i in range(len(path)-1):
                        used.add(tuple(sorted((tuple(path[i]), tuple(path[i+1])))))
                    for r in range(self.n):
                        for c in range(self.n):
                            if c < self.n-1 and tuple(sorted(((r,c),(r,c+1)))) not in used and random.random()>0.6:
                                walls.append({"p1":[r,c], "p2":[r,c+1]})
                            if r < self.n-1 and tuple(sorted(((r,c),(r+1,c)))) not in used and random.random()>0.6:
                                walls.append({"p1":[r,c], "p2":[r+1,c]})

                step = max(1, len(path) // (k - 1))
                pts = {str(i+1): path[i*step if i*step < len(path) else -1] for i in range(k-1)}
                pts[str(k)] = path[-1]
                return {"size": self.n, "checkpoints": pts, "blockades": blockades, "walls": walls}
        return None

    def solve(self, grid, path, cur, target):
        r, c = cur
        grid[r][c] = 1
        path.append(cur)
        if len(path) == target: return True
        moves = []
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.n and 0 <= nc < self.n and grid[nr][nc] == 0:
                exits = sum(1 for ddr, ddc in [(0,1),(1,0),(0,-1),(-1,0)] 
                            if 0 <= nr+ddr < self.n and 0 <= nc+ddc < self.n and grid[nr+ddr][nc+ddc] == 0)
                moves.append((exits, nr, nc))
        moves.sort()
        for _, nr, nc in moves:
            if self.solve(grid, path, (nr, nc), target): return True
        grid[r][c] = 0
        path.pop()
        return False

@app.post("/generate")
def gen(data: dict):
    res = Generator(int(data.get("size", 4))).generate(int(data.get("checkpoints", 3)), data.get("mode", "normal"))
    if not res: raise HTTPException(status_code=500)
    return res

@app.post("/submit")
def sub(data: dict):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO scores(name,time,grid,backtracks,timestamp) VALUES(?,?,?,?,?)", 
                     (data.get("name"), data.get("time"), data.get("grid"), data.get("backtracks"), datetime.now().isoformat()))
    return {"ok": True}

@app.get("/leaderboard")
def lead():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT name, time, grid, backtracks FROM scores ORDER BY CAST(REPLACE(time, 's', '') AS INTEGER) ASC")
        return [{"name":r[0], "time":r[1], "grid":r[2], "backtracks":r[3]} for r in c.fetchall()]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)