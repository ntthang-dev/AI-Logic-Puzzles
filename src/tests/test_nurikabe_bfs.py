import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nurikabe')))
from bfs_solver import Nurikabe # type: ignore
class TestNurikabeInit(unittest.TestCase):

    print("Toàn bộ quá trình test BFS được lưu ở src/nurikabe/Log(bfs)/")
    '''
    grid = [
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?']
            ]
    '''
    def test_bfs_1(self):
        grid = [
            ['?', '?', '?'],
            ['?', '1', '?'],
            ['?', '?', '?']
        ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/101.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
            ['.', '.', '.'],
            ['.', 1, '.'],
            ['.', '.', '.']
        ]
        self.assertEqual(solver.grid, expected)

    def test_bfs_2(self):   # No solution
        grid = [
            ['?', '?', '?'],
            ['?', '2', '?'],
            ['?', '3', '?']
        ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/102.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
            ['?', '?', '?'],
            ['?', 2, '?'],
            ['?', 3, '?']
        ] # No solution
        self.assertEqual(solver.grid, expected)

    def test_bfs_3(self):
        grid = [
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '2', '?', '2', '?'],
                ['?', '?', '?', '?', '?'],
                ['4', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/103.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                ['.', '.', '.', '.', '.'],
                ['.', '#', '.', '#', '.'],
                ['.', 2, '.', 2, '.'],
                ['.', '.', '.', '.', '.'],
                [4, '#', '#', '#', '.']
        ]
        self.assertEqual(solver.grid, expected)

    def test_bfs_4(self):
        grid = [
                ['?', '?', '?', '2', '?'],
                ['?', '?', '2', '?', '?'],
                ['?', '?', '?', '2', '?'],
                ['?', '1', '?', '?', '?'],
                ['?', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/104.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                ['.', '.', '.', 2, '#'],
                ['.', '#', 2, '.', '.'],
                ['.', '.', '.', 2, '.'],
                ['.', 1, '.', '#', '.'],
                ['.', '.', '.', '.', '.']
        ]
        self.assertEqual(solver.grid, expected)

    def test_bfs_5(self): # No solution
        grid = [
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '2', '?', '2', '?'],
                ['?', '?', '?', '?', '?'],
                ['3', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/105.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', 2, '?', 2, '?'],
                ['?', '?', '?', '?', '?'],
                [3, '?', '?', '?', '?']
        ]
        self.assertEqual(solver.grid, expected)
    def test_bfs_6(self):
        grid = [
                ['1', '?', '?', '?', '?'],
                ['?', '?', '2', '?', '?'],
                ['?', '2', '?', '?', '3'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/106.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                [1, '.', '.', '.', '.'],
                ['.', '.', 2, '#', '.'],
                ['.', 2, '.', '.', 3],
                ['.', '#', '.', '#', '#'],
                ['.', '.', '.', '.', '.']
        ]
        self.assertEqual(solver.grid, expected)
    def test_bfs_7(self):
        grid = [
                ['4', '?', '6', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '1'],
                ['?', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/107.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                [4, '.', 6, '#', '.'],
                ['#', '.', '#', '#', '.'],
                ['#', '.', '#', '.', '.'],
                ['#', '.', '#', '.', 1],
                ['.', '.', '.', '.', '.']
        ]
        self.assertEqual(solver.grid, expected)
    def test_bfs_8(self):
        grid = [
                ['?', '?', '?', '?', '5'],
                ['?', '4', '?', '?', '?'],
                ['3', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?'],
                ['?', '?', '?', '?', '?']
            ]
        solver = Nurikabe(grid, log_file="src/nurikabe/Log(bfs)/108.txt")
        solver.set_ID_begin()
        solver.solve_puzzle()
        expected = [
                ['.', '.', '.', '.', 5],
                ['.', 4, '#', '.', '#'],
                [3, '.', '#', '.', '#'],
                ['#', '.', '#', '.', '#'],
                ['#', '.', '.', '.', '#']
        ]
        self.assertEqual(solver.grid, expected)
        print("BFS tests passed")
if __name__ == "__main__":
    unittest.main()