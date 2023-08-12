from enum import Enum, IntEnum

import pygame
from pygame import Surface


class Pair:
    def __init__(self,first,second):
        self.first = first
        self.second = second

    def __str__(self):
        return "(" + str(self.first) + "," + str(self.second) + ")"

    def __add__(self, other):
        if isinstance(other,Pair):
            newFirst = int((self.first + other.first) / 2)
            newSecond = int((self.second + other.second) / 2)
            return Pair(newFirst,newSecond)

    def __eq__(self,other):
        if isinstance(other, Pair):
            if other.first == self.first and other.second == self.second:
                return True
        return False

class inGameState(IntEnum):
    PLAYERONE = 1
    PLAYERTWO = 2

class GameState(IntEnum):
    MENU = 1
    INGAME = 2

def surfaceBorder(surface: Surface,thickness: int,color):
    widthIndex = (thickness/(thickness-2)) if (thickness-2 > 0) else 0
    xLimit = surface.get_width()-widthIndex
    yLimit = surface.get_height()-widthIndex
    pygame.draw.lines(surface, color, True, [(widthIndex,widthIndex),(widthIndex,yLimit),(xLimit,yLimit),(xLimit,widthIndex)],thickness)


