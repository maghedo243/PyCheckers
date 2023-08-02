import copy
import random
from enum import IntEnum

import pygame
from pygame import Rect, Surface

from util import Pair




class Board:
    def __init__(self):
        self.boardState = [[BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black")],
                           [BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white")],
                           [BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black")],
                           [BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white")],
                           [BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black")],
                           [BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white")],
                           [BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black")],
                           [BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white"),BoardSquare("black"),BoardSquare("white")]]
        self.checkerLocations = [[None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None],
                                [None,None,None,None,None,None,None,None]]

    def drawBoard(self,screen : Surface):
        if screen.get_height() != screen.get_width():
            return False

        metric = screen.get_width()/8
        metric2 = metric*0.8
        for x in range(self.boardState.__len__()):
            for y in range(self.boardState.__len__()):
                square = Rect(x*metric,y*metric,metric,metric)
                if self.boardState[y][x]:
                    self.boardState[y][x].hitbox = copy.deepcopy(square)
                    pygame.draw.rect(screen,self.boardState[y][x].color,self.boardState[y][x].hitbox)
                if self.checkerLocations[y][x]:
                    pygame.draw.circle(screen, self.checkerLocations[y][x].color, (x * metric + metric / 2, y * metric + metric / 2), metric2 / 2)
                    if self.checkerLocations[y][x].selected:
                        pygame.draw.circle(screen, "lightblue",(x * metric + metric / 2, y * metric + metric / 2), metric2 / 4)

    def defaultBoardLayout(self):
        for x in range(8):
            for y in range(8):
                if (x%2 == 0 and y%2 == 1 and x < 3) or (x%2 == 1 and y%2 == 0 and x < 3):
                    Checker("white", self, CheckerDirection.DOWN, Pair(x, y))
                elif (x%2 == 0 and y%2 == 1 and x > 4) or (x%2 == 1 and y%2 == 0 and x > 4):
                    Checker("red", self, CheckerDirection.UP, Pair(x, y))

        startingChecker = None
        while True:
            startingChecker = self.checkerLocations[random.randint(2,5)][random.randint(2,5)]
            if startingChecker is not None:
                break
        return startingChecker



class BoardSquare:
    def __init__(self,color):
        self.color = color
        self.hitbox = Rect(0,0,0,0)

class CheckerDirection(IntEnum):
    KING = 0
    UP = 1
    DOWN = 2

class Checker:
    def __init__(self, color: str, board: Board, direction: CheckerDirection, position: Pair):
        self.color = color
        self.possibleMoves = list()
        self.possibleKills = list()
        self.board = board
        self.direction = direction
        self.pos = position
        self.lastPos = position
        self.board.checkerLocations[self.pos.first][self.pos.second] = self
        self.selected = False

    def calculateMoves(self):
        self.possibleMoves.clear()
        self.calculateKills()
        match self.direction:
            case CheckerDirection.UP:
                if 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second - 1] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first - 1][self.pos.second - 1])
                elif 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][
                            self.pos.second - 1].color != self.color and 7 >= self.pos.first - 2 >= 0 and 7 >= self.pos.second - 2 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 2][self.pos.second - 2] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first - 2][self.pos.second - 2])

                if 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second + 1] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first - 1][self.pos.second + 1])
                elif 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][
                            self.pos.second + 1].color != self.color and 7 >= self.pos.first - 2 >= 0 and 7 >= self.pos.second + 2 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 2][self.pos.second + 2] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first - 2][self.pos.second + 2])

            case CheckerDirection.DOWN:
                if 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second + 1] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first + 1][self.pos.second + 1])
                elif 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][
                            self.pos.second + 1].color != self.color and 7 >= self.pos.first + 2 >= 0 and 7 >= self.pos.second + 2 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 2][self.pos.second + 2] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first + 2][self.pos.second + 2])

                if 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second - 1] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first + 1][self.pos.second - 1])
                elif 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][
                            self.pos.second - 1].color != self.color and 7 >= self.pos.first + 2 >= 0 and 7 >= self.pos.second - 2 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 2][self.pos.second - 2] is None:
                    self.possibleMoves.append(self.board.boardState[self.pos.first + 2][self.pos.second - 2])

    def calculateKills(self):
        self.possibleKills.clear()
        match self.direction:
            case CheckerDirection.UP:
                if 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second - 1] is not None and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second - 1].color != self.color:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first - 1][self.pos.second - 1])

                if 7 >= self.pos.first - 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second + 1] is not None and \
                        self.board.checkerLocations[self.pos.first - 1][self.pos.second + 1].color != self.color:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first - 1][self.pos.second + 1])

            case CheckerDirection.DOWN:
                if 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second + 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second + 1] is not None and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second + 1].color != self.color:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first + 1][self.pos.second + 1])

                if 7 >= self.pos.first + 1 >= 0 and 7 >= self.pos.second - 1 >= 0 and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second - 1] is not None and \
                        self.board.checkerLocations[self.pos.first + 1][self.pos.second - 1].color != self.color:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first + 1][self.pos.second - 1])

    def moveHighlight(self, reset=False):
        if len(self.possibleMoves) == 0:
            return
        if reset:
            for x in self.possibleMoves:
                x.color = "black"
        else:
            for x in self.possibleMoves:
                x.color = "lightblue"

    def move(self, x: int, y: int):
        if self.board.checkerLocations[y][x] is None and self.board.boardState[y][x] in self.possibleMoves:
            self.board.checkerLocations[self.pos.first][self.pos.second] = None
            self.board.checkerLocations[y][x] = self
            self.lastPos = Pair(self.pos.first, self.pos.second)
            self.pos.first = y
            self.pos.second = x
            self.moveHighlight(True)
            for i in self.possibleKills:
                if i.pos == (self.pos + self.lastPos):
                    self.board.checkerLocations[i.pos.first][i.pos.second] = None
            return True