import pygame
from pygame import Rect, Color
from pygame_menu import themes

from boardUtils import Board
from util import inGameState
import util
from boardUtils import Board, Checker, CheckerDirection
from util import Pair, inGameState, GameState

import pygame_menu

#initial game setup
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("PyCheckers")
boardSurface = pygame.Surface((400,400))
winSurface = pygame.Surface((350,350))
winSurface.fill("blue")
winSurface.set_alpha(0)
util.surfaceBorder(winSurface,10,"black")
clock = pygame.time.Clock()
running = True
dt = 0
boole = True
board = Board()
board.defaultBoardLayout("red","white")
selectedChecker = None
currentTurn = inGameState.PLAYERONE
gameState = GameState.INGAME
mouseBox = Rect(0,0,1,1)

mainmenu = pygame_menu.Menu('Welcome', 400, 500,
                                 theme=themes.THEME_SOLARIZED)
mainmenu.add.button('Play', mainmenu.disable)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

while running:
    if selectedChecker is not None:
        selectedChecker.calculateMoves()
        selectedChecker.moveHighlight()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == GameState.INGAME: #Board Click Check
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

    #game ui and game creation
    if not mainmenu.is_enabled():
        mouseBox.center = pygame.mouse.get_pos()
        textFont = pygame.font.SysFont("monospace", 15)
        turnText = textFont.render("Turn:",1,(255,255,255,0))
        turnSquare = Rect(204,429,30,30)
        turnSquareBorder = Rect(200,425,38,38)

        board.drawBoard(boardSurface)

        screen.blits(((boardSurface,(0,0)),(turnText,(150,430)),(winSurface,(25,75))))
        pygame.draw.rect(screen, Color(255,255,255,0), mouseBox)
        pygame.draw.rect(screen,"lightgray", turnSquareBorder,border_radius=6)
        pygame.draw.rect(screen,"white" if currentTurn == inGameState.PLAYERTWO else "red",turnSquare)

    #menu draw
    if mainmenu.is_enabled():
        mainmenu.update(events)
        if mainmenu.is_enabled():
            mainmenu.draw(screen)

    # win check
    if not board.playerSearch(1):
        print(board.twoColor.capitalize(),"Wins")
        running = False
    elif not board.playerSearch(2):
        print(board.oneColor.capitalize(),"Wins")
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()



    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()