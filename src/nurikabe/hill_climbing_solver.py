import numpy as np
import random
import time
import psutil
import os

class NurikabeHillClimbing:
    def __init__(self, initial_grid, max_iterations=10000):
        # Chuyển đổi grid sang kiểu object để lưu trữ cả số và ký tự
        self.grid = np.array(initial_grid, dtype=object)
        # Initialize rows and columns from the shape of the grid
        self.rows, self.cols = self.grid.shape
        self.max_iterations = max_iterations
        self.directions = [(-1,0), (1,0), (0,-1), (0,1)]
        
        # Khởi tạo trạng thái ban đầu (L = đảo, W = nước)
        self.current_state = np.where(np.vectorize(lambda x: str(x).isdigit())(self.grid), 'L', 'W')
        self.current_score = self.evaluate_state(self.current_state)

    def is_valid_cell(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    # hàm mục tiêu càng về gần 0 càng tốt
    def evaluate_state(self, state):
        score = 0
        
        # Kiểm tra các đảo
        numbered_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if str(self.grid[i,j]).isdigit():
                    numbered_cells.append((i,j))

        # khi đảo sai kích thước sẽ được cộng thêm chênh lệch kích thước * 2
        for (i, j) in numbered_cells:
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

    # duyệt theo chiều sâu lấy tất cả các thành phần liên thông với nhau theo loại của ô đang xét
    # Trả về size của loại ô liên thông đang kiểm tra (size đảo hoặc size nước)
    def dfs(self, row, col, state, visited, cell_type):
        if not self.is_valid_cell(row, col) or visited[row,col] or state[row,col] != cell_type:
            return 0
        visited[row,col] = True
        size = 1
        for dr, dc in self.directions:
            size += self.dfs(row + dr, col + dc, state, visited, cell_type)
        return size

    # Kiểm tra xem vùng nước có liên thông thành 1 vùng không
    # nếu có trả về true ngược lại trả về false
    def check_water_connectivity(self, state):
        visited = np.zeros((self.rows, self.cols), dtype=bool)
        water_regions = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if state[i,j] == 'W' and not visited[i,j]:
                    water_regions += 1
                    if water_regions > 1:
                        return False
                    self.dfs(i, j, state, visited, 'W')
        return True
    
    # lấy ra vùng nước thứ 2 bị cô lập
    # Trả về một list chứa tọa độ các ô nước của vùng nước bị cô lập
    def get_error_isolated_water_regions(self, state):
        visited = np.zeros((self.rows, self.cols), dtype=bool)
        water_regions = []
        water_regions_number = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i,j] == 'W' and not visited[i,j]:
                    water_regions_number += 1
                    if water_regions_number > 1:
                        water_regions.append((i,j))
                        return water_regions
                    self.dfs(i, j, state, visited, 'W')
        return water_regions

    # Lấy ra vùng đảo sai kích thước được quy định trong ô đánh số
    # Trả về một list chứa tọa độ các ô đảo sai kích thước   
    def get_false_size_island(self, state):
        global_visited = np.zeros((self.rows, self.cols), dtype=bool)
        false_island_regions = []
        
        # lấy ra các ô được đánh số cho đảo
        # các ô này là cố định không thay đổi
        numbered_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if str(self.grid[i,j]).isdigit():
                    numbered_cells.append((i,j))
        
        # dùng dfs duyệt qua tất cả vùng đảo được đánh số 
        # sau đó kiểm tra xem trong vùng đảo hiện tại có đảo không đảm bảo kích thước không
        # điều kiện đảo không đảm bảo kích thước là vượt qua / không bằng số ô được quy định trong ô đánh số
        for (i, j) in numbered_cells:
            visited = np.zeros((self.rows, self.cols), dtype=bool)  
            if state[i,j] == 'L' and visited[i,j] == False:
                island_size = self.dfs(i, j, state, visited, 'L')
                target_size = int(self.grid[i,j])
                if island_size != target_size:
                    false_island_regions.append((i,j))
            
            # đánh dấu các ô đảo chứa ô được đánh số đã đi qua
            for i in range(self.rows):
                for j in range(self.cols):
                    global_visited[i,j] = visited[i,j]
        
        # duyệt qua các đảo không được đánh số
        # đây có thể là các đảo bị đánh ngẫu nhiên mà không chứa ô đánh số 
        # nếu có trường hợp này thì phải lập tức xóa đảo này đi
        # chuyển từ L ---> W
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         if state[i,j] == 'L' and global_visited[i,j] == False and (i,j) not in numbered_cells:
        #             global_visited[i,j] = True
        #             state[i,j] = 'W'

        
        return false_island_regions

    def check_2x2_water(self, state):
        for i in range(self.rows-1):
            for j in range(self.cols-1):
                if (state[i,j] == 'W' and
                    state[i,j+1] == 'W' and
                    state[i+1,j] == 'W' and
                    state[i+1,j+1] == 'W'):
                    return True
        return False
    
    def get_error_2x2_water_cells(self, state):
        for i in range(self.rows-1):
            for j in range(self.cols-1):
                if (state[i,j] == 'W' and
                    state[i,j+1] == 'W' and
                    state[i+1,j] == 'W' and
                    state[i+1,j+1] == 'W'):
                    return [(i,j), (i,j+1), (i+1,j), (i+1,j+1)]
        return []

    def get_best_neighbor(self):
        new_state = self.current_state.copy()
        is_new_state_valid = False
        
        # Tìm các ô có thể thay đổi (không phải ô số)
        change_candidates = []  # Danh sách chứa tọa độ các ô có thể thay đổi

        for i in range(self.rows):  # Lặp qua từng hàng
            for j in range(self.cols):  # Lặp qua từng cột
                if not str(self.grid[i, j]).isdigit():  # Nếu ô không chứa số
                    change_candidates.append((i, j))  # Thêm tọa độ vào danh sách

        
        if not change_candidates:
            return new_state
            
        error_cells = []
        error_cells += self.get_false_size_island(new_state)
        error_cells += self  .get_error_isolated_water_regions(new_state)
        error_cells += self.get_error_2x2_water_cells(new_state)
        # print(f'Error cells: {error_cells}')
        
        # Thực hiện thay đổi ngẫu nhiên trên các ô có thể thay đổi và là ô bị lỗi
        # Chọn lấy best neighbor
        for error_cell in error_cells:
            # nếu ô hiện tại có thể thay đổi (không phải ô số) và ô hiện tại bị lỗi
            if error_cell in change_candidates:
                temp_state = new_state.copy()
                temp_state[error_cell] = 'W' if new_state[error_cell] == 'L' else 'L'
                if self.evaluate_state(temp_state) < self.evaluate_state(new_state):
                    new_state = temp_state
                    is_new_state_valid = True
                    return new_state  
            
            # nếu ô này là ô lỗi và nó là ô chứa số 
            # chứng tỏ đây là ô và dãy ô liên quan nó là đảo bị sai size
            # chọn ngẫu nhiên hướng đi liền kề là đảo và thay đổi ô đó thành nước để điều chỉnh size
            else:

                # đi lần lượt qua ô liền kề theo 4 hướng
                # nếu ô liền kề là đảo thì chọn ô đó để đi
                # kiểm tra xem có phải là láng giềng tốt nhất không
                for dr, dc in self.directions:
                    new_row, new_col = error_cell[0] + dr, error_cell[1] + dc
                    if self.is_valid_cell(new_row, new_col) and not str(self.grid[new_row, new_col]).isdigit() and new_state[new_row, new_col] == 'L':
                        temp_state = new_state.copy()
                        temp_state[new_row, new_col] = 'W'
                        if self.evaluate_state(temp_state) < self.evaluate_state(new_state):
                            new_state = temp_state
                            is_new_state_valid = True
                            return new_state
        
        # nếu không có chuyển sang trạng thái mới hợp lệ
        # Thực hiện 3 thay đổi ngẫu nhiên trên các ô có thể thay đổi 
        # để thoát khỏi local optima
        if not is_new_state_valid:
            for x in range(3):
                secure_random = random.SystemRandom()
                row, col = secure_random.choice(change_candidates)
                new_state[row,col] = 'W' if new_state[row,col] == 'L' else 'L'
         
        return new_state

    def solve(self):
        start_time = time.perf_counter()
        process = psutil.Process(os.getpid())  # Lấy thông tin tiến trình hiện tại
        start_memory = process.memory_info().rss / 1024 / 1024  # Bộ nhớ ban đầu (MB)
        start_cpu = process.cpu_percent(interval=None)  # CPU ban đầu
        
        print(f"=============================================")
        print("Solving using Hill Climbing...")
        print(f"Max iterations: {self.max_iterations}")
        print(f"Start time: {start_time}")
        print(f"Start memory: {start_memory} MB")
        print(f"Start CPU: {start_cpu}%")
        print(f"Current process: {process}")
        print(f"Initial score: {self.current_score}")
        print(f"Initial state: \n{self.current_state}")


        for x in range(self.max_iterations):
            if self.current_score == 0:
                end_time = time.perf_counter()
                end_memory = process.memory_info().rss / 1024 / 1024  # Bộ nhớ cuối (MB)
                end_cpu = process.cpu_percent(interval=None)  # CPU cuối

                print(f"End time: {end_time}")
                print(f"Processing time: {end_time - start_time:.4f} seconds")
                print(f"Used memory: {end_memory - start_memory:.2f} MB")
                print(f"Average CPU usage: {end_cpu:.2f}%")
                
                print("\nSolution found:")
                print(self.current_state)

                return self.current_state

            neighbor = self.get_best_neighbor()
            neighbor_score = self.evaluate_state(neighbor)

            if neighbor_score < self.current_score:
                self.current_state = neighbor
                self.current_score = neighbor_score
                print(f"Improved score: {self.current_score}")  # Thêm log để theo dõi
                print(self.current_state) # Thêm log để theo dõi

        end_time = time.perf_counter()
        end_memory = process.memory_info().rss / 1024 / 1024  # Bộ nhớ cuối (MB)
        end_cpu = process.cpu_percent(interval=None)  # CPU cuối

        print(f"End time: {end_time}")
        print(f"Processing time: {end_time - start_time:.4f} seconds")
        print(f"Used memory: {end_memory - start_memory:.2f} MB")
        print(f"Average CPU usage: {end_cpu:.2f}%")
        
        print("\nNo exactly solution found in given iterations")

        return None

# Ví dụ sử dụng với puzzle đơn giản
if __name__ == "__main__":
    puzzle = [
        ['5', '.', '1', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['3', '.', '.', '.', '5']
    ]

    solver = NurikabeHillClimbing(puzzle, max_iterations=50000)
    solution = solver.solve()

    if solution is not None:
        print("\nSolution found:")
        print(solution)
    else:
        print("\nNo exactly solution found in given iterations")