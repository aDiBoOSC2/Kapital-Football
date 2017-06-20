#-*-coding:utf8;-*-

import random
def game():
    ft1=800
    ft2=700
    coeff=0.5
    butT1=0
    butT2=0
    tabBut=[]
    balle=1 #1: Team1 2: Team2
    #lignes=[-4,-3,-2,-1,0,1,2,3,4]
    currLine=0
    nbBoucles=90
    #0: monte 1: reste 2: prendre
    for i in range(0,nbBoucles):
        var=ft1*random.random()*coeff-ft2*random.random()*(1-coeff)
        if balle==1:#Equipe 1 a la balle"""
            if var>0:#monte"""
                currLine=currLine+1  #*balle[-1]balle[-1] correspond à la dernière case
            elif var<0:#perd"""
                balle=2
        else:#Equipe 2 a la balle"""
            if var<0:#monte"""
                currLine=currLine-1  #*balle[-1]balle[-1] correspond à la dernière case
            elif var>0:#perd"""
                balle=1
        if currLine==4:
            #print "BUUUUUUUUUT !!!! Equipe 1 marque !"
            tabBut.append(1)
            currLine=0
            #print "score:",tabBut.count(1),"-",tabBut.count(2)
        elif currLine==-4:
            #print "BUUUUUUUUUT !!!! Equipe 2 marque !"
            tabBut.append(2)
            #print "score:",tabBut.count(1),"-",tabBut.count(2)
            currLine=0
        
        coeff=0.5-currLine*0.01
        #print "coeff=",coeff
    print "score final:", tabBut.count(1),"-",tabBut.count(2)
    return tabBut.count(1),tabBut.count(2)

#print "t1 gagne :",tab.count(False)
#print "soit :",float(tab.count(False))/nbBoucles*100,"%"

for i in range(0,10):
    game()
