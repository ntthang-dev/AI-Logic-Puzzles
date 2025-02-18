markdown
# AI Logic Puzzles (Sudoku + Nurikabe)

## Giới thiệu
Dự án này triển khai các thuật toán giải quyết hai bài toán logic: Sudoku và Nurikabe. Chúng tôi sử dụng nhiều phương pháp khác nhau như DFS, A*, BFS và Hill Climbing để tìm giải pháp hiệu quả.


## Cài đặt
Để chạy dự án này, bạn cần cài đặt các gói cần thiết từ file `requirements.txt`:
```bash
pip install -r requirements.txt
Sử dụng
Sudoku
Phân tích bài toán:

Sudoku là một trò chơi logic với ma trận 9x9. Nhiệm vụ của bạn là điền các số từ 1 đến 9 vào các ô trống sao cho mỗi hàng, mỗi cột và mỗi khối 3x3 không có số lặp lại.

Input: Ma trận Sudoku ban đầu với một số ô đã được điền sẵn.

Output: Ma trận Sudoku đã hoàn thành.

Triển khai DFS cho Sudoku:

DFS (Depth-First Search) là một thuật toán tìm kiếm dựa trên ngăn xếp. Với Sudoku, ta sử dụng backtracking để thử tất cả các khả năng và quay lại khi gặp phải ngõ cụt.

Chạy giải pháp DFS cho Sudoku:

bash
python src/sudoku/dfs_solver.py
Nghiên cứu và triển khai A với MRV (Most Restrained Variable)*:

A Search* là một thuật toán tìm kiếm dựa trên heuristic. MRV là một chiến lược heuristic chọn biến có ít khả năng nhất trước tiên để giảm không gian tìm kiếm.

Chạy giải pháp A* cho Sudoku:

bash
python src/sudoku/astar_solver.py
Nurikabe
Phân tích bài toán:

Nurikabe là một trò chơi logic với lưới ô vuông. Nhiệm vụ của bạn là xác định các khu vực đảo và biển sao cho tất cả các đảo đều đúng kích thước và không có biển nào tách biệt.

Input: Lưới Nurikabe ban đầu với một số ô đã được xác định là đảo.

Output: Lưới Nurikabe đã hoàn thành với các khu vực đảo và biển hợp lệ.

Triển khai BFS cho Nurikabe:

BFS (Breadth-First Search) là một thuật toán tìm kiếm dựa trên hàng đợi. Với Nurikabe, ta sử dụng BFS để tìm các trạng thái hợp lệ của lưới.

Chạy giải pháp BFS cho Nurikabe:

bash
python src/nurikabe/bfs_solver.py
Nghiên cứu và triển khai Hill Climbing:

Hill Climbing là một thuật toán tối ưu hóa dựa trên việc lựa chọn bước đi tiếp theo dựa trên hàm mục tiêu. Với Nurikabe, ta tối ưu hóa vị trí đảo để tránh vi phạm quy tắc.

Chạy giải pháp Hill Climbing cho Nurikabe:

bash
python src/nurikabe/hill_climbing_solver.py
Kiểm thử
Để chạy các bài kiểm thử, sử dụng:

bash
pytest src/tests/
Báo cáo và Demo
Báo cáo: docs/report/AI_Logic_Puzzles_Report.md

Video demo: docs/video/demo.mp4