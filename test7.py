from random import randint
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.models_world = self.loader.loadModel("block.egg") # Замените на вашу модель
        self.texture_dirt = loader.loadTexture("dirt.png") # Замените на вашу текстуру

        self.generate_world()

    def generate_world(self):
        objects = []
        for i in range(40):
            x = randint(0, 64)
            y = randint(0, 64)
            z = randint(0, 5)
            objects.append((x, y, z))

        # Группировка и усреднение
        grouped_objects = []
        for x, y, z in objects:
            found_group = False
            for i, (gx, gy, gz, count, group) in enumerate(grouped_objects):
                if abs(x - gx) <= 2 and abs(y - gy) <= 2: # Проверка близости
                    grouped_objects[i] = (gx + x, gy + y, gz + z, count + 1, group + [(x,y,z)])
                    found_group = True
                    break
            if not found_group:
                grouped_objects.append((x, y, z, 1, [(x,y,z)]))

        # Создание объектов с усредненными позициями
        for gx, gy, gz, count, group in grouped_objects:
            avg_x = gx / count
            avg_y = gy / count
            avg_z = gz / count
            new_model_dirt = self.models_world.copyTo(render)
            new_model_dirt.setTexture(self.texture_dirt)
            new_model_dirt.setPos(avg_x, avg_y, avg_z)

app = World()
app.run()