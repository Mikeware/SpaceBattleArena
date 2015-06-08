
import pygame
import logging

class BasicTournament:
    def __init__(self, cfg):
        self.cfg = cfg
        self._initialized = False
        self._numgroups = cfg.getint("Tournament", "groups")
        self._groups = []
        self._currentgroup = 0
        self._finalgroup = []
        self._finalround = False
        self._finalwinner = None

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
            self._finalwinner = players[0]

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
        screen.blit(self._tfont.render("Basic Tournament", False, (255, 255, 255)), (100, 50))

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

        if self._finalwinner:
            screen.blit(self._tfont.render(self._finalwinner.name, False, (128, 255, 255)), (835, py + (y - py) / 2))