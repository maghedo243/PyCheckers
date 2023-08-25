import copy
import random
import time
from enum import IntEnum, Enum

import pygame
from pygame import Rect, Surface

from util import Pair, inGameState, CheckerMove, get_path

crownImage = pygame.image.load(get_path("resources/images/crown.png"))
crownImage = pygame.transform.smoothscale(crownImage,(30,30))
crownImage.fill("yellow",special_flags=pygame.BLEND_ADD)

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
        self.oneColor = None
        self.twoColor = None

    def drawBoard(self,screen : Surface):
        """
        Draws the board squares and checkers on the given screen

        :param screen: the Surface that the board is drawn on.
        :type screen: Surface
        :return: True if the board draw is complete
        """
        if screen.get_height() != screen.get_width():
            return False

        metric = screen.get_width()/8
        metric2 = metric*0.8
        metric3 = metric*0.2
        for x in range(self.boardState.__len__()):
            for y in range(self.boardState.__len__()):
                square = Rect(x*metric,y*metric,metric,metric)
                if self.boardState[y][x]:
                    self.boardState[y][x].hitbox = copy.deepcopy(square)
                    pygame.draw.rect(screen,self.boardState[y][x].color,self.boardState[y][x].hitbox)
                if self.checkerLocations[y][x]:
                    pygame.draw.circle(screen, self.checkerLocations[y][x].color, (x * metric + metric / 2, y * metric + metric / 2), metric2 / 2)
                    if self.checkerLocations[y][x].direction == CheckerDirection.KING:
                        screen.blit(crownImage,(x * metric + metric3,y * metric + metric3))
                    if self.checkerLocations[y][x].selected:
                        pygame.draw.circle(screen, "lightblue",(x * metric + metric / 2, y * metric + metric / 2), metric2 / 4)

    def playerSearch(self,player:int):
        """
        Searches to see if a playerID exists on the board. (1 or 2)

        :param player: The playerID that is given. (1 or 2)
        :type player: int
        :return: True if the player is found
        """
        for x in self.checkerLocations:
            for y in x:
                if y is not None:
                    match player:
                        case 1:
                            if y.color == self.oneColor:
                                return True
                        case 2:
                            if y.color == self.twoColor:
                                return True
        return False

    def winCheck(self):
        if not self.playerSearch(2): #player one wins
            return 1
        elif not self.playerSearch(1): #player two wins
            return 2
        else:
            return False

    def clear(self):
        self.checkerLocations = [[None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None],
                                 [None, None, None, None, None, None, None, None]]

    def defaultBoardLayout(self,oneColor,twoColor):
        """
        Makes the board match the standard Checkers layout.

        :param oneColor: Player One color
        :param twoColor: Player Two color
        :return: The starting checker
        """
        self.oneColor = oneColor
        self.twoColor = twoColor
        for x in range(8):
            for y in range(8):
                if (x%2 == 0 and y%2 == 1 and x < 3) or (x%2 == 1 and y%2 == 0 and x < 3):
                    Checker(twoColor, self, CheckerDirection.DOWN, Pair(x, y), inGameState.PLAYERTWO)
                elif (x%2 == 0 and y%2 == 1 and x > 4) or (x%2 == 1 and y%2 == 0 and x > 4):
                    Checker(oneColor, self, CheckerDirection.UP, Pair(x, y), inGameState.PLAYERONE)

        while True:
            startingChecker = self.checkerLocations[random.randint(2,5)][random.randint(2,5)]
            if startingChecker is not None:
                break
        return startingChecker

    def testBoardLayout(self,oneColor,twoColor):
        self.oneColor = oneColor
        self.twoColor = twoColor
        Checker(twoColor, self, CheckerDirection.DOWN, Pair(2, 5), inGameState.PLAYERTWO)
        Checker(oneColor, self, CheckerDirection.UP, Pair(6, 1), inGameState.PLAYERONE)
        while True:
            startingChecker = self.checkerLocations[random.randint(2,5)][random.randint(2,5)]
            if startingChecker is not None:
                break
        return startingChecker




class BoardSquare:
    """A square on a board. It stores the hitbox and color."""

    def __init__(self,color):
        self.color = color
        self.hitbox = Rect(0,0,0,0)

class CheckerDirection(IntEnum):
    """The direction state a checker can move. Options are \"KING\", \"UP\", or \"DOWN\" """
    KING = 0
    UP = 1
    DOWN = 2

