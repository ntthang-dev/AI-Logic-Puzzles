# gui.py 
# Tạo game sudoku với ma trận 9x9

import pygame
import sys
from solve_astar import solve_astar
from solve_dfs import solve_dfs
from utils import zero_number, is_valid

# Khởi tạo màn hình cho pygame
pygame.init()

# Kích thước cửa màn hình
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE # 540 / 9 = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Demo
sudoku_board = [
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 1, 3, 0, 5, 9, 0],
    [0, 0, 0, 0, 2, 7, 3, 4, 0],
    [0, 2, 0, 0, 0, 3, 0, 0, 0],
    [0, 6, 9, 0, 0, 2, 0, 0, 0],
    [3, 0, 8, 5, 4, 0, 0, 2, 0],
    [0, 7, 3, 0, 0, 0, 0, 1, 0],
    [0, 5, 4, 0, 0, 1, 7, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4]
]
"""
    DEMO
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 0, 6, 0, 4, 2, 3],
    [4, 2, 6, 8, 0, 3, 7, 9, 1],
    [7, 1, 3, 0, 2, 0, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
    Output1:
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]

    Input1
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 1, 3, 0, 5, 9, 0],
    [0, 0, 0, 0, 2, 7, 3, 4, 0],
    [0, 2, 0, 0, 0, 3, 0, 0, 0],
    [0, 6, 9, 0, 0, 2, 0, 0, 0],
    [3, 0, 8, 5, 4, 0, 0, 2, 0],
    [0, 7, 3, 0, 0, 0, 0, 1, 0],
    [0, 5, 4, 0, 0, 1, 7, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4]
    
"""

# Global variables
font = pygame.font.SysFont("comicsans", 36)
noted_font = pygame.font.SysFont("comicsans", 20)
msg_font = pygame.font.SysFont(None, 60)
initial_board = [row[:] for row in sudoku_board]
selected_cell = None         # (row, col) của ô được chọn
number_marks = {}            # Dictionary lưu candidate: key=(row,col), value=số người chơi nhập (chưa confirm)

# Set fps cho game
clock = pygame.time.Clock()

# ICON
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PUZZLE SUDOKU")
img = pygame.image.load('src/sudoku/img/sudoku-icon-1024x1024.png')
pygame.display.set_icon(img)

# help function
def draw_grid():
    """Vẽ lưới cho sudoku"""
    for i in range(GRID_SIZE + 1):
        # Cứ 3 ô là vẽ 1 lưới dài để tạo các box 3x3
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i*CELL_SIZE, 0), (i*CELL_SIZE, WIDTH), thickness)
        pygame.draw.line(screen, BLACK, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE), thickness)

def draw_numbers(board, font, color):
    """
    Vẽ số từ board_input vào lưới
    Các số ban đầu (trong initial_board) sẽ được vẽ màu đen
    Mới nhập sẽ màu xanh
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = board[row][col]
            if num != 0:
                color = BLACK if initial_board[row][col] != 0 else BLUE
                text = font.render(str(num), True, color)
                text_rect = text.get_rect(center=(col*CELL_SIZE + CELL_SIZE//2, row*CELL_SIZE + CELL_SIZE//2))
                screen.blit(text, text_rect)

def draw_number_mark(number_mark, number_font):
    """note số ở góc trái màn trước khi xác nhận"""
    for (row, col), candidates in number_mark.items():
        text = number_font.render(str(candidates), True, GRAY)
        screen.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 5))

def highlight_selected(cell):
    """Highlight ô được chọn"""
    if cell is not None:
        row, col = cell
        rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect, 3, 2)

def display_congratulation_msg():
    """Hiển thị thông báo khi giải đã xong"""
    text = msg_font.render("CONGRATULATIONS!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2 , HEIGHT - 30))
    screen.blit(text, text_rect)

def display_wrong_msg():
    """Hiển thị thông báo khi bạn nhập sai"""
    text = msg_font.render("WRONG!!!", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2 , HEIGHT - 30))
    screen.blit(text, text_rect)

def display_lose_msg():
    """Hiển thị thông báo thất bại"""
    text = msg_font.render("YOU LOSE!!!", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2 , HEIGHT - 30))
    screen.blit(text, text_rect)

def main():
    global selected_cell, number_marks, sudoku_board
    running = True
    solved = False
    error = 0
    total_error = 0

    # Chọn giải thuật dfs hay A*
    solver = solve_astar

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers(sudoku_board, font, BLACK)
        draw_number_mark(number_marks, noted_font)
        highlight_selected(selected_cell)

        # Hiện thị màn hình kết thúc
        if solved:
            display_congratulation_msg()
        elif total_error == 3:
            display_lose_msg()
        elif error == 1:
            display_wrong_msg()

        # Khi trò chơi kết thúc thì chỉ được nhấn quit
        if solved or total_error == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Chọn ô bằng chuột
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // CELL_SIZE
                    row = pos[1] // CELL_SIZE
                    if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                        selected_cell = (row, col)
                
                # Xử lý nhập phím
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_cell = (row, col - 1)
                    if event.key == pygame.K_RIGHT:
                        selected_cell = (row, col + 1)
                    if event.key == pygame.K_UP:
                        selected_cell = (row - 1, col)
                    if event.key == pygame.K_DOWN:
                        selected_cell = (row + 1, col)
                    row, col = selected_cell
                    if initial_board[row][col] == 0:
                        # chỉ cho phép số từ 1 đến 9
                        mapping = {
                            pygame.K_1: 1,
                            pygame.K_2: 2,  
                            pygame.K_3: 3,  
                            pygame.K_4: 4,  
                            pygame.K_5: 5,  
                            pygame.K_6: 6,  
                            pygame.K_7: 7,  
                            pygame.K_8: 8,  
                            pygame.K_9: 9,  
                        }
                        if event.key in mapping and sudoku_board[row][col] == 0:
                            number_marks[(row, col)] = mapping[event.key]
                        # Xóa ghi chú hoặc số đã xác nhận nếu nhấn Backspace/Delete (nếu không phải ô đề bài)
                        elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                            if (row, col) in number_marks:
                                del number_marks[(row, col)]
                        # Nếu nhấn Enter khi có ô được chọn, xác nhận ghi chú thành số chính thức
                        elif event.key == pygame.K_RETURN:
                            if (row, col) in number_marks:
                                if is_valid(sudoku_board, row, col, number_marks[(row, col)]):
                                    sudoku_board[row][col] = number_marks[(row, col)]
                                    del number_marks[(row, col)]
                                    error = 0
                                    if not zero_number(sudoku_board):
                                        solved = True
                                else:
                                    error = 1
                                    total_error = total_error + 1
                    # Nhấn A, gọi solver để hiển thị giải pháp solve_astar
                    elif event.key == pygame.K_a:
                        # TODO:
                        pass
                    # Nhấn D, gọi solver để hiển thị giải pháp solve_dfs
                    elif event.key == pygame.K_d:
                        # TODO:
                        pass

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()