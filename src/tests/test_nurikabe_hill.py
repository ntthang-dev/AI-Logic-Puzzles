import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nurikabe')))
from hill_climbing_solver import NurikabeHillClimbing # type: ignore

class TestNurikabeInit(unittest.TestCase):

    def test_hill_1(self):
        '''Template_Hill
                puzzle = [
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        '''
        grid = [
            ['.', '.', '.'],
            ['.', '1', '.'],
            ['.', '.', '.']
        ]
        solver = NurikabeHillClimbing(grid, max_iterations=50000)
        solution = solver.solve()
        expected = np.array(
            [['W', 'W', 'W'],
            ['W', 'L', 'W'],
            ['W', 'W', 'W']]
            )
        self.assertTrue(np.array_equal(solution, expected))
    def test_hill_2(self):
        grid = [
            ['.', '.', '.'],
            ['.', '2', '.'],
            ['.', '3', '.']
        ]
        solver = NurikabeHillClimbing(grid, max_iterations=50000)
        solution = solver.solve()
        expected = None
        self.assertTrue(np.array_equal(solution, expected))
    def test_hill_3(self):
        grid = [
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '2', '.', '2', '.'],
            ['.', '.', '.', '.', '.'],
            ['4', '.', '.', '.', '.']
        ]
        expected = np.array(
            [['W', 'W', 'W', 'W', 'W'],
            ['W', 'L', 'W', 'L', 'W'],
            ['W', 'L', 'W', 'L', 'W'],
            ['W', 'W', 'W', 'W', 'W'],
            ['L', 'L', 'L', 'L', 'W']]
            )
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return  # Nếu một lần đúng, kết thúc test luôn
        print(solution)
        self.fail("Solution was incorrect in all 3 attempts")
    def test_hill_4(self):
        grid = [
            ['.', '.', '.', '2', '.'],
            ['.', '.', '2', '.', '.'],
            ['.', '.', '.', '2', '.'],
            ['.', '1', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        expected = np.array(
            [['W', 'W', 'W', 'L', 'L'],
            ['W', 'L', 'L', 'W', 'W'],
            ['W', 'W', 'W', 'L', 'W'],
            ['W', 'L', 'W', 'L', 'W'],
            ['W', 'W', 'W', 'W', 'W']]
            )
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return  # Nếu một lần đúng, kết thúc test luôn
        print(solution)
        self.fail("Solution was incorrect in all 3 attempts")
    def test_hill_5(self):
        grid = [
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '2', '.', '2', '.'],
            ['.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.']
        ]
        expected = None
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return  # Nếu một lần đúng, kết thúc test luôn
        print(solution)
        self.fail("Solution was incorrect in all 3 attempts")
    def test_hill_6(self):
        grid=[
            ['1', '.', '.', '.', '.'],
            ['.', '.', '2', '.', '.'],
            ['.', '2', '.', '.', '3'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        expected=np.array(
            [['L', 'W', 'W', 'W', 'W'],
            ['W', 'W', 'L', 'L', 'W'],
            ['W', 'L', 'W', 'W', 'L'],
            ['W', 'L', 'W', 'L', 'L'],
            ['W', 'W', 'W', 'W', 'W']]
        )
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return  # Nếu một lần đúng, kết thúc test luôn
        print(solution)
        self.fail("Solution was incorrect in all 3 attempts")
    def test_hill_7(self):
        grid=[
            ['4', '.', '6', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '1'],
            ['.', '.', '.', '.', '.']
        ]
        expected=np.array(
            [['L' 'W', 'L', 'L', 'W'],
            ['L', 'W', 'L', 'L', 'W'],
            ['L', 'W', 'L', 'W', 'W'],
            ['L', 'W', 'L', 'W', 'L'],
            ['W', 'W', 'W', 'W', 'W']]
        )
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return
        print(solution)    
        self.fail("Solution was incorrect in all 3 attempts")
    def test_hill_8(self):
        grid=[
            ['.', '.', '.', '.', '5'],
            ['.', '4', '.', '.', '.'],
            ['3', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.']
        ]
        expected=np.array(
            [['W', 'W', 'W', 'W', 'L'],
            ['W', 'L', 'L', 'W', 'L'],
            ['L', 'W', 'L', 'W', 'L'],
            ['L', 'W', 'L', 'W', 'L'],
            ['L', 'W', 'W', 'W', 'L']]
        )
        for _ in range(3):  # Lặp tối đa 3 lần
            solver = NurikabeHillClimbing(grid, max_iterations=50000)
            solution = solver.solve()
            
            if np.array_equal(solution, expected):  
                return
        print(solution)    
        self.fail("Solution was incorrect in all 3 attempts")
if __name__ == "__main__":
    unittest.main()