from tkinter.colorchooser import askcolor
import pygame
import pygame.gfxdraw
from pygame import Rect, Color, Surface

import util
from boardUtils import Board
from util import inGameState, GameState, Settings

import pygame_gui

#initial game setup
Settings.loadSettings()
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("PyCheckers")
boardSurface = pygame.Surface((400,400))
clock = pygame.time.Clock()

#pausemenu surface
pauseSurface = pygame.Surface((350,350))
pauseSurface.fill("blue")
pauseSurface.set_alpha(0)
util.surfaceBorder(pauseSurface,10,"black")

#winmenu surface
winSurface = pygame.Surface((350,350))
winSurface.fill("blue")
winSurface.set_alpha(0)
util.surfaceBorder(winSurface,10,"black")


gameState = GameState.MENU
oneImage = util.getImage("resources/images/playerone.png",(300,49))
twoImage = util.getImage("resources/images/playertwo.png",(300,49))
winImage = util.getImage("resources/images/wins.png",(145,49))
logo = util.getImage("resources/images/pycheckers.png",(370,69))
settingsImg = util.getImage("resources/images/settings.png", (350, 85))

textFont = pygame.font.SysFont("monospace", 15)
winFont = pygame.font.SysFont("monospace", 30)

def gameInit(newboard: Board):
    newboard.clear()
    newboard.defaultBoardLayout()
    oneImage.fill(newboard.oneColor, special_flags=pygame.BLEND_MAX)
    twoImage.fill(newboard.twoColor, special_flags=pygame.BLEND_MAX)
    return [None,inGameState.PLAYERONE]

running = True
dt = 0
board = Board()
selectedChecker, currentTurn = gameInit(board)
background = pygame.Surface(screen.get_size())
background.fill("darkolivegreen4")

#mainmenu setup
mainMenuManager = pygame_gui.UIManager(screen.get_size())
mainMenu = pygame_gui.core.UIContainer(relative_rect=screen.get_rect(),
                                       manager=mainMenuManager)
startButton = pygame_gui.elements.UIButton(relative_rect=Rect((0, 150), (300, 50)),
                                            text='Play',
                                            manager=mainMenuManager,
                                            container=mainMenu,
                                            anchors={'centerx': 'centerx'})

settingsButton = pygame_gui.elements.UIButton(relative_rect=Rect((0,10),(300,50)),
                                          text='Settings',
                                          manager=mainMenuManager,
                                          container=mainMenu,
                                          anchors={'centerx': 'centerx',
                                                   'top_target': startButton})

quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,10),(300,50)),
                                          text='Quit',
                                          manager=mainMenuManager,
                                          container=mainMenu,
                                          anchors={'centerx': 'centerx',
                                                   'top_target': settingsButton})


#settingsmenu setup
previewBoard = Board()
previewBoard.defaultBoardLayout()
settingsMenuManager = pygame_gui.UIManager(screen.get_size())
settingsMenu = pygame_gui.core.UIContainer(relative_rect=screen.get_rect(),
                                       manager=settingsMenuManager)
colorDropdownText = pygame_gui.elements.UILabel(Rect(40,200,110,25),
                                                "Color Choice:",
                                                manager=settingsMenuManager,
                                                container=settingsMenu)
colorDropdown = pygame_gui.elements.UIDropDownMenu(["Player One Color","Player Two Color","Primary Square Color","Secondary Square Color"],
                                                   "Player One Color",
                                                   relative_rect=Rect(0,colorDropdownText.relative_rect.y,210,25),
                                                   manager=settingsMenuManager,
                                                   container=settingsMenu,
                                                   anchors={'left_target':colorDropdownText})
colorOption = colorDropdown.selected_option
colorChoiceButton = pygame_gui.elements.UIButton(relative_rect=Rect(100,250,100,30),
                                                 text="Choose",
                                                 manager=settingsMenuManager,
                                                 container=settingsMenu)
previewLabel = pygame_gui.elements.UILabel(Rect(185,290,150,40),
                                                "Board Preview:",
                                                manager=settingsMenuManager,
                                                container=settingsMenu)
settingsConfirmButton = pygame_gui.elements.UIButton(relative_rect=Rect(27,330,150,40),
                                                     text="Save and Exit",
                                                     manager=settingsMenuManager,
                                                     container=settingsMenu)
settingsExitButton = pygame_gui.elements.UIButton(relative_rect=Rect(7,380,190,40),
                                                     text="Exit without saving",
                                                     manager=settingsMenuManager,
                                                     container=settingsMenu)

#gamemenu setup
gameMenuManager = pygame_gui.UIManager(screen.get_size())
gameMenu = pygame_gui.core.UIContainer(relative_rect=Rect(0,400,400,100),
                                       manager=gameMenuManager)
pauseButton = pygame_gui.elements.UIButton(relative_rect=Rect(0, 75, 75, 25),
                                           text="Pause",
                                           manager=gameMenuManager,
                                           container=gameMenu)

#pausemenu setup
pauseMenuManager = pygame_gui.UIManager(screen.get_size())

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

