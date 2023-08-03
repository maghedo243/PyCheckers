import pygame
from pygame import Rect, Color

from boardUtils import Board, Checker, CheckerDirection
from util import Pair, inGameState

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 500))
boardSurface = pygame.Surface((400,400))
clock = pygame.time.Clock()
running = True
dt = 0
boole = True
board = Board()
board.defaultBoardLayout("red","white")
selectedChecker = None
currentTurn = inGameState.PLAYERONE
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
                        print("White exists?",board.playerSearch(2))
                        print("Cell Color:",cell.color)
                        print("Cell Location:",y,x)
                        print("Selected Checker Location:", selectedChecker.pos if selectedChecker is not None else "No Checker Selected")
                        print("Selected Checker Possible Kills:", selectedChecker.possibleKills.__len__() if selectedChecker is not None else "No Checker Selected")
                        if board.checkerLocations[y][x] is not None:
                            if selectedChecker is not None and board.checkerLocations[y][x].playerID == selectedChecker.playerID:
                                print("New Checker Selected")
                                selectedChecker.selected = False
                                selectedChecker.moveHighlight(True)
                                selectedChecker = board.checkerLocations[y][x]
                                selectedChecker.selected = True
                            elif selectedChecker is None and board.checkerLocations[y][x].playerID == currentTurn:
                                selectedChecker = board.checkerLocations[y][x]
                                selectedChecker.selected = True
                        elif selectedChecker is not None:
                            if selectedChecker.move(x, y):
                                match currentTurn:
                                    case inGameState.PLAYERONE:
                                        currentTurn = inGameState.PLAYERTWO
                                    case inGameState.PLAYERTWO:
                                        currentTurn = inGameState.PLAYERONE
                                selectedChecker.selected = False
                                selectedChecker = None

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkgray")

    mouseBox.center = pygame.mouse.get_pos()
    textFont = pygame.font.SysFont("monospace", 15)
    turnText = textFont.render("Turn:",1,(255,255,255,0))
    turnSquare = Rect(204,429,30,30)
    turnSquareBorder = Rect(200,425,38,38)

    board.drawBoard(boardSurface)

    screen.blit(boardSurface,(0,0))
    screen.blit(turnText,(150,430))
    pygame.draw.rect(screen, Color(255,255,255,0), mouseBox)
    pygame.draw.rect(screen,"lightgray", turnSquareBorder,border_radius=6)
    pygame.draw.rect(screen,"white" if currentTurn == inGameState.PLAYERTWO else "red",turnSquare)
    # flip() the display to put your work on screen
    pygame.display.flip()

    if not board.playerSearch(1):
        print(board.twoColor.capitalize(),"Wins")
        running = False
    elif not board.playerSearch(2):
        print(board.oneColor.capitalize(),"Wins")
        running = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()