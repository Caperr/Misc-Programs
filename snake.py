#import game modules
import pygame
import time
import random

#initialize pygame
#note: init() will return a count of successful and failed module initializations. e.g x = pygame.init()
pygame.init()

#initialize colours using RGB touples.
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)
yellow = (255,255,0)

#Game window size and centre.
windowWidth = 800
windowHeight = 600
centre = [windowWidth/2, windowHeight/2]

#set up the game window
window =  pygame.display.set_mode((windowWidth,windowHeight))
#set the window title
pygame.display.set_caption("Snake")

#Update the display (moved into the game loop)
#pygame.display.update()
#an alternate update function:
#pygame.display.flip()
#update will update objects you define, unless you don't give it any objects to update (where it will update all available objects)
#flip will update all available objects.

#define a game clock variable for
gameClock = pygame.time.Clock()
#The size of each block of the snake
snakeSize = 10
#The rate at which the game updates the graphics
FPS = 30

#Get the game's main font for text from pygame. 25 is the font size.
font = pygame.font.SysFont(None, 25)

#show some text on the screen. Text is the text to show, colour is the colour of the text.
def showText(text, colour, position):
    #Render the text stored in "text", with antialiasing, and with colour "colour"
    shownText = font.render(text, True, colour)
    #Place the rendered text in the centre of the screen. co-ords passed as array. Remember to update after.
    window.blit(shownText, position)
    #pygame.display.update()!!

#generate a random position for an apple
def makeApple():
    #using -snakeSize because the apple could potentially go partially offscreen otherwise, since it's not a single pixel.
    #round the x co-rds to the nearest 10 in order to make sure it will always align with the snake perfectly
    appleX = round(random.randrange(0,windowWidth - snakeSize)/10.0)*10.0
    appleY = round(random.randrange(0,windowHeight - snakeSize)/10.0)*10.0
    return appleX, appleY

#Draw the snake blocks
def drawSnake(bodyList):
    for XY in bodyList:
        pygame.draw.rect(window, black, [XY[0],XY[1],snakeSize,snakeSize])

def doubleScore(addScore, double, doubles):
    if double:
        return 3, doubleScore*2
    elif doubles != 0:
        return doubles-1, addScore*2
    else:
        return 0, addScore

def gameLoop():
    #track whether the game has ended
    gameStop = False
    #Track whether the game is quitting
    gameQuit = False

    #Whether double score is active
    double = False
    #How many double score apples are left
    doubles = 0
    #how many apples until a double score
    nextDouble = random.randint(1,7)
    #coords
    doubleX, doubleY = makeApple()
    
    #Score
    score = 0
    #Score to add per apple
    addScore = 20
    
    #Variables to hold the co-ords of the head block. May change this to array later.
    headX = windowWidth/2
    headY = windowHeight/2
    headX_change = 0
    headY_change = 0

    #stores the snake block co-ords.
    bodyList = []
    #Stores the length of the snake.
    bodyLength = 1
    
    #Generate an apple.
    appleX, appleY = makeApple()

    #while the game hasn't stopped
    while not gameQuit:

        #If the game has ended
        while gameStop == True:
            #wipe the screen
            window.fill(white)
            #render text..
            showText("Game over, press C to play again, or Q to quit.", red, centre)
            #update.
            pygame.display.update()

            #event loop to detect what the user presses
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #if they press q
                    if event.key == pygame.K_q:
                        #leave the gameStop loop and quit the game
                        gameQuit = True
                        gameStop = False
                    #if they press c
                    if event.key == pygame.K_c:
                        #restart the game
                        gameLoop()
        
        #get continuously check for events
        for event in pygame.event.get():
            #print(event)
            #if the quit event occurs
            if event.type == pygame.QUIT:
                #stop running the game
                gameQuit = True
            #if a keypress occurs
            elif event.type == pygame.KEYDOWN:
                #if the key was left
                if event.key == pygame.K_LEFT:
                    #move the head to the left by however big the snake's head is
                    headX_change = -snakeSize
                    #reset the other movement tracker
                    headY_change = 0
                #if the key was left
                elif event.key == pygame.K_RIGHT:
                    #move the head to the right by however big the snake's head is
                    headX_change = snakeSize
                    #reset the other movement tracker
                    headY_change = 0
                #if the key was left
                elif event.key == pygame.K_UP:
                    #move the head up by however big the snake's head is
                    headY_change = -snakeSize
                    #reset the other movement tracker
                    headX_change = 0
                #if the key was left
                elif event.key == pygame.K_DOWN:
                    #move the head down by however big the snake's head is
                    headY_change = snakeSize
                    #reset the other movement tracker
                    headX_change = 0
                        
        
        #Move the head based on what was decided above
        headX += headX_change
        headY += headY_change

        #move the snake head if it goes off screen
        if headX >= windowWidth:
            headX = 0
        elif headX < 0:
            headX = windowWidth
        elif headY >= windowHeight:
            headY = 0
        elif headY < 0:
            headY = windowHeight

        #Quit the game if the snake goes offscreen
        #if not 0 <= headX <= windowWidth or not 0 <= headY <= windowHeight:
        #    gameStop = True

        #fill the entire window with the colour white (var defined near top)
        window.fill(white)

        #Draw the apple. make sure it's drawn before the snake, otherwise it will be on top of the snake.
        pygame.draw.rect(window, red, [appleX,appleY,snakeSize,snakeSize])        

        #draw double score block
        if nextDouble == 0:
            pygame.draw.rect(window, blue, [doubleX,doubleY,snakeSize,snakeSize])  

        headXY = []
        headXY.append(headX)
        headXY.append(headY)
        bodyList.append(headXY)

        if len(bodyList) > bodyLength:
            del bodyList[0]

        for eachSegment in bodyList[:-1]:
            if eachSegment == headXY:
                gameStop = True
            
        ##Draw a snake head.
        ##args: surface, colour, origin and size as [x, y, width, height]. Origin is the top left corner. height goes down, width goes right.
        #pygame.draw.rect(window, black, [headX,headY,snakeSize,snakeSize])
        ##here's an alternative method for drawing rectangles.
        ##it may be preferred because fill can be graphics accelerated, whereas draw.rect cannot.
        ##window.fill(red, rect=[200,200,50,50])
        drawSnake(bodyList)

        #Draw score
        showText("Score: " + str(score), yellow, [windowWidth/10*7,0])

        #update the window
        pygame.display.update()

        #if the head and apple have the same co-ords, eat it.
        if headX == appleX and headY == appleY:
            appleX, appleY = makeApple()
            bodyLength += 1
            score = score + addScore
            if nextDouble != 0:
                nextDouble -= 1
            else:
                doubleScore(addScore, True, doubles)
        
        #tick the clock for 10 FPS
        gameClock.tick(FPS)

        print(nextDouble)

    ##Game loop ended, so the user must have lost the game. Show a loose message...
    #showText("You loose!",red, centre)
    ##Update the display
    #pygame.display.update()
    ##Wait for a second so that the user can read the message before the game quits.
    #time.sleep(2)
    
    #un-initialize pygame modules
    pygame.quit()
    #Kill python
    quit()

gameLoop()
