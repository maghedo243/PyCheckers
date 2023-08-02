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
selectedChecker = board.defaultBoardLayout()
selectedChecker.selected = True
mouseBox = Rect(0,0,1,1)


while running:
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
                        print("Selected Checker Location:", selectedChecker.pos)
                        print("Selected Checker Possible Kills:", selectedChecker.possibleKills.__len__())
                        selectedChecker.move(x, y)
                        if board.checkerLocations[y][x] is not None and board.checkerLocations[y][x].color == selectedChecker.color:
                            print("New Checker Selected")
                            selectedChecker.selected = False
                            selectedChecker.moveHighlight(True)
                            selectedChecker = board.checkerLocations[y][x]
                            selectedChecker.selected = True



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    mouseBox.center = pygame.mouse.get_pos()

    board.drawBoard(boardSurface)

    selectedChecker.calculateMoves()

    screen.blit(boardSurface,(0,0))
    pygame.draw.rect(screen, Color(255,255,255,0), mouseBox)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()