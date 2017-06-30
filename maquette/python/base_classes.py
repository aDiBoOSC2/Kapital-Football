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
    
    def __init__(self, post,name="Joueur"):
        """Initialisation member.
         
        Use Player(post) to create a new player.

        post is the index of the job the player must do. That is, reffer to listPostEn and listPostFr.
        """
        
        """Global Stats"""
        self.name=name
        self.__baseStrength=DEFAULT_VALUE #1-100
        self.playedMatchList=[] #True=won False=Lost
        self.woundedList=[] #True/False
        self.easinessJob=[random() for i in range(14)]#On initialise les 14 cases avec random()
        """Stats during the match"""
        self.__fitness=DEFAULT_VALUE #1-100
        self.__currentMoral=DEFAULT_VALUE #1-100
        self.__moral=self.__currentMoral
        self.currentPost=post
        self.injured=False
        self.spirit={'happy':True,'disturbed':False}
        self.__currentStrength=self.baseStrength*float(self.fitness)/100*float( self.moral )/100*self.easinessJob[self.currentPost]
        self.strength=self.__currentStrength

    @property
    def baseStrength(self):
        return self.__baseStrength
    @baseStrength.setter
    def baseStrength(self, baseStrength):
        if baseStrength<0:
            raise ValueError("value of baseStrength must be over 0")
        elif baseStrength>100:
            raise ValueError("value of baseStrength must be under 100")
        self.__baseStrength = baseStrength

    @property
    def fitness(self):
        return self.__fitness
    @fitness.setter
    def fitness(self, fitness):
        if fitness<0:
            raise ValueError("value of fitness must be over 0")
        elif fitness>100:
            raise ValueError("value of fitness must be under 100")
        self.__fitness = fitness

    @property
    def moral(self):
        return self.__moral
    @moral.setter
    def moral(self, moral):
        if moral<0:
            raise ValueError("value of moral must be over 0")
        elif moral>100:
            raise ValueError("value of moral must be under 100")
        self.__moral = moral

    @property
    def currentMoral(self):
        """ Le moral est calculé à partir du nombre de matchs gagnés(coeff 3), du nombre de blessures(coeff 1)
            et de l'état d'esprit du joueur: si il est en colère son moral diminu de 50% si il est troublé son moral diminu de 25%...
        """
        if len(self.playedMatchList)>0 and len(self.woundedList)>0:
            self.__currentMoral=100*float(self.playedMatchList.count(True)*3+self.woundedList.count(False))/(len(self.playedMatchList)*3+len(self.woundedList))*( 1*self.spirit['happy']+0.5*(not self.spirit['happy']) )*( 1*(not self.spirit['disturbed'])+0.75*self.spirit['disturbed'] )
            """( 1*self.spirit['happy']+0.5*(not self.spirit['happy']) ) : si il est content self.spirit['happy']=True (soit 1) et (not self.spirit['happy'])=False (soit 0),
                d'où 1*self.spirit['happy']=1*1=1    0.5*(not self.spirit['happy'])=0.5*0=0    1+0=1, le moral de change pas
            """
        else:
            self.__currentMoral=DEFAULT_VALUE
        self.moral=self.__currentMoral
        return self.__currentMoral
    @currentMoral.setter
    def currentMoral(self, moral):
        self.__moral = moral
        self.moral=self.__currentMoral
    
    @property
    def currentStrength(self):
        self.__currentStrength=(self.baseStrength*float(self.fitness)/100*float( self.moral )/100*self.easinessJob[self.currentPost])* (not self.injured)
        self.strength=self.__currentStrength
        return self.__currentStrength
    @currentStrength.setter
    def currentStrength(self, currentStrength):
        if currentStrength<0:
            raise ValueError("value of currentStrength must be over 0")
        elif currentStrength>100:
            raise ValueError("value of currentStrength must be under 100")
        self.__currentStrength = currentStrength
        self.strength=__currentStrength

class Team:
    def __init__(self,filePath="",jobPlayers=[], namePlayers=[]):
        self.playersList=[] 
        self.filePath=filePath
        self.score=0
        self.currentPos=0
        self.hasBall=False
        self.leftTime=90
        self.nbCurrentPlayer=11
        if filePath != "":
            self.loadFromFile(filePath)
        else:
            for job in jobPlayers:
                self.playersList.append(Player(job))
        self.__strength=math.fsum(Player.currentStrength for Player in self.playersList)
    
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

    def update(self):
        """ Actualise l'équipe."""
        self.leftTime-=1
        """ Définit si un joueur est blessé """
        for player in self.playersList:
            if player.injured==True:
                continue
            if randint(0,int(25000*float(player.fitness)/100*float( player.moral )/100*player.easinessJob[player.currentPost])) in range(0,1):#5000
                player.injured=True
                self.nbCurrentPlayer-=1

    def restore(self):
        self.leftTime=90
        self.score=0
        self.currentPos=0
        self.hasBall=False
        """Réinitialise les propriétés de match des joueurs.
        """
        for player in self.playersList:
            player.injured=False
        self.nbCurrentPlayer=11
    
    @property
    def strength(self):
        self.__strength=math.fsum(Player.currentStrength for Player in self.playersList)
        return self.__strength
    @strength.setter
    def strength(self, strength):
        self.__strength = strength
