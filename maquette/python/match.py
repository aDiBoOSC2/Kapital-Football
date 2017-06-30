#-*-coding:utf8;-*-

from base_classes import*
import random
import pygame.time
import threading

def match(team1, team2, matchLock, matchEvent, waitTime=1000):
    if not isinstance(team1, Team):
        raise NameError("type of team1 must be 'Team', not %s" % type(team1))
    if not isinstance(team2,Team):
        raise NameError("type of team2 must be 'Team', not %s" % type(team2))
    coeff=0.5
    tabBut=[]
    balle=randint(1,2) #1=Team1 ; 2=Team2
    #On verrouille le thread pour protéger les ressources
    with matchLock:
        team2.hasBall=balle-1
        team1.hasBall=not team2.hasBall
    currLine=0
    nbBoucles=90
    goal=False
    #0: monte 1: reste 2: prendre
    for i in range(0,nbBoucles):
        if matchEvent.is_set():
            break
        goal=False
        #On verrouille le thread pour protéger les ressources
        matchLock.acquire()
        var=team1.strength*random.random()*coeff-team2.strength*random.random()*(1-coeff)
        #On déverrouille le thread, les ressources peuvent être utilisées par d'autres threads.
        matchLock.release()
        if balle==1:#Equipe 1 a la balle
            if var>0:#monte
                currLine=currLine+1
            elif var<0:#perd
                balle=2
        else:#Equipe 2 a la balle
            if var<0:#monte
                currLine=currLine-1
            elif var>0:#perd
                balle=1
        if currLine==4:
            goal=1
            tabBut.append(1)
        elif currLine==-4:
            goal=2
            tabBut.append(2)

        #On verrouille le thread pour protéger les ressources
        with matchLock:
            coeff=0.5-currLine*0.01
            team1.currentPos=currLine
            team2.currentPos=currLine

            if balle==1:
                team1.hasBall=True
                team2.hasBall=False
            elif balle==2:
                team1.hasBall=False
                team2.hasBall=True

            if goal==1:
                team1.score+=1
            elif goal==2:
                team2.score+=1
            
            team1.update()
            team2.update()
        if goal:
            currLine=0
            coeff=0.5-currLine*0.01
            pygame.time.wait(waitTime*2)
        pygame.time.wait(waitTime)

    #On verrouille le thread pour protéger les ressources
    with matchLock: 
        team1.restore()
        team2.restore()
    
    return tabBut.count(1),tabBut.count(2)
