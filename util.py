import json
import os
import sys
from enum import Enum, IntEnum

import pygame
from pygame import Surface, Color
from pygame import system

import ast

def parse_tuple(string):
    try:
        s = ast.literal_eval(str(string))
        if type(s) == tuple:
            return s
        return
    except:
        return

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

class MoveDirection(Enum):
    """The directions that a checker can move. \"UPLEFT\", \"UPRIGHT\", \"DOWNLEFT\", \"DOWNRIGHT\" """
    UPLEFT = (-1,-1)
    UPRIGHT = (-1,1)
    DOWNLEFT = (1,-1)
    DOWNRIGHT = (1,1)

    def __neg__(self):
        return -self.value[0],-self.value[1]

class CheckerMove:
    def __init__(self,square,coords:Pair,direction:MoveDirection,moveType:str,parentMove=None):
        self.moveSquare = square
        self.moveDirection = direction
        self.moveType = moveType
        self.coords = coords
        self.kill = None
        self.parentMove = parentMove

    def __str__(self):
        return "Move Square - " + str(self.moveSquare) + ", Move Direction: " + str(self.moveDirection) + ", Move Type: " + self.moveType + ", Kill Target: " + str(self.kill)

    def __repr__(self):
        return self.__str__()


class inGameState(IntEnum):
    PLAYERONE = 1
    PLAYERTWO = 2

class GameState(IntEnum):
    MENU = 1
    SETTINGS = 2
    INGAME = 3
    GAMEOVER = 4

class Settings:
    checkerColorOne = Color("red")
    checkerColorTwo = Color("white")
    squareColorOne = Color("black")
    squareColorTwo = Color("white")
    writepath = pygame.system.get_pref_path("PyGames", "PyCheckers")

    if not os.path.isfile(writepath+"/settings.json"):
        with open(writepath+"/settings.json","w") as f:
            option_dict = {"colors": {"checkerColorOne":'["255","0","0"]',
                                      "checkerColorTwo":'["255","255","255"]',
                                      "squareColorOne":'["0","0","0"]',
                                      "squareColorTwo":'["255","255","255"]'
            }}
            json.dump(option_dict,f,indent=4)

    @classmethod
    def loadSettings(cls):
        with open(cls.writepath + "/settings.json", "r") as f:
            option_dict = json.load(f)

        cls.checkerColorOne = Color([int(n) for n in ast.literal_eval(option_dict["colors"]["checkerColorOne"])])
        cls.checkerColorTwo = Color([int(n) for n in ast.literal_eval(option_dict["colors"]["checkerColorTwo"])])
        cls.squareColorOne = Color([int(n) for n in ast.literal_eval(option_dict["colors"]["squareColorOne"])])
        cls.squareColorTwo = Color([int(n) for n in ast.literal_eval(option_dict["colors"]["squareColorTwo"])])

    @classmethod
    def saveSettings(cls):
        with open(cls.writepath + "/settings.json", "w") as f:
            option_dict = {"colors": {"checkerColorOne": str(list(cls.checkerColorOne)),
                                      "checkerColorTwo": str(list(cls.checkerColorTwo)),
                                      "squareColorOne": str(list(cls.squareColorOne)),
                                      "squareColorTwo": str(list(cls.squareColorTwo))
                                      }}
            json.dump(option_dict, f, indent=4)









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

def borderedColorSquare(surface,mainColor,x,y,width,height,borderColor=None,borderwidth=0,borderradius=0):
    if borderColor:
        borderX = borderwidth*2
        borderRect = pygame.Rect(x,y,width,height)
        colorRect = pygame.Rect(x+borderwidth,y+borderwidth,width-borderX,height-borderX)
        pygame.draw.rect(surface,borderColor,borderRect,border_radius=borderradius)
        pygame.draw.rect(surface,mainColor,colorRect)
    else:
        colorRect = pygame.Rect(x,y,width,height)
        pygame.draw.rect(surface,mainColor,colorRect)
    return colorRect
