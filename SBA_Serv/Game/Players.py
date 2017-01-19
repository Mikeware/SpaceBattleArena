
class Player(object):
    """Controller of an object in the world"""

    def __init__(self, name, color, imageindex, netid, highscore=True):
        self.name = name
        self.color = color
        self.image = imageindex
        self.netid = netid
        self.object = None # Assigned Later
        self.roundover = False
        self.waiting = False
        self.sound = None
        self.score = 0
        self.bestscore = 0
        self.deaths = 0
        self.disconnected = False
        self.lastkilledby = None
        self.wanthighscore = highscore

    def update_score(self, amount):
        """
        Should be called to manipulate a player's score, will do extra bookkeeping and sanity for you.
        """
        self.score += amount

        # scores can't be negative
        if self.score < 0:
            self.score = 0

        # update personal best
        if self.wanthighscore and self.score > self.bestscore:
            self.bestscore = self.score
        elif not self.wanthighscore and self.score < self.bestscore:
            self.bestscore = self.score

#TODO: Put alliegiences in here?

class Team(object):
    """A team consists of multiple Players all with the same objective"""

    def __init__(self, name):
        self.name = name
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)