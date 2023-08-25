import os
import sys
from enum import Enum, IntEnum

import pygame
from pygame import Surface


class Pair:
    def __init__(self,first,second):
        self.first = first
        self.second = second

    def __str__(self):
        return "(" + str(self.first) + "," + str(self.second) + ")"

    def __add__(self,other):
        if isinstance(other, Pair):
            return Pair(self.first+other.first,self.second+other.second)
        elif isinstance(other,tuple):
            return Pair(self.first+other[0],self.second+other[1])
        return False

    def __mul__(self, other):
        if isinstance(other,Pair):
            newFirst = int((self.first + other.first) / 2)
            newSecond = int((self.second + other.second) / 2)
            return Pair(newFirst,newSecond)

    def __eq__(self,other):
        if isinstance(other, Pair):
            if other.first == self.first and other.second == self.second:
                return True
        elif isinstance(other,tuple):
            if other.__len__() == 2:
                if other[0] == self.first and other[1] == self.second:
                    return True
        return False

class CheckerMove:
    def __init__(self,square,direction):
        self.moveSquare = square
        self.moveDirection = direction


class inGameState(IntEnum):
    PLAYERONE = 1
    PLAYERTWO = 2

class GameState(IntEnum):
    MENU = 1
    INGAME = 2
    GAMEOVER = 3

def surfaceBorder(surface: Surface,thickness: int,color):
    widthIndex = (thickness/(thickness-2)) if (thickness-2 > 0) else 0
    xLimit = surface.get_width()-widthIndex
    yLimit = surface.get_height()-widthIndex
    pygame.draw.lines(surface, color, True, [(widthIndex,widthIndex),(widthIndex,yLimit),(xLimit,yLimit),(xLimit,widthIndex)],thickness)


def get_path(relative_path):
    """
    Finds path to file relative to the runtime.

    :param relative_path: pathstring
    :return: runtime filepath
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.normpath(os.path.join(base_path, relative_path))

def getImage(path:str, newScale:tuple=None):
    """
    Gets image from path and resizes it if necessary

    :param path: path to image file
    :param newScale: scale to set on image (default: None)
    :return: image Surface
    """
    image = pygame.image.load(get_path(path))
    if newScale != None:
        image = pygame.transform.smoothscale(image,newScale)
    return image