class MoveDirection(Enum):
    """The directions that a checker can move. \"UPLEFT\", \"UPRIGHT\", \"DOWNLEFT\", \"DOWNRIGHT\" """
    UPLEFT = (-1,-1)
    UPRIGHT = (-1,1)
    DOWNLEFT = (1,-1)
    DOWNRIGHT = (1,1)

    def __neg__(self):
        return -self.value[0],-self.value[1]

class Checker:
    """A checker. This stores its:

    - color
    - playerID
    - possible moves
    - possible kills
    - the board it is assigned to
    - its direction state
    - its position and last position
    - its most recent move
    - if it's selected or not.

    """
    def __init__(self, color: str, board: Board, direction: CheckerDirection, position: Pair, playerID: inGameState):
        self.color = color
        self.playerID = playerID
        self.possibleMoves = list()
        self.possibleKills = list()
        self.board = board
        self.direction = direction
        self.pos = position
        self.lastPos = position
        self.lastMove = None
        self.board.checkerLocations[self.pos.first][self.pos.second] = self
        self.selected = False

    
    def calculateMoves(self):
        """Calculates the move possibilities based on the Checker's direction state."""
        self.possibleMoves.clear()
        self.calculateKills()
        match self.direction:
            case CheckerDirection.UP:
                self.moveCast(MoveDirection.UPLEFT,"standard")
                self.moveCast(MoveDirection.UPRIGHT, "standard")
            case CheckerDirection.DOWN:
                self.moveCast(MoveDirection.DOWNRIGHT, "standard")
                self.moveCast(MoveDirection.DOWNLEFT, "standard")
            case CheckerDirection.KING:
                self.moveCast(MoveDirection.UPLEFT, "king")
                self.moveCast(MoveDirection.UPRIGHT, "king")
                self.moveCast(MoveDirection.DOWNLEFT, "king")
                self.moveCast(MoveDirection.DOWNRIGHT, "king")


    def moveCast(self,direction:MoveDirection,moveClass:str):
        """
        Auxilary method used by :py:meth:`calculateMoves()` to determine where each move location is.

        :param direction: Ordinal direction in which the moveCast is happening.
        :param moveClass: Type of Checker ("standard" or "king")
        """
        match direction:
            case MoveDirection.UPLEFT:
                first = MoveDirection.UPLEFT.value[0]
                xfirst = MoveDirection.UPLEFT.value[0] - 1
                second = MoveDirection.UPLEFT.value[1]
                xsecond = MoveDirection.UPLEFT.value[1] - 1
            case MoveDirection.UPRIGHT:
                first = MoveDirection.UPRIGHT.value[0]
                xfirst = MoveDirection.UPRIGHT.value[0] - 1
                second =  MoveDirection.UPRIGHT.value[1]
                xsecond =  MoveDirection.UPRIGHT.value[1] + 1
            case MoveDirection.DOWNLEFT:
                first = MoveDirection.DOWNLEFT.value[0]
                xfirst = MoveDirection.DOWNLEFT.value[0] + 1
                second = MoveDirection.DOWNLEFT.value[1]
                xsecond = MoveDirection.DOWNLEFT.value[1] - 1
            case MoveDirection.DOWNRIGHT:
                first = MoveDirection.DOWNRIGHT.value[0]
                xfirst = MoveDirection.DOWNRIGHT.value[0] + 1
                second = MoveDirection.DOWNRIGHT.value[1]
                xsecond = MoveDirection.DOWNRIGHT.value[1] + 1
        match moveClass:
            case "standard":
                if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                        self.board.checkerLocations[self.pos.first + first][self.pos.second + second] is None:
                    self.possibleMoves.append(CheckerMove(self.board.boardState[self.pos.first + first][self.pos.second + second],direction))
                elif 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                        self.board.checkerLocations[self.pos.first + first][
                            self.pos.second + second].color != self.color and 7 >= self.pos.first + xfirst >= 0 and 7 >= self.pos.second + xsecond >= 0 and \
                        self.board.checkerLocations[self.pos.first + xfirst][self.pos.second + xsecond] is None:
                    self.possibleMoves.append(CheckerMove(self.board.boardState[self.pos.first + xfirst][self.pos.second + xsecond],direction))
            case "king":
                while True:
                    if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                            self.board.checkerLocations[self.pos.first + first][self.pos.second + second] is None:
                        self.possibleMoves.append(CheckerMove(
                            self.board.boardState[self.pos.first + first][self.pos.second + second],direction))
                    else:
                        break

                    first = (first - 1) if first < 0 else first + 1
                    second = (second - 1) if second < 0 else second + 1

                xfirst = (first - 1) if first < 0 else first + 1
                xsecond = (second - 1) if second < 0 else second + 1

                if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                        self.board.checkerLocations[self.pos.first + first][
                            self.pos.second + second].color != self.color and 7 >= self.pos.first + xfirst >= 0 and 7 >= self.pos.second + xsecond >= 0 and \
                        self.board.checkerLocations[self.pos.first + xfirst][self.pos.second + xsecond] is None:
                    self.possibleMoves.append(CheckerMove(self.board.boardState[self.pos.first + xfirst][self.pos.second + xsecond],direction))



    def calculateKills(self):
        """Calculates which enemy checkers are available to kill."""
        self.possibleKills.clear()
        match self.direction:
            case CheckerDirection.UP:
                self.killCast(MoveDirection.UPLEFT,"standard")
                self.killCast(MoveDirection.UPRIGHT, "standard")
            case CheckerDirection.DOWN:
                self.killCast(MoveDirection.DOWNLEFT, "standard")
                self.killCast(MoveDirection.DOWNRIGHT, "standard")
            case CheckerDirection.KING:
                self.killCast(MoveDirection.UPLEFT, "king")
                self.killCast(MoveDirection.UPRIGHT, "king")
                self.killCast(MoveDirection.DOWNLEFT, "king")
                self.killCast(MoveDirection.DOWNRIGHT, "king")

    def killCast(self, direction:MoveDirection,killClass:str):
        """Auxilary method used by :py:meth:`calculateKills()` to determine where each kill location is."""
        match direction:
            case MoveDirection.UPLEFT:
                first = -1
                second = -1
            case MoveDirection.UPRIGHT:
                first = -1
                second = 1
            case MoveDirection.DOWNLEFT:
                first = 1
                second = -1
            case MoveDirection.DOWNRIGHT:
                first = 1
                second = 1
        match killClass:
            case "standard":
                if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                        self.board.checkerLocations[self.pos.first + first][self.pos.second + second] is not None and \
                        self.board.checkerLocations[self.pos.first + first][self.pos.second + second].color != self.color:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first + first][self.pos.second + second])
            case "king":
                while True:
                    if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0 and \
                            self.board.checkerLocations[self.pos.first + first][self.pos.second + second] is None:
                        pass
                    else:
                        break

                    first = (first - 1) if first < 0 else first + 1
                    second = (second - 1) if second < 0 else second + 1

                if 7 >= self.pos.first + first >= 0 and 7 >= self.pos.second + second >= 0:
                    self.possibleKills.append(self.board.checkerLocations[self.pos.first + first][self.pos.second + second])



    def moveHighlight(self, reset=False):
        """
        Highlights the squares that represent the moves you can do.

        :param reset: if True, the squares return to their default color.
        """
        if len(self.possibleMoves) == 0:
            return
        if reset:
            for x in self.possibleMoves:
                x.moveSquare.color = "black"
        else:
            for x in self.possibleMoves:
                x.moveSquare.color = "lightblue"

    def move(self, x: int, y: int):
        """
        Moves checker to location if it's included in the possible moves.

        :param x: attempted X location
        :param y: attempted Y location
        """
        moveSquares = list(map(lambda move: move.moveSquare,self.possibleMoves))
        if self.board.checkerLocations[y][x] is None and self.board.boardState[y][x] in [move.moveSquare for move in self.possibleMoves]:
            moveIndex = moveSquares.index(self.board.boardState[y][x])
            self.board.checkerLocations[self.pos.first][self.pos.second] = None
            self.board.checkerLocations[y][x] = self
            self.lastPos = Pair(self.pos.first, self.pos.second)
            self.lastMove = self.possibleMoves[moveIndex]
            self.pos.first = y
            self.pos.second = x
            self.moveHighlight(True)
            for i in self.possibleKills:
                if i.pos == self.pos + -self.lastMove.moveDirection:
                    self.board.checkerLocations[i.pos.first][i.pos.second] = None

            if (self.playerID == inGameState.PLAYERONE and self.pos.first == 0) or (self.playerID == inGameState.PLAYERTWO and self.pos.first == 7):
                self.direction = CheckerDirection.KING
            return True