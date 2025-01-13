from random import randint
from direct.showbase.ShowBase import ShowBase



class MyApp(ShowBase):
    def __init__(self):
        super().__init__()
        for i in range(10):
            x = randint(0,40)
            y = randint(0, 40)
            z = randint(0, 5)
            self.cube = self.loader.loadModel("models/box")
            self.cube.setScale(1, 1, 1)
            self.cube.setPos(x, y, z)
            self.cube.reparentTo(self.render)

app = MyApp()
app.run()