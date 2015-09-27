
#My First Game


import random, sys, time, pygame
from pygame.locals import *

Number_of_flash = 30
Width = 640
Height = 480
flash_speed = 500 # in milliseconds
flash_delay = 200 # in milliseconds
button_size = 200
button_gapsize = 20
Timeout = 4 # 4 seconds before game over if no button is pushed.


WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

Xaxis = int((Width - (2 * button_size) - button_gapsize) / 2)
Yaxis = int((Height - (2 * button_size) - button_gapsize) / 2)

# Rect objects for each of the four buttons
YELLOW_RECT = pygame.Rect(Xaxis, Yaxis, button_size, button_size)
BLUE_RECT   = pygame.Rect(Xaxis + button_size + button_gapsize, Yaxis, button_size, button_size)
RED_RECT    = pygame.Rect(Xaxis, Yaxis + button_size + button_gapsize, button_size, button_size)
GREEN_RECT  = pygame.Rect(Xaxis + button_size + button_gapsize, Yaxis + button_size + button_gapsize, button_size, button_size)

def main():
    global clock, screen, font, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('Simulate')

    font = pygame.font.Font('freesansbold.ttf', 16)
    info_Surf = font.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    info_Rect = info_Surf.get_rect()
    info_Rect.topleft = (10, Height - 25)

    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True: # main game loop
        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        screen.fill(bgColor)
        drawButtons()

        score_Surf = font.render('Score: ' + str(score), 1, WHITE)
        score_Rect = score_Surf.get_rect()
        score_Rect.topleft = (Width - 100, 10)
        screen.blit(score_Surf, score_Rect)

        screen.blit(info_Surf, info_Rect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN



        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(flash_delay)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - Timeout > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        clock.tick(Number_of_flash)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOW_RECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUE_RECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = RED_RECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREEN_RECT

    orig_Surf = screen.copy()
    flash_Surf = pygame.Surface((button_size, button_size))
    flash_Surf = flash_Surf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            screen.blit(orig_Surf, (0, 0))
            flash_Surf.fill((r, g, b, alpha))
            screen.blit(flash_Surf, rectangle.topleft)
            pygame.display.update()
            clock.tick(Number_of_flash)
    screen.blit(orig_Surf, (0, 0))


def drawButtons():
    pygame.draw.rect(screen, YELLOW, YELLOW_RECT)
    pygame.draw.rect(screen, BLUE,   BLUE_RECT)
    pygame.draw.rect(screen, RED,    RED_RECT)
    pygame.draw.rect(screen, GREEN,  GREEN_RECT)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((Width, Height))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()
        screen.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        screen.blit(newBgSurf, (0, 0))

        drawButtons() # redraw the buttons on top of the tint

        pygame.display.update()
        clock.tick(Number_of_flash)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    orig_Surf = screen.copy()
    flash_Surf = pygame.Surface(screen.get_size())
    flash_Surf = flash_Surf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time, roughly.
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flash_Surf.fill((r, g, b, alpha))
                screen.blit(orig_Surf, (0, 0))
                screen.blit(flash_Surf, (0, 0))
                drawButtons()
                pygame.display.update()
                clock.tick(Number_of_flash)



def getButtonClicked(x, y):
    if YELLOW_RECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUE_RECT.collidepoint( (x, y) ):
        return BLUE
    elif RED_RECT.collidepoint( (x, y) ):
        return RED
    elif GREEN_RECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()

