from panda3d.core import Point3, Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()

        # Загружаем куб
        self.cube = self.loader.loadModel("models/box")
        self.cube.setScale(1, 1, 1)
        self.cube.setPos(0, 10, 0)
        self.cube.reparentTo(self.render)

        # Устанавливаем камеру в центр куба
        self.camera.setPos(self.cube.getPos() + Vec3(0, 0, 0))
        self.camera.lookAt(self.cube)

        # Захват мыши
        self.disableMouse()
        self.mouse_sensitivity = 0.1

        # Переменные для хранения углов поворота
        self.pitch = 0
        self.yaw = 0

        # Задаем обработчик событий мыши
        self.taskMgr.add(self.update_camera, "update_camera")

    def update_camera(self, task):
        # Получаем текущие координаты мыши
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            dx = mpos.getX() * self.mouse_sensitivity * 100  # Увеличиваем чувствительность
            dy = mpos.getY() * self.mouse_sensitivity * 100

            # Обновляем углы поворота
            self.yaw += dx
            self.pitch -= dy

            # Ограничиваем наклон (pitch) камеры
            self.pitch = max(-89, min(89, self.pitch))

            # Устанавливаем позицию камеры в центр куба
            cube_pos = self.cube.getPos()
            self.camera.setPos(cube_pos + Vec3(0, 0, 0))

            # Поворачиваем камеру по углам yaw и pitch
            self.camera.setHpr(self.yaw, self.pitch, 0)

            # Сбрасываем положение мыши (это не скрывает курсор, но позволяет игнорировать его)
            self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)

        return Task.cont

app = MyApp()
app.run()