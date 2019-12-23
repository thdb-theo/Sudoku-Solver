import numpy as np
from itertools import product
import random
import os
import time
import curses

screen = curses.initscr()


class Solver:
    def __init__(self, board):
        self.board = board
        assert board.shape[0] == board.shape[1], "The board is not a square!"
        self.sidelength = len(board[0])
        self.sqrsize = int(self.sidelength ** 0.5)
        self.boardsize = self.sidelength ** 2
        self.emptyindices = np.argwhere(board == 0)
        self.ticks = 0

    def violates(self, i, j):
        row = self.board[i]
        col = self.board[:,j]
        non0row = row[row != 0]
        non0col = col[col != 0]
        if len(set(non0row)) != len(non0row):
            return True
        if len(set(non0col)) != len(non0col):
            return True
        squarex = j // self.sqrsize
        squarey = i // self.sqrsize
        square = self.board[self.sqrsize*squarex:self.sqrsize*squarex+self.sqrsize,
                            self.sqrsize*squarey:self.sqrsize*squarey+self.sqrsize]
        non0square = square[square != 0]

        if len(set(non0square)) != len(non0square):
            return True
        return False

    def printboard(self):
        if self.ticks % 150 == 0:
            screen.addstr(self.sidelength+1, 0, str(self.board)+"\n")
            screen.refresh()

    def isviolation(self):
        for i, j in product(range(self.sidelength), range(self.sidelength)):
            if self.violates(i, j):
                return True
        return False

    def solved(self):
        if 0 in self.board:
            return False
        return self.isviolation()


    def solve(self):
        assert not self.isviolation(), "The board starts with a violation"
        
        current = 0
        while current < len(self.emptyindices):
            i, j = self.emptyindices[current]
            self.ticks += 1
            while self.board[i, j] < self.sidelength:
                self.board[i, j] += 1
                if not self.violates(i, j):
                    break
            else:
                self.board[i, j] = 0
                current -= 1
                if current < 0:
                    raise ValueError("The board is unsolvable")
                self.printboard()
                continue
            current += 1


def create_board(sidelength, givens):
    boardsize = sidelength ** 2
    while True:
        indices = random.sample(range(boardsize), givens)
        board = np.zeros([sidelength, sidelength], dtype=np.int)
        for idx in indices:
            num = random.randint(1, 9)
            board[idx // sidelength, idx % sidelength] = num
        if not Solver(board).isviolation():
            return board

if __name__ == "__main__":
    # board = np.array((
    #     [5,3,0,0,7,0,0,0,0],
    #     [6,0,0,1,9,5,0,0,0],
    #     [0,9,8,0,0,0,0,6,0],
    #     [8,0,0,0,6,0,0,0,3],
    #     [4,0,0,8,0,3,0,0,1],
    #     [7,0,0,0,2,0,0,0,6],
    #     [0,6,0,0,0,0,2,8,0],
    #     [0,0,0,4,1,9,0,0,5],
    #     [0,0,0,0,8,0,0,7,9]
    # ))

    board = np.array((
        [0,4,5,13,8,12,16,9,11,0,1,0,15,6,0,14],
        [3,0,11,9,14,15,6,4,10,7,16,13,0,0,12,0],
        [0,6,0,0,2,11,7,10,8,15,0,0,3,0,0,0],
        [15,0,0,0,3,0,1,13,0,12,14,0,10,2,11,4],
        [14,0,0,8,0,3,0,0,7,0,0,0,5,0,0,0],
        [0,5,0,0,0,0,14,11,12,0,0,10,0,16,0,13],
        [4,0,9,2,5,10,13,7,0,8,6,1,11,15,0,0],
        [12,0,1,0,0,0,0,16,0,0,13,0,0,0,3,0],
        [0,0,0,12,15,0,0,14,0,6,10,16,13,0,4,7],
        [16,1,13,0,10,0,0,3,0,0,7,0,0,9,6,15],
        [6,0,14,15,0,0,11,0,4,0,0,9,0,0,2,10],
        [2,3,10,4,7,16,0,0,0,0,8,0,0,11,0,0],
        [5,11,3,10,16,14,15,8,0,0,12,4,0,0,0,1],
        [0,14,0,0,11,9,0,0,0,13,15,0,4,0,5,0],
        [13,0,4,0,6,0,0,0,0,0,0,2,0,12,16,9],
        [0,12,0,16,0,13,0,0,0,1,0,0,6,14,15,11]
    ))

    #board = create_board(9, 15)
    # board = np.array((
    #     [0,2,0,0],
    #     [0,0,0,0],
    #     [3,0,0,0],
    #     [0,0,4,0]
    # ))
    oldboardstring = str(board)

    solver = Solver(board)
    screen.addstr(0,0,str(board))
    try:
        solver.solve()
    finally:
        curses.endwin()
    print(solver.board)
    print(solver.ticks)