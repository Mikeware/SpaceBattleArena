
class Player(object):
    """Controller of an object in the world"""

    def __init__(self, name, color, imageindex, netid, wobj):
        self.name = name
        self.color = color
        self.image = imageindex
        self.netid = netid
        self.object = wobj
        self.roundover = False
        self.waiting = False
        self.sound = None
        self.score = 0
        self.bestscore = 0
        self.deaths = 0
        self.disconnected = False
        self.lastkilledby = None

#TODO: Put alliegiences in here?

class Team(object):
    """A team consists of multiple Players all with the same objective"""

    def __init__(self, name):
        self.name = name
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)