"""Base classes project

    Define the classes used in the project, as the Player class and the Team class.

"""
#-*-coding:utf8;-*-

import math
import copy
from random import random,randint
import cPickle
#utiliser copy.deepcopy pour copier un object

DEFAULT_VALUE=100

listPostEn=['goalkeeper','libero','left-back','centre-back','right-back','defensive midfield','left midfield','centre midfield','right midfield','attacking midfield','left midfield','right midfield','second striker','winger']
listPostFr=['gardien','libero','défenseur gauche','défenseur central','défenseur droit','milieu défensif','milieu gauche','milieu axial','milieu droit','milieu offensif','ailier gauche','ailier droit','attaquant de soutien','avant-centre']


class Player:
    """Player that will be trained.

    Do NOT confuse with the enduser, that will train the Player.
    """
    
    def __init__(self, post):
        """Initialisation member.
         
        Use Player(post) to create a new player.

        post is the index of the job the player must do. That is, reffer to listPostEn and listPostFr.
        """
        
        """Global Stats"""
        self.name="Joueur"
        self.baseStrength=DEFAULT_VALUE #1-100
        self.playedMatchList=[] #True=won False=Lost
        self.woundedList=[] #True/False
        self.easinessJob=[random() for i in range(14)]#On initialise les 14 cases avec random()
        """Stats during the match"""
        self.fitness=DEFAULT_VALUE #1-100
        self.moral=DEFAULT_VALUE #1-100
        self.currentPost=post
        self.injured=False
        self.spirit={'happy':True,'disturbed':False}
        self.currentStrength=self.baseStrength*float(self.fitness)/100*float( self.getMoral() )/100*self.easinessJob[self.currentPost]
        
    def updateMoral(self):
        """ Le moral est calculé à partir du nombre de matchs gagnés(coeff 3), du nombre de blessures(coeff 1)
            et de l'état d'esprit du joueur: si il est en colère son moral diminu de 50% si il est troublé son moral diminu de 25%...
        """
        if len(self.playedMatchList)>0 and len(self.woundedList)>0:
            self.moral=100*float(self.playedMatchList.count(True)*3+self.woundedList.count(False))/(len(self.playedMatchList)*3+len(self.woundedList))*( 1*self.spirit['happy']+0.5*(not self.spirit['happy']) )*( 1*(not self.spirit['disturbed'])+0.75*self.spirit['disturbed'] )
            """( 1*self.spirit['happy']+0.5*(not self.spirit['happy']) ) : si il est content self.spirit['happy']=True (soit 1) et (not self.spirit['happy'])=False (soit 0),
                d'où 1*self.spirit['happy']=1*1=1    0.5*(not self.spirit['happy'])=0.5*0=0    1+0=1, le moral de change pas
            """
        else:
            self.moral=DEFAULT_VALUE
            
    def getMoral(self, update=True):
        if update==True:
           self.updateMoral()
        return self.moral
    
    def updateCurrentStrength(self):
        self.currentStrength=self.baseStrength*float(self.fitness)/100*float( self.getMoral() )/100*self.easinessJob[self.currentPost]
        
    def getCurrentStrength(self, update=True):
        if update==True:
            self.updateCurrentStrength()
        return self.currentStrength
    
    def getPost(self):
        return self.currentPost

class Team:
    def __init__(self,filePath="",jobPlayers=[]):
        self.playersList=[] 
        self.filePath=filePath
        self.score=0
        if filePath != "":
            self.loadFromFile(filePath)
        else:
            for i in jobPlayers:
                self.playersList.append(Player(i))
        self.strength=math.fsum(Player.getCurrentStrength() for Player in self.playersList)
        
    def updateStrength(self):
        self.strength=math.fsum(Player.getCurrentStrength() for Player in self.playersList)
        
    def getStrength(self, update=True):
        if update==True:
            self.updateStrength()
        return self.strength
    
    def getPlayer(self, index):
        return self.playersList[index]

    def size(self):
        return len(self.playersList)
    
    def loadFromFile(self, filePath):
        """En cours d'implémentation.

        Permet de charger l'équipe directement depuis un fichier.
        """
        with open(filePath,"rb") as fileTeam:
            readPickler = cPickle.Unpickler(fileTeam)
            self = readPickler.load()
##        fileContent=fileTeam.read();
##        self.playersList=[]
##        self.playersList.append(Player(i))
##        
##        fileTeam.close()

    def saveToFile(self, filePath):
        """En cours d'implémentation.

        Permet de sauvegarder l'équipe directement dans un fichier.
        """
        with open(filePath,"wb") as fileTeam:
            writePickler = cPickle.Pickler(fileTeam)
            writePickler.dump(self)
