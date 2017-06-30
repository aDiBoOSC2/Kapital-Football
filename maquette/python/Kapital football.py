#-*-coding:utf8;-*-

from base_classes import*
from match import match
import math
import copy
import cPickle
import pygame.display
from pygame.locals import *
import threading

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#utiliser copy.deepcopy pour copier un object

print "Equipe 1:"
team1=Team(jobPlayers=[0,0,0,0,0,0,0,0,0,0,0])
print "Force :",team1.strength

print "Equipe 2:"

team2=Team(jobPlayers=[0,1,2,3,4,5,6,7,8,9,10])
print "Force :",team2.strength

##for i in range(20):
##    scoreT1, scoreT2 = match(team1,team2)
##    print "score final:", scoreT1,"-",scoreT2

leftTime=90

matchLock=threading.RLock()
matchEvent=threading.Event()
threadMatch = threading.Thread(None, match, None, (team1,team2, matchLock, matchEvent, 500))

pygame.init()
#Ouverture de la fenêtre Pygame
screen = pygame.display.set_mode((857, 768), pygame.SRCALPHA, 32)
pygame.display.set_caption('Kapital Football !')

# Création du fond blanc
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

#Chargement et collage du fond
field = pygame.image.load("field.png").convert_alpha()
field = pygame.transform.smoothscale(field, (507,768))
screen.blit(field, (0,0))

#Chargerment des textures des joueurs et du ballon
bluePlayerImage = pygame.image.load("player blue.png").convert_alpha()
bluePlayerImage = pygame.transform.smoothscale(bluePlayerImage, (90,90))

redPlayerImage = pygame.image.load("player red.png").convert_alpha()
redPlayerImage = pygame.transform.smoothscale(redPlayerImage, (90,90))

ballImage = pygame.image.load("ball.png").convert_alpha()
ballImage = pygame.transform.smoothscale(ballImage, (45,45))

normalFont = pygame.font.Font(None, 36)
specialFont = pygame.font.Font(None, 36)
specialFont.set_underline(True)
specialFont.set_bold(True)
specialFont.set_italic(True)

#Numéros des parties
goalText = normalFont.render("Goal", 1, BLACK)
threeText = normalFont.render("3", 1, BLACK)
twoText = normalFont.render("2", 1, BLACK)
oneText = normalFont.render("1", 1, BLACK)
centerText = normalFont.render("Center", 1, BLACK)
minusOneText = normalFont.render("-1", 1, BLACK)
minusTwoText = normalFont.render("-2", 1, BLACK)
minusThreeText = normalFont.render("-3", 1, BLACK)

specialGoalText = specialFont.render("Goal !!!", 1, BLACK,RED)

#Texte annexe

timeText = specialFont.render("Left Time: 90", 1, BLACK)

infoText = ["Press 'Space' to ","start and stop.","Game end after","90 sec, plus 3","sec each goal."]
infoTextRender = []
for text in infoText:
    infoTextRender.append(specialFont.render(text, 1, BLACK))

scoreText = specialFont.render("0 - 0", 1, BLACK)

#Rafraîchissement de l'écran
pygame.display.flip()

continuer=True
#boucle de jeu
while continuer:
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT:     #Si un de ces événements est de type QUIT
            continuer = False      #On arrête la boucle
            if threadMatch.is_alive():
                matchEvent.set()
                threadMatch.join()
            continue
        if event.type == KEYUP:
            if event.key == K_SPACE:
                if not threadMatch.is_alive():
                    matchLock=threading.RLock()
                    matchEvent=threading.Event()
                    threadMatch = threading.Thread(None, match, None, (team1,team2, matchLock, matchEvent, 500))
                    threadMatch.start()
                    print "Début du match !!"
                else:
                    matchEvent.set()
                    threadMatch.join()
                    print "Fin du match !!"
        if event.type == MOUSEBUTTONUP:
            if event.button == 2:
                x=event.pos[0]
                y=event.pos[1]
    
    #Affichage et rafraîchissement de l'écran
    screen.blit(background, (0,0))
    screen.blit(field, (0,0))
    
    #Affichage des images
    #On verrouille le thread pour protéger les ressources, il sera déverrouillé lorsque with finira
    with matchLock:
        screen.blit(bluePlayerImage, (20, 340+team1.currentPos*81))
        screen.blit(redPlayerImage, (400, 340+team2.currentPos*81))
        if team1.hasBall:
            screen.blit(ballImage, (115, 363+team1.currentPos*81))
        else:
            screen.blit(ballImage, (350, 363+team2.currentPos*81))

    #Affichage du nombre de joueurs
    with matchLock:
        screen.blit(normalFont.render(str(team1.nbCurrentPlayer), 1, WHITE), (53,373+team1.currentPos*81))
        screen.blit(normalFont.render(str(team2.nbCurrentPlayer), 1, WHITE), (433, 373+team2.currentPos*81))
    
    #Affichage du texte
    with matchLock:
        if team1.currentPos==-4:
            screen.blit(specialGoalText, (520,50))
        else:
            screen.blit(goalText, (520,50))
    screen.blit(minusThreeText, (520,130))
    screen.blit(minusTwoText, (520,211))
    screen.blit(minusOneText, (520,292))
    screen.blit(centerText, (520,375))
    screen.blit(oneText, (520,457))
    screen.blit(twoText, (520,539))
    screen.blit(threeText, (520,620))
    with matchLock:
        if team1.currentPos==4:
            screen.blit(specialGoalText, (520,703))
        else:
            screen.blit(goalText, (520,703))
    
    with matchLock:
        timeText = specialFont.render("Left Time: %s" % team1.leftTime, 1, BLACK)
    
    screen.blit(timeText, (620,130))
    
    for i in range(len(infoTextRender)):
        screen.blit(infoTextRender[i], (620,375+30*(i-float(len(infoTextRender)-1)/2)))

    with matchLock:
        scoreText = specialFont.render("%s - %s" % (team1.score,team2.score), 1, BLACK)
        screen.blit(scoreText, (620,620))
    
    pygame.display.flip()
    pygame.time.wait(16)

pygame.quit()
