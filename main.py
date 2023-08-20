import pygame
from pygame import Rect

import util
from boardUtils import Board
from util import inGameState, GameState, get_path

import pygame_gui

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

gameState = GameState.MENU
oneImage = pygame.image.load(get_path("resources/images/playerone.png"))
oneImage = pygame.transform.smoothscale(oneImage,(300,49))
twoImage = pygame.image.load(get_path("resources/images/playertwo.png"))
twoImage = pygame.transform.smoothscale(twoImage,(300,49))
winImage = pygame.image.load(get_path("resources/images/wins.png"))
winImage = pygame.transform.smoothscale(winImage,(145,49))

textFont = pygame.font.SysFont("monospace", 15)
winFont = pygame.font.SysFont("monospace", 30)

def gameInit(newboard: Board,oneColor,twoColor):
    newboard.defaultBoardLayout(oneColor,twoColor)
    return [None,inGameState.PLAYERONE]

running = True
dt = 0
board = Board()
selectedChecker, currentTurn = gameInit(board,"red","white")
background = pygame.Surface((400,500))
background.fill("lightgray")

#mainmenu setup
mainMenuManager = pygame_gui.UIManager((400,500))
mainMenu = pygame_gui.core.UIContainer(relative_rect=screen.get_rect(),
                                       manager=mainMenuManager)
startButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (300, 50)),
                                            text='Play',
                                            manager=mainMenuManager,
                                            container=mainMenu,
                                            anchors={'centerx': 'centerx'})

quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,10),(300,50)),
                                          text='Quit',
                                          manager=mainMenuManager,
                                          container=mainMenu,
                                          anchors={'centerx': 'centerx',
                                                   'top_target': startButton})

#winmenu setup
winMenuManager = pygame_gui.UIManager(screen.get_size())
winMenu = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((25,75),winSurface.get_size()),
                                      manager=winMenuManager)
replayButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 180), (300, 50)),
                                             text='Replay',
                                             manager=winMenuManager,
                                            container=winMenu,
                                           anchors={'centerx': 'centerx'})

menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 240), (300, 50)),
                                             text='Return to Menu',
                                             manager=winMenuManager,
                                            container=winMenu,
                                           anchors={'centerx': 'centerx'})

winMenu.disable()

while running:
    if selectedChecker is not None:
        selectedChecker.calculateMoves()
        selectedChecker.moveHighlight()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        mainMenuManager.process_events(event)
        winMenuManager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                gameState = GameState.INGAME
                mainMenu.disable()
            elif event.ui_element == quitButton:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.ui_element == replayButton:
                print("Restart")
                selectedChecker, currentTurn = gameInit(board, board.oneColor, board.twoColor)
                winMenu.disable()
                winSurface.set_alpha(0)
                gameState = GameState.INGAME
            elif event.ui_element == menuButton:
                winMenu.disable()
                winSurface.set_alpha(0)
                mainMenu.enable()
                gameState = GameState.MENU
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == GameState.INGAME: #Board Click Check
                for y,rows in enumerate(board.boardState):
                    for x,cell in enumerate(rows):
                        if cell.hitbox.collidepoint(event.pos):
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

    mainMenuManager.update(dt)
    winMenuManager.update(dt)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkgray")


    #game ui and game creation
    match gameState:
        case GameState.MENU: #menu draw
            screen.blit(background, (0, 0))
            mainMenuManager.draw_ui(screen)
        case GameState.INGAME | GameState.GAMEOVER: #visual game process
            turnText = textFont.render("Turn:",1,(255,255,255,0))
            turnSquare = Rect(204,429,30,30)
            turnSquareBorder = Rect(200,425,38,38)

            board.drawBoard(boardSurface)

            screen.blits(((boardSurface,(0,0)), (turnText,(150,430)), (winSurface,(25,75))))
            pygame.draw.rect(screen,"lightgray", turnSquareBorder,border_radius=6)
            pygame.draw.rect(screen,"white" if currentTurn == inGameState.PLAYERTWO else "red",turnSquare)

            if gameState == GameState.GAMEOVER:
                winMenuManager.draw_ui(screen)
                match wincheck:
                    case 1:
                        oneImage.fill(board.oneColor, special_flags=pygame.BLEND_ADD)
                        winImage.fill(board.oneColor, special_flags=pygame.BLEND_ADD)
                        winSurface.blits(((oneImage, (25, 50)),(winImage,(102.5,110))))
                    case 2:
                        twoImage.fill(board.twoColor, special_flags=pygame.BLEND_ADD)
                        winImage.fill(board.twoColor, special_flags=pygame.BLEND_ADD)
                        winSurface.blits(((twoImage, (25, 50)),(winImage,(102.5,110))))
                    case _:
                        raise Exception("WINVALUE ERROR")
                winSurface.set_alpha(255)

            else: #win checking
                wincheck = board.winCheck()
                if wincheck:
                    winMenu.enable()
                    gameState = GameState.GAMEOVER

    pygame.display.flip()



    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()