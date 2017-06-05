
import pygame
import logging

class BasicTournament(object):
    def __init__(self, cfg, leaderfunc):
        self.cfg = cfg
        self._name = "Basic Tournament"
        self._initialized = False
        self._numgroups = cfg.getint("Tournament", "groups")
        self._groups = []
        self._currentgroup = 0
        self._finalgroup = []
        self._finalround = False
        self._finalwinners = None
        self._leaderfunc = leaderfunc
        self._primary_victory = cfg.get("Game", "primary_victory_attr")
        self._secondary_victory = cfg.get("Game", "secondary_victory_attr")

    def is_initialized(self):
        return self._initialized

    def is_final_round(self):
        return self._finalround

    def initialize(self, players):
        """
        Initialize a tournament from the list of players.

        The first round should be set to go
        """
        logging.info("[Tournament] Initialized with %d players", len(players))
        self._groups = []
        for x in xrange(self._numgroups):
            self._groups.append([])
        #next
        x = 0
        for player in players:
            self._groups[x % self._numgroups].append(player)
            x += 1
        #next
        self._initialized = True

    def check_score_equal(self, player1, player2):
        """
        Checks to see if two player scores are equal according to the current game rules.
        """
        return getattr(player1, self._primary_victory) == getattr(player2, self._primary_victory) and getattr(player1, self._secondary_victory) == getattr(player2, self._secondary_victory)

    def check_results(self, players, stats):
        """
        Get the end results, pre-sorted (top players first in list)
        """
        if not self._finalround:
            # get winner(s)
            for x in xrange(self.cfg.getint("Tournament", "number_to_final_round")):
                logging.info("Adding player to final round %s stats: %s", players[x].name, stats[x])
                self._finalgroup.append(players[x])
            #next
        else:
            logging.info("Final Round Winner %s stats: %s", players[0].name, stats[0])
            self._finalwinners = [players[0]]
            i = 1
            # Check for ties
            while i < len(players) and self.check_score_equal(players[0], players[i]):
                self._finalwinners.append(players[i])
                i += 1

    def next_round(self):
        """
        Setup a subsequent round of players.
        """
        self._currentgroup += 1
        logging.info("[Tournament] Round %d of %d", self._currentgroup, self._numgroups)
        if self._currentgroup == self._numgroups:
            self._finalround = True

    def get_players_in_round(self):
        """
        Returns the list of players in the current round.
        """
        if self._finalround:
            return self._finalgroup
        else:
            if self._currentgroup < len(self._groups):
                return self._groups[self._currentgroup]
            else:
                return []
        #eif

    def gui_initialize(self):
        self._tfont = pygame.font.Font("freesansbold.ttf", 18)

    def gui_draw_tournament_bracket(self, screen, flags, trackplayer):
        screen.blit(self._tfont.render(self._name, False, (255, 255, 255)), (100, 50))

        # draw first Bracket
        y = 100
        for x in xrange(self._numgroups):
            py = y
            for player in self._groups[x]:
                c = (128, 128, 128)
                if x == self._currentgroup:
                    c = (255, 255, 255)
                if trackplayer != None and player == trackplayer:
                    c = trackplayer.color
                screen.blit(self._tfont.render(player.name, False, c), (100, y))
                y += 24
                                
            # draw bracket lines
            pygame.draw.line(screen, (192, 192, 192), (400, py), (410, py))
            pygame.draw.line(screen, (192, 192, 192), (410, py), (410, y))
            pygame.draw.line(screen, (192, 192, 192), (400, y), (410, y))
            pygame.draw.line(screen, (192, 192, 192), (410, py + (y - py) / 2), (410, py + (y - py) / 2))
                                
            y += 36

        # draw Final Bracket
        y = 96 + ((y - 96) / 2) - len(self._finalgroup) * 16
        py = y
        for player in self._finalgroup:
            c = (255, 255, 128)
            if trackplayer != None and player == trackplayer:
                c = trackplayer.color
            screen.blit(self._tfont.render(player.name, False, c), (435, y))
            y += 24
        pygame.draw.line(screen, (192, 192, 192), (800, py), (810, py))
        pygame.draw.line(screen, (192, 192, 192), (810, py), (810, y))
        pygame.draw.line(screen, (192, 192, 192), (800, y), (810, y))

        if self._finalwinners:
            for player in self._finalwinners:
                screen.blit(self._tfont.render(player.name, False, (128, 255, 255)), (835, py + (y - py) / 2))
                y += 36

        return y

class WildTournament(BasicTournament):
    def __init__(self, cfg, leaderfunc):
        super(WildTournament, self).__init__(cfg, leaderfunc)
        self._name = "Wild Tournament"
        self._wildgroup = []
        self._playwildround = cfg.getboolean("Wildcard", "play_round")
        self._toplay = cfg.getint("Wildcard", "number")
        self._andties = cfg.getboolean("Wildcard", "take_ties")
        self._wildround = False

    def check_results(self, players, stats):
        """
        Get the end results, pre-sorted (top players first in list)
        """
        super(WildTournament, self).check_results(players, stats)
        if not self._finalround and not self._wildround:
            #self._wildgroup = []
            self.check_wildcard()

    def check_wildcard(self):
        x = 0
        self._wildgroup = []
        for player in self._leaderfunc(True): # Get all player scores sorted
            if player not in self._finalgroup:
                # do check before, so we have 'next' player after appending last to check ties
                if x >= self._toplay and \
                    (not self._andties or 
                     (len(self._wildgroup) >= 1 and not self.check_score_equal(player, self._wildgroup[-1]))):
                    break
                x += 1
                self._wildgroup.append(player)

    def next_round(self):
        """
        Setup a subsequent round of players.
        """
        super(WildTournament, self).next_round()
        if self._currentgroup >= self._numgroups and self._playwildround and not self._wildround:
            logging.info("Wild Tournament Round")
            self._wildround = True
            self._finalround = False
        elif self._playwildround and self._wildround:
            self._finalround = True
            self._wildround = False

        if not self._playwildround and self._finalround:
            #self._wildgroup = []
            #self.check_wildcard()
            for player in self._wildgroup:
                self._finalgroup.append(player)

    def get_players_in_round(self):
        """
        Returns the list of players in the current round.
        """
        if self._wildround:
            return self._wildgroup
        else:
            return super(WildTournament, self).get_players_in_round()

    def gui_draw_tournament_bracket(self, screen, flags, trackplayer):
        y = super(WildTournament, self).gui_draw_tournament_bracket(screen, flags, trackplayer)

        if not self._wildround:
            self.check_wildcard() # update

        # draw Final Bracket
        if not self._finalround:
            if self._playwildround:
                y += 96
            else:
                y += 24

            py = y

            for player in self._wildgroup:
                c = (128, 255, 255)
                if self._playwildround and self._wildround:
                    c = (255, 255, 255)
                if trackplayer != None and player == trackplayer:
                    c = trackplayer.color
                screen.blit(self._tfont.render(player.name, False, c), (435, y))
                y += 24
        
            y = py + len(self._wildgroup) * 24
            pygame.draw.line(screen, (0, 192, 192), (800, py), (810, py))
            pygame.draw.line(screen, (0, 192, 192), (810, py), (810, y))
            pygame.draw.line(screen, (0, 192, 192), (800, y), (810, y))
