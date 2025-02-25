import numpy as np
import random

class NurikabeHillClimbing:
    def __init__(self, initial_grid, max_iterations=10000):
        # Chuyển đổi grid sang kiểu object để lưu trữ cả số và ký tự
        self.grid = np.array(initial_grid, dtype=object)
        self.rows, self.cols = self.grid.shape
        self.max_iterations = max_iterations
        self.directions = [(-1,0), (1,0), (0,-1), (0,1)]
        
        # Khởi tạo trạng thái ban đầu (L = đảo, B = nước)
        self.current_state = np.where(np.vectorize(lambda x: str(x).isdigit)(self.grid), 'L', 'B')
        self.current_score = self.evaluate_state(self.current_state)

    def is_valid_cell(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def evaluate_state(self, state):
        score = 0
        
        # Kiểm tra các đảo
        numbered_cells = [(i,j) for i in range(self.rows) 
                         for j in range(self.cols) if str(self.grid[i,j]).isdigit()]
        
        for i, j in numbered_cells:
            target_size = int(self.grid[i,j])
            visited = np.zeros((self.rows, self.cols), dtype=bool)
            island_size = self.dfs(i, j, state, visited, 'L')
            score += abs(island_size - target_size) * 2  # Trọng số cao cho sai lệch kích thước

        # Kiểm tra nước liên thông
        if not self.check_water_connectivity(state):
            score += 20  # Trọng số cao cho nước không liên thông

        # Kiểm tra khối nước 2x2
        if self.check_2x2_water(state):
            score += 15  # Trọng số cho khối nước 2x2

        return score

    def dfs(self, row, col, state, visited, cell_type):
        if not self.is_valid_cell(row, col) or visited[row,col] or state[row,col] != cell_type:
            return 0
        visited[row,col] = True
        size = 1
        for dr, dc in self.directions:
            size += self.dfs(row + dr, col + dc, state, visited, cell_type)
        return size

    def check_water_connectivity(self, state):
        visited = np.zeros((self.rows, self.cols), dtype=bool)
        water_regions = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if state[i,j] == 'B' and not visited[i,j]:
                    water_regions += 1
                    if water_regions > 1:
                        return False
                    self.dfs(i, j, state, visited, 'B')
        return True

    def check_2x2_water(self, state):
        for i in range(self.rows-1):
            for j in range(self.cols-1):
                if (state[i,j] == 'B' and
                    state[i,j+1] == 'B' and
                    state[i+1,j] == 'B' and
                    state[i+1,j+1] == 'B'):
                    return True
        return False

    def get_neighbor(self):
        new_state = self.current_state.copy()
        
        # Tìm các ô có thể thay đổi (không phải ô số)
        change_candidates = [(i,j) for i in range(self.rows) 
                            for j in range(self.cols) 
                            if not str(self.grid[i,j]).isdigit()]
        
        if not change_candidates:
            return new_state
            
        # Thực hiện 3 thay đổi ngẫu nhiên để tăng khả năng thoát local optima
        for _ in range(3):
            row, col = random.choice(change_candidates)
            new_state[row,col] = 'L' if new_state[row,col] == 'B' else 'B'
        
        return new_state

    def solve(self):
        for _ in range(self.max_iterations):
            if self.current_score == 0:
                return self.current_state

            neighbor = self.get_neighbor()
            neighbor_score = self.evaluate_state(neighbor)

            if neighbor_score < self.current_score:
                self.current_state = neighbor
                self.current_score = neighbor_score
                print(f"Improved score: {self.current_score}")  # Thêm log để theo dõi
                print(self.current_state) # Thêm log để theo dõi

        return None

# Ví dụ sử dụng với puzzle đơn giản
if __name__ == "__main__":
    puzzle = [
        ['2', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '3', '.'],
        ['.', '.', '.', '.']
    ]

    solver = NurikabeHillClimbing(puzzle, max_iterations=50000)
    solution = solver.solve()

    if solution is not None:
        print("\nSolution found:")
        print(solution)
    else:
        print("\nNo solution found in given iterations")