import pygame

from GUIEntity import GUIEntity
from World.WorldCommands import ThrustCommand, BrakeCommand, WarpCommand, CloakCommand, RaiseShieldsCommand
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, namefont, debugfont, infofont
from GUI.GraphicsCache import Cache

class ShipGUI(GUIEntity):
    _exsurface = None
    _shieldsurface = None
    _shieldhudsurface = None

    """description of class"""
    def __init__(self, ship, world):
        super(ShipGUI, self).__init__(ship, world)
        self.surface = Cache().getImage("Ships/ship" + repr(ship.player.image))
        self.dying = False
        self.dead = False
        self.dyframe = 0
        if ShipGUI._exsurface == None:
            ShipGUI._exsurface = Cache().getImage("Ships/ExplosionWarp")
            ShipGUI._shieldsurface = Cache().getImage("Ships/Shield")
            ShipGUI._shieldhudsurface = Cache().getImage("HUD/Shield")

    def draw(self, surface, flags):
        # Check if Thrusting or Braking
        state = 0

        # TODO: Notify Ship of Start/End of Commands...?

        yoff = 0
        if self._worldobj.commandQueue.containstype(CloakCommand):
            yoff = 64

        if self._worldobj.commandQueue.containstype(WarpCommand):
            state = 6
        elif self._worldobj.commandQueue.containstype(BrakeCommand):
            state = 5
        else:
            cmd = self._worldobj.commandQueue.containstype(ThrustCommand) # HACK? TODO - One loop
            if cmd != None:
                #pygame.draw.circle(surface, (255, 255, 0), intpos(pos + cmd.getForceVector(self._worldobj.thrusterForce, self._worldobj.rotationAngle, 0.02)), 5)
                state = 1 + ['L','F','R','B'].index(cmd.direction)
            #eif
        #eif

        # Rotate to Current Direction
        rotimg = pygame.transform.rotate(self.surface.subsurface(pygame.Rect(64 * state, yoff, 64, 64)), self._worldobj.rotationAngle - 90)
        w, h = rotimg.get_rect().size
        bp = intpos(self._worldobj.body.position)
        pos = intpos(self._worldobj.body.position - (w/2, h/2))

        if len(self._worldobj.lasernodes) > 0:
            for i in range(0, len(self._worldobj.lasernodes)+1, 2):
                if i < len(self._worldobj.lasernodes)-1:
                    pygame.draw.line(surface, self._worldobj.player.color, self._worldobj.lasernodes[i], self._worldobj.lasernodes[i+1], 3)
                elif i < len(self._worldobj.lasernodes):
                    pygame.draw.line(surface, self._worldobj.player.color, self._worldobj.lasernodes[i], intpos(self._worldobj.body.position), 3)
                #eif

        # Draw
        surface.blit(rotimg, pos)

        gp = intpos(self._worldobj.body.position - (32, 32)) #adjusted fixed graphic size
        # Draw shield
        if self._worldobj.commandQueue.containstype(RaiseShieldsCommand) and self._worldobj.shield.value > 0:
            surface.blit(ShipGUI._shieldsurface, gp)

        # Draw explosion
        if self.dying:
            surface.blit(ShipGUI._exsurface.subsurface(pygame.Rect(64 * self.dyframe, 0, 64, 64)), gp)
            self.dyframe += 1
            if self.dyframe == 16:
                self.dead = True
                self.dying = False

        if flags["NAMES"]:
            # HACK TODO: Ship name should be from team
            text = namefont().render(self._worldobj.player.name, False, self._worldobj.player.color)
            surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-44))

        if flags["DEBUG"]:
            #wrapcircle(surface, (0, 255, 0), bp, 4, self._world.size)  # Position            
            wrapcircle(surface, (255, 255, 0), bp, self._worldobj.radarRange, self._world.size, 1) # Radar            

        if flags["STATS"] and self._worldobj.shield.maximum > 0:
            # Energy Bar
            pygame.draw.rect(surface, (0, 0, 96), pygame.Rect(bp[0]-16, bp[1] + 21, 32, 5))

            if flags["DEBUG"]:
                surface.blit(debugfont().render(repr(int(100 * self._worldobj.shield.percent)), False, (255, 255, 255)), (bp[0]+18, bp[1] + 16))
            surface.blit(ShipGUI._shieldhudsurface, (bp[0]-15, bp[1] + 22), pygame.Rect(0, 0, 30 * self._worldobj.shield.percent, 3))
            
        if flags["GAME"] and self._worldobj.player.score > 0:
            surface.blit(infofont().render(("%.1f" % self._worldobj.player.score) + " Pts", False, (0, 255, 255)), (bp[0]-24, bp[1] + 32))

        super(ShipGUI, self).draw(surface, flags)