gameMenu.disable()
settingsMenu.disable()
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
        settingsMenuManager.process_events(event)
        gameMenuManager.process_events(event)
        winMenuManager.process_events(event)


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == startButton:
                Settings.loadSettings()
                selectedChecker, currentTurn = gameInit(board)
                gameState = GameState.INGAME
                mainMenu.disable()
                gameMenu.enable()
            elif event.ui_element == settingsButton:
                mainMenu.disable()
                settingsMenu.enable()
                gameState = GameState.SETTINGS
            elif event.ui_element == settingsExitButton:
                Settings.loadSettings()
                settingsMenu.disable()
                mainMenu.enable()
                gameState = GameState.MENU
            elif event.ui_element == settingsConfirmButton:
                Settings.saveSettings()
                settingsMenu.disable()
                mainMenu.enable()
                gameState = GameState.MENU
            elif event.ui_element == quitButton:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.ui_element == replayButton:
                selectedChecker, currentTurn = gameInit(board)
                winMenu.disable()
                winSurface.fill("blue")
                winSurface.set_alpha(0)
                util.surfaceBorder(winSurface, 10, "black")
                gameState = GameState.INGAME
            elif event.ui_element == menuButton:
                winMenu.disable()
                winSurface.fill("blue")
                winSurface.set_alpha(0)
                util.surfaceBorder(winSurface, 10, "black")
                mainMenu.enable()
                gameState = GameState.MENU
            elif event.ui_element == pauseButton:
                gameMenu.disable()
                mainMenu.enable()
                gameState = GameState.MENU
            elif event.ui_element == colorChoiceButton:
                colorChoice = askcolor(title="Choose Color")[0]
                if colorChoice:
                    colorChoice = Color(colorChoice)
                    match colorDropdown.selected_option:
                        case "Player One Color": Settings.checkerColorOne = colorChoice
                        case "Player Two Color": Settings.checkerColorTwo = colorChoice
                        case "Primary Square Color": Settings.squareColorOne = colorChoice
                        case "Secondary Square Color": Settings.squareColorTwo = colorChoice
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == colorDropdown:
                colorOption = colorDropdown.selected_option
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == GameState.INGAME: #Board Click Check
                for y,rows in enumerate(board.boardState):
                    for x,cell in enumerate(rows):
                        if cell.hitbox.collidepoint(event.pos):
                            print("Cell Color:",cell.color)
                            print("Cell Location:",y,x)
                            print("Selected Checker Location:", selectedChecker.pos if selectedChecker is not None else "No Checker Selected")
                            print("Selected Checker Possible Kills:", selectedChecker.possibleKills.__len__() if selectedChecker is not None else "No Checker Selected")
                            if board.checkerLocations[y][x] is not None:
                                if selectedChecker is not None and board.checkerLocations[y][x].playerID == selectedChecker.playerID:
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
    settingsMenuManager.update(dt)
    gameMenuManager.update(dt)
    winMenuManager.update(dt)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkgray")


    #game ui and game creation
    match gameState:
        case GameState.MENU: #main menu draw
            screen.blit(background, (0, 0))
            screen.blit(logo,(15,50))
            mainMenuManager.draw_ui(screen)
        case GameState.SETTINGS: #settings menu draw
            match colorOption:
                case "Player One Color": settingsOptionColor = Settings.checkerColorOne
                case "Player Two Color": settingsOptionColor = Settings.checkerColorTwo
                case "Primary Square Color": settingsOptionColor = Settings.squareColorOne
                case "Secondary Square Color": settingsOptionColor = Settings.squareColorTwo

            previewSpace = Surface((160, 160))
            previewBoard.defaultBoardLayout()
            previewBoard.drawBoard(previewSpace)

            screen.blit(background, (0, 0))
            screen.blit(settingsImg, (25, 40))
            util.borderedColorSquare(screen, settingsOptionColor, 220, colorChoiceButton.relative_rect.y-10 , 50, 50, "gray", 4, 4)
            previewRect = util.borderedColorSquare(screen, "white", 200,320,170,170,"gray",5,4)

            screen.blit(previewSpace,previewRect)

            settingsMenuManager.draw_ui(screen)
        case GameState.INGAME | GameState.GAMEOVER: #visual game process
            turnText = textFont.render("Turn:",1,(255,255,255,0))
            turnColor = board.twoColor if currentTurn == inGameState.PLAYERTWO else board.oneColor

            board.drawBoard(boardSurface)

            screen.blits(((boardSurface,(0,0)), (turnText,(150,430)), (winSurface,(25,75))))
            util.borderedColorSquare(screen,turnColor,200,425,38,38,"lightgray",4,6)

            if gameState == GameState.GAMEOVER:
                winMenuManager.draw_ui(screen)
                match wincheck:
                    case 1:
                        winImage.fill(board.twoColor, special_flags=pygame.BLEND_SUB)
                        winImage.fill(board.oneColor, special_flags=pygame.BLEND_ADD)
                        winSurface.blits(((oneImage, (25, 50)),(winImage,(102.5,110))))
                    case 2:
                        winImage.fill(board.oneColor, special_flags=pygame.BLEND_SUB)
                        winImage.fill(board.twoColor, special_flags=pygame.BLEND_ADD)
                        winSurface.blits(((twoImage, (25, 50)),(winImage,(102.5,110))))
                    case _:
                        raise Exception("WINVALUE ERROR")
                winSurface.set_alpha(255)

            else: #win checking
                gameMenuManager.draw_ui(screen)
                wincheck = board.winCheck()
                if wincheck:
                    gameMenu.disable()
                    winMenu.enable()
                    gameState = GameState.GAMEOVER

    pygame.display.flip()



    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()