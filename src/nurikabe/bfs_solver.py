from collections import deque
from copy import deepcopy
class Nurikabe:
    def __init__(self, grid, log_file="src/nurikabe/Log(bfs)/log_Bfs_nurikabe.txt"):
        self.log_file = log_file
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        self.id = [[-1] * self.cols for _ in range(self.rows)]
        self.id_stack = []
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    #Rule 1: các ô nước phải kết nối với nhau (Result -> True)
    def is_water_connected(self):
        dot_positions = {(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] == '.'}
        if not dot_positions:
            return True  

        def bfs(start):
            queue = deque([start])
            visited = set([start])
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in dot_positions and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            return visited

        start = next(iter(dot_positions))
        connected_dots = bfs(start)

        return connected_dots == dot_positions

    #Rule 2: Các đảo không được dính nhau (Result -> False)
    def is_islands_connected(self):
        stack = list(self.id_stack) 
        seen = set()
        while stack:
            r, c, id_island = stack.pop()
            queue = deque([(r, c)])
            visited = set([(r, c)])
            seed_ids = {id_island}  
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in seen or not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                        continue
                    if self.grid[nr][nc] == '.' or self.grid[nr][nc] == '?':
                        continue
                    seen.add((nr, nc))
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Kiểm tra nếu có seed island khác
                    for x, y, id_other in self.id_stack:
                        if (x, y) == (nr, nc) and id_other != id_island:
                            seed_ids.add(id_other)
                if len(seed_ids) > 1:
                    return True  

        return False  # Không có đảo nào dính nhau

    #Rule 3: nước không được tạo thành hình vuông 2x2 (Result -> False)
    def has_2x2_water_square(self):
        for r in range(self.rows - 1):
            for c in range(self.cols - 1):
                if (self.grid[r][c] == '.' and 
                    self.grid[r][c+1] == '.' and 
                    self.grid[r+1][c] == '.' and 
                    self.grid[r+1][c+1] == '.'):
                    return True  
        return False

    #Rule 4: các đảo phải có đủ diện tích theo số trên đảo (Result -> True)
    def is_island_area_correct(self):
        stack = list(self.id_stack)
        seen = set()
        while stack:
            r,c,id_island = stack.pop()
            queue = deque([(r, c)])
            visited = set([(r, c)])
            area = 1
            order=self.grid[r][c]
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in seen or (nr,nc)in visited or not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                        continue
                    if self.grid[nr][nc] == '.' or self.grid[nr][nc] == '?':
                        continue
                    seen.add((nr, nc))
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    area += 1
            if isinstance(order, int) and area != order:
                return False
        return True        
    
    #Rule 5: Không có đảo tự do (Result -> False)
    def has_free_island(self):
        # Đếm tổng số ô đất ('#')
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '#':  
                    count += 1
        count_island = 0
        stack = list(self.id_stack)
        seen = set()
        while stack:
            r, c, id_island = stack.pop()
            if (r, c) in seen:  
                continue
            queue = deque([(r, c)])
            visited = set([(r, c)])
            area = 0
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in seen or (nr, nc) in visited or not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                        continue
                    if self.grid[nr][nc] == '.' or self.grid[nr][nc] == '?':
                        continue
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    area += 1
            seen.update(visited) 
            count_island += area
        return count_island < count  # Đảm bảo tất cả đất đều thuộc một đảo có trọng số
    def is_island_area_correct2(self):
        stack = list(self.id_stack)
        seen = set()
        while stack:
            r,c,id_island = stack.pop()
            queue = deque([(r, c)])
            visited = set([(r, c)])
            area = 1
            order=self.grid[r][c]
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in seen or (nr,nc)in visited or not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                        continue
                    if self.grid[nr][nc] == '.' or self.grid[nr][nc] == '?':
                        continue
                    seen.add((nr, nc))
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    area += 1
            if isinstance(order, int) and area > order:
                return False
        return True     
    #Kiểm tra rule (Result -> True)
    def Rule(self):
        if self.is_water_connected() == False:
            return False
        if self.is_island_area_correct() == False:
            return False
        if self.has_free_island() == True:
            return False
        return True

    def set_ID_begin(self):
        id_island = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.grid[r][c], str) and self.grid[r][c].isdigit():
                    self.grid[r][c] = int(self.grid[r][c])  # Chuyển đổi sang số nguyên
                if isinstance(self.grid[r][c], int):
                    self.id[r][c] = id_island
                    self.id_stack.append((r, c, id_island))
                    id_island += 1

    def print_grid(self):
        for row in self.grid:
            print(' '.join(map(str, row)))

    def partly_rule(self):
        if self.is_islands_connected() == True:
            return False
        if self.has_2x2_water_square() == True:
            return False
        if self.is_island_area_correct2() == False:
            return False
        return True
    def fill_dirt_remaning(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.grid[r][c], int) and self.grid[r][c] > 1:
                    water_count = 0
                    unknown_cell = None

                    for dr, dc in self.directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc] == '.':
                                water_count += 1
                            elif self.grid[nr][nc] == '?':
                                if unknown_cell is None:
                                    unknown_cell = (nr, nc)
                                else:
                                    unknown_cell = None  # Có hơn 1 ô '?', không chắc chắn điền '#'
                                    break
                    
                    if water_count == 3 and unknown_cell:
                        ur, uc = unknown_cell
                        self.grid[ur][uc] = '#'

    def fill_water_remaning(self):
        # Điền '.' vào góc bảng nếu hai ô liền kề còn lại là nước
        corners = [(0, 0, [(0, 1), (1, 0)]),  # Góc trên trái
                (0, self.cols - 1, [(0, -1), (1, 0)]),  # Góc trên phải
                (self.rows - 1, 0, [(0, 1), (-1, 0)]),  # Góc dưới trái
                (self.rows - 1, self.cols - 1, [(0, -1), (-1, 0)])]  # Góc dưới phải

        for r, c, adjacent in corners:
            if self.grid[r][c] == '?':
                if all(0 <= r + dr < self.rows and 0 <= c + dc < self.cols and self.grid[r + dr][c + dc] == '.'
                    for dr, dc in adjacent):
                    self.grid[r][c] = '.'

    def pre_solve(self):
        # Điền '.' vào các ô xung quanh ô có số '1'
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    for dr, dc in self.directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == '?':
                            self.grid[nr][nc] = '.'
        # Điền '.' nếu một ô '?' có ít nhất 2 ô số xung quanh
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '?':
                    count_numbers = sum(
                        1 for dr, dc in self.directions
                        if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols and isinstance(self.grid[r + dr][c + dc], int)
                    )
                    if count_numbers >= 2:
                        self.grid[r][c] = '.'   
        self.fill_dirt_remaning()
        self.fill_water_remaning()
        
    def solve_puzzle(self,log_file=None):
        original_grid = deepcopy(self.grid)
        if log_file is None:
            log_file = self.log_file  # Sử dụng giá trị mặc định từ constructor
        # Tìm tất cả các vị trí có giá trị '?' trong lưới
        Iteration=0
        skip=0
        self.pre_solve()
        with open(log_file, "w") as f:
            
            f.write("Pre-solve"+"\n") 
            for row in self.grid:
                f.write(" ".join(map(str, row)) + "\n")
        unknowns = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] == '?']
        queue = deque()
        # Khởi tạo trạng thái ban đầu (lưới hiện tại)
        initial_state = deepcopy(self.grid)
        # Mỗi trạng thái là một tuple: (index, state)
        # index là số ô '?' đã được gán giá trị trong state
        queue.append((0, initial_state))
        while queue:
            Iteration+=1
            if Iteration % 200 == 0:
                with open(log_file, "a") as f:
                    f.write("Interation: "+str(Iteration)+"\n")
                    for row in state:
                        f.write(" ".join(map(str, row)) + "\n")
            index, state = queue.popleft()
            if index == len(unknowns) :
                candidate_solver = Nurikabe(state)
                candidate_solver.set_ID_begin()
                if candidate_solver.Rule():
                    self.grid = state
                    with open(log_file, "a") as f:
                        f.write("Solution found"+"\n")
                        f.write("Total Iteration: "+str(Iteration)+"\n")
                        f.write("Skip: "+str(skip)+"\n")
                        f.write("Actual Iteration: "+str(Iteration-skip)+"\n")
                        for row in state:
                            f.write(" ".join(map(str, row)) + "\n")
                    return self.grid 
                skip+=1
                continue
            r, c = unknowns[index]
            for value in ('.', '#'):
                new_state = deepcopy(state)
                new_state[r][c] = value
                candidate_solver = Nurikabe(new_state)
                candidate_solver.set_ID_begin()
                if candidate_solver.partly_rule() == False:
                    Iteration+=1
                    skip+=1
                    continue
                queue.append((index + 1, new_state))
        with open(log_file, "a") as f:
            self.grid = original_grid
            f.write("No solution found\n")
        return None  # Nếu không tìm được lời giải

# Test
if __name__ == "__main__":
    grid = [
                ['?', '?', '?', '?', '5'],
                ['?', '4', '?', '?', '?'],
                ['3', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?']
    ]
    solver = Nurikabe(grid)

    solver.set_ID_begin()

    solver.solve_puzzle()
    solver.print_grid()
    print("""Các dữ liệu quá trình được lưu vào file """,solver.log_file)