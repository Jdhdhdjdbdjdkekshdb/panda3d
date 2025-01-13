from random import randint
import math





class MapManager():
    def __init__(self):
        self.models_world = loader.loadModel('block.egg')
        self.texture_grass_block = loader.loadTexture('grass_block.jpg')
        self.texture_dirt = loader.loadTexture("dirt.jpg")
        self.texture_stone = loader.loadTexture("stone.png")
        self.spisok_grass_block = []
        self.spisok_dirt = []
        self.spisok_stone = []
        #self.models_world.setScale(30)
        #self.models_world.setPos(0, 250, -30) #влево/вправо +<) #вперёд/назад +на нас) #верх/низ -вверх)
        #self.models_world.setTexture(self.texture, 1)
        #self.models_world.reparentTo(render)
        self.generate_map()
        self.build_map()


    def build_map(self):
        with open('map.txt', 'r') as file:
            for line in file:
                x, y, z = line.split(',')
                block = loader.loadModel('block.egg')
                block.setScale(30)
                if int(z) < 2 * 30:
                    block.setTexture(self.texture_stone, 1)
                else:
                    block.setTexture(self.texture_dirt, 1)
                block.setPos(int(x), int(y), int(z))
                block.reparentTo(render)

    def generate_map(self):
        with open('map.txt', 'w') as file:
            for x in range(16):
                for y in range(16):
                    z = self.get_hate(x, y)
                    new_model_grass_block = self.models_world.copyTo(render)
                    new_model_grass_block.setTexture(self.texture_grass_block)
                    new_model_grass_block.setPos(x, y, z)
                    self.spisok_grass_block.append((x, y, z))
                    for d in range(3):
                        z -= 1
                        if z >= -10:
                            new_model_dirt = self.models_world.copyTo(render)
                            new_model_dirt.setTexture(self.texture_dirt)
                            new_model_dirt.setPos(x, y, z)
                            self.spisok_dirt.append((x, y, z))
                    for s in range(40):
                        z -= 1
                        if z >= -10:
                            new_model_stone = self.models_world.copyTo(render)
                            new_model_stone.setTexture(self.texture_stone)
                            new_model_stone.setPos(x, y, z)
                            self.spisok_stone.append((x, y, z))



    def get_hate(self, x , y):
        return int(5 * math.sin(x * 0.1) + 5 * math.cos(y * 0.1) + 5)




        '''for i in range(80):
                x = randint(0, 64)
                y = randint(0, 64)
                z = randint(0, 5)
                new_model_dirt = self.models_world.copyTo(render)
                new_model_dirt.setTexture(self.texture_dirt)
                new_model_dirt.setPos(x, y, z)'''
                #file.write(xyz)



            #for x in range(16):
                #for y in range(16):
                    #for z in range(5):
                        #xyz = str(x * 30) + ',' + str(y * 30) + ',' + str(z * 30) + '\n'
                        #file.write(xyz)




    def save_map(self):
        pass
