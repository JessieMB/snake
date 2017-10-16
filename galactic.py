import random, pygame, sys, tkinter
from pygame.locals import *

FPS = 10 #Number of frames per second the game plays at; This could be changed to accommodate difficulty levels within the game
WINDOWWIDTH = 1000
WINDOWHEIGHT = 680
CELLSIZE = 40 #Size of cell 
assert WINDOWWIDTH % CELLSIZE == 0, "Window width needs to be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height needs to be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#RGB colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
PURPLE    = ( 139,  0, 139)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


earth = pygame.image.load("earths.jpg")
galaxy = pygame.image.load("galaxy.jpg")

UNIVERSELIST = [galaxy, earth]
background = random.choice(UNIVERSELIST)

BACKGROUND = background
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # Head of player

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    
    surface = pygame.image.load("favicon.ico")
    pygame.display.set_icon(surface)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Galactic Attack')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    playerCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Place food in random space
    food = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the player has hit itself or the edge
        if playerCoords[HEAD]['x'] == -1 or playerCoords[HEAD]['x'] == CELLWIDTH or playerCoords[HEAD]['y'] == -1 or playerCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for playerBody in playerCoords[1:]:
            if playerBody['x'] == playerCoords[HEAD]['x'] and playerBody['y'] == playerCoords[HEAD]['y']:
                return # game over

        # check if player has eaten the food
        if playerCoords[HEAD]['x'] == food['x'] and playerCoords[HEAD]['y'] == food['y']:
            # don't remove player's tail segment
            food = getRandomLocation() # set a new food somewhere
        else:
            del playerCoords[-1] # remove player's tail segment

        # move the player by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': playerCoords[HEAD]['x'], 'y': playerCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': playerCoords[HEAD]['x'], 'y': playerCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': playerCoords[HEAD]['x'] - 1, 'y': playerCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': playerCoords[HEAD]['x'] + 1, 'y': playerCoords[HEAD]['y']}
        playerCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawplayer(playerCoords)
        drawfood(food)
        drawScore(len(playerCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('GALACTIC', True, WHITE, BLACK)
    titleSurf2 = titleFont.render('ATTACK!', True, PURPLE)
    degrees1 = 0
    degrees2 = 0
    while True:
        
        DISPLAYSURF.blit(random.choice(UNIVERSELIST), [0,0])
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('RIP!', True, WHITE)
    overSurf = gameOverFont.render(':(', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            
            return

def drawScore(score):
    time = pygame.time.get_ticks()
    footprint = score/time
    timeSurf = BASICFONT.render('Light years traveled: %s'% (time), True, WHITE)
    scoreSurf = BASICFONT.render('Galaxies saved: %s'% (score), True, WHITE)
    footprintSurf = BASICFONT.render('Universal footprint: %s' % (footprint), True, WHITE)
    
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (WINDOWWIDTH -350, 10)
    DISPLAYSURF.blit(timeSurf, timeRect)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-350, 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    footRect = footprintSurf.get_rect()
    footRect.topleft = (WINDOWWIDTH -350, 70)
    DISPLAYSURF.blit(footprintSurf, footRect)

def drawplayer(playerCoords):
    moe = pygame.image.load('moe.jpg')
    
    spriteList = [moe]
    
    for coord in playerCoords:
        randomSprite = random.choice(spriteList)
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        DISPLAYSURF.blit(randomSprite, (x, y))   
        #playerSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        #pygame.draw.rect(DISPLAYSURF, DARKGREEN, playerSegmentRect)
        #playerInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        #pygame.draw.rect(DISPLAYSURF, GREEN, playerInnerSegmentRect)


def drawfood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    #catfood = pygame.image.load('catfood.png')
    #tuna = pygame.image.load('tuna.png')
    #chicken = pygame.image.load('chicken.png')
    #ham = pygame.image.load('ham.png')
    #pencil = pygame.image.load('pencil.gif')
    planet = pygame.image.load('planet.jpg')
    #goodieList = [catfood, tuna, chicken, ham, pencil]    
    #food = random.choice(goodieList)  
    
   #foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    DISPLAYSURF.blit(planet, (x,y))

#def selectGoodie():
    #catfood = pygame.image.load('catfood.png')
    #tuna = pygame.image.load('tuna.png')
    #chicken = pygame.image.load('chicken.png')
    #ham = pygame.image.load('ham.png')
    #pencil = pygame.image.load('pencil.gif')
    
    #goodieList = [catfood, tuna, chicken, ham, pencil]
    
    #return(random.choice(goodieList))
    
    

def drawGrid():
    
    #galaxy = pygame.image.load("galaxy.png")

    DISPLAYSURF.blit(BACKGROUND, [0,0])
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()