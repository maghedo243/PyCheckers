import pygame
from pygame import Rect, Color

from boardUtils import Board, Checker, CheckerDirection
from util import Pair

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500),pygame.RESIZABLE)
boardSurface = pygame.Surface((400,400))
clock = pygame.time.Clock()
running = True
dt = 0
boole = True
board = Board()
board.defaultBoardLayout()
selectedChecker = None
currentTurn = "red"
mouseBox = Rect(0,0,1,1)


while running:
    if selectedChecker is not None:
        selectedChecker.calculateMoves()
        selectedChecker.moveHighlight()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for y,rows in enumerate(board.boardState):
                for x,cell in enumerate(rows):
                    if mouseBox.colliderect(cell.hitbox):
                        print("Cell Color:",cell.color)
                        print("Cell Location:",y,x)
                        print("Selected Checker Location:", selectedChecker.pos if selectedChecker is not None else "No Checker Selected")
                        print("Selected Checker Possible Kills:", selectedChecker.possibleKills.__len__() if selectedChecker is not None else "No Checker Selected")
                        if board.checkerLocations[y][x] is not None:
                            if selectedChecker is not None and board.checkerLocations[y][x].color == selectedChecker.color:
                                print("New Checker Selected")
                                selectedChecker.selected = False
                                selectedChecker.moveHighlight(True)
                                selectedChecker = board.checkerLocations[y][x]
                                selectedChecker.selected = True
                            elif selectedChecker is None and board.checkerLocations[y][x].color == currentTurn:
                                selectedChecker = board.checkerLocations[y][x]
                                selectedChecker.selected = True
                        elif selectedChecker is not None:
                            if selectedChecker.move(x, y):
                                match currentTurn:
                                    case "red":
                                        currentTurn = "white"
                                    case "white":
                                        currentTurn = "red"
                                selectedChecker.selected = False
                                selectedChecker = None



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white") if currentTurn == "white" else screen.fill("red")

    mouseBox.center = pygame.mouse.get_pos()

    board.drawBoard(boardSurface)



    screen.blit(boardSurface,(0,0))
    pygame.draw.rect(screen, Color(255,255,255,0), mouseBox)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()