#-*-coding:utf8;-*-

from base_classes import*
import random

def game(team1,team2):
    if not isinstance(team1, Team):
        raise NameError("type of team1 must be 'Team', not %s" % type(team1))
    if not isinstance(team2,Team):
        raise NameError("type of team2 must be 'Team', not %s" % type(team2))
    coeff=0.5
    tabBut=[]
    balle=1 #1: Team1 2: Team2
    currLine=0
    nbBoucles=90
    #0: monte 1: reste 2: prendre
    for i in range(0,nbBoucles):
        var=team1.getStrength()*random.random()*coeff-team2.getStrength()*random.random()*(1-coeff)
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
            tabBut.append(1)
            currLine=0
        elif currLine==-4:
            tabBut.append(2)
            currLine=0
        
        coeff=0.5-currLine*0.01
    team1.score = tabBut.count(1)
    team2.score = tabBut.count(2)
    return tabBut.count(1),tabBut.count(2)
