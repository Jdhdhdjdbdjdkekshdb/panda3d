from direct.showbase.ShowBase import ShowBase
from mapmanager import MapManager
from player import PlayerControl
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.camLens.setFov(110)
        self.mapp = MapManager()
        self.cam = PlayerControl(self.mapp)


game = Game()
game.run()