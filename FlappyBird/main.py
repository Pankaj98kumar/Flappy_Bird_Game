import random
import sys
import pygame
from pygame.locals import *

# Global variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\bird.png"
BACKGROUND = "C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\background.png"
PIPE =  "C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\pipe.png"

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES["player"].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES["message"].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get(): #it record which key has been pressed
            
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)
        
        
def mainGame():
    score = 0
    aceelerator=score
    playery=int(SCREENWIDTH/2)
    playerx=int(SCREENWIDTH/5)
    basex=0
    print(playery)
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x' : SCREENWIDTH+200 , 'y' : newPipe1[0]['y']},
        {'x' : SCREENWIDTH+200+(SCREENWIDTH/2) , 'y' : newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x' : SCREENWIDTH+200 , 'y' : newPipe1[1]['y']},
        {'x' : SCREENWIDTH+200+(SCREENWIDTH/2) , 'y' : newPipe2[1]['y']}
    ]
    
    pipeVelx = -4
    playerVely = -9
    playerMaxVel = 10
    playerAccy = 1

    playerFlapVely = -8
    playerFlapped = False
    # GAME_SOUNDS['wing'].play()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapVely
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        
        if(crashTest):
            GAME_SOUNDS['die'].play()
            return
        # score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos <pipeMidPos+4:
                score += 1
                print(f"Score : {score}")
                GAME_SOUNDS["point"].play()
        if playerVely < playerMaxVel and not playerFlapped:
            playerVely += playerAccy
        
        if playerFlapped :
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)
        
        for upperpipe ,lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

    # Blinting
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe , lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(0,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width =0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)  


def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playerx<0 or playery>(GROUNDY-25):
        GAME_SOUNDS['hit'].play()
        return True
    pipeHieght = GAME_SPRITES['pipe'][0].get_height()
    for pipe in upperPipes:
        if playery < (pipe['y']+pipeHieght) and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()/2:
            GAME_SOUNDS['hit'].play()
            return True
        
    for pipe in lowerPipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()/2:
            GAME_SOUNDS['hit'].play()
            return True
    return False



        
def getRandomPipe():
    pipeHeigth=GAME_SPRITES["pipe"][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES["base"].get_height()-offset*1.2))
    pipex=SCREENWIDTH+10
    y1=pipeHeigth-y2+offset
    pipe = [
        {'x': pipex,'y':-y1},
        {'x': pipex,'y': y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy bird by Pankaj")
    GAME_SPRITES['numbers'] = (
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\0.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\1.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\2.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\3.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\4.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\5.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\6.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\7.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\8.png").convert_alpha(),
        pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\9.png").convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\Message.png").convert_alpha()
    GAME_SPRITES['pipe'] =  (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
        )
    
    GAME_SPRITES['base'] = pygame.image.load("C:\\Users\\panka\\OneDrive\\Documents\\FlappyBird\\gallary\\sprites\\base.png").convert_alpha()
    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()

    # Game Sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound("gallary\\audio\\die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("gallary\\audio\\hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("gallary\\audio\\point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("gallary\\audio\\swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("gallary\\audio\\wing.wav")

    while True:
        welcomeScreen()
        mainGame()
    