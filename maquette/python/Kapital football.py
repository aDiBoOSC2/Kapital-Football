#-*-coding:utf8;-*-

from base_classes import*
from match import game
import math
import copy
import cPickle
#utiliser copy.deepcopy pour copier un object

print "Equipe 1:"
team1=Team(jobPlayers=[0,0,0,0,0,0,0,0,0,0,0])
print "Force :",team1.getStrength()

print "Equipe 2:"

team2=Team(jobPlayers=[0,1,2,3,4,5,6,7,8,9,10])
print "Force :",team2.getStrength()

for i in range(10):
    scoreT1, scoreT2 = game(team1,team2)
    print "score final:", scoreT1,"-",scoreT2
