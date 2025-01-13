from panda3d.core import WindowProperties, Vec3
from direct.task import Task
import sys

class CameraController():
    def __init__(self):
        super().__init__()

        # Отключаем стандартное управление камерой
        base.disableMouse()

        # Инициализация параметров камеры
        self.angle_h = 0  # Угол поворота по горизонтали
        self.angle_v = 0  # Угол поворота по вертикали

        # Инициализация параметров движения
        self.speed_x = 100.0
        self.speed_y = 30.0
        self.move_direction = Vec3(0, 0, 0)

        # Настройка окна
        props = WindowProperties()
        props.setCursorHidden(True)  # Скрываем курсор
        base.win.requestProperties(props)
        self.center_mouse()

        # Привязываем события клавиш
        base.accept('escape', sys.exit)
        base.accept('w', self.set_move, ["forward", True])
        base.accept('w-up', self.set_move, ["forward", False])
        base.accept('s', self.set_move, ["backward", True])
        base.accept('s-up', self.set_move, ["backward", False])
        base.accept('a', self.set_move, ["left", True])
        base.accept('a-up', self.set_move, ["left", False])
        base.accept('d', self.set_move, ["right", True])
        base.accept('d-up', self.set_move, ["right", False])
        base.accept('space', self.set_move, ["up", True])
        base.accept('space-up', self.set_move, ["up", False])
        base.accept('shift', self.set_move, ["down", True])
        base.accept('shift-up', self.set_move, ["down", False])

        # Добавляем задачи
        base.taskMgr.add(self.update_camera, "update_camera_task")
        base.taskMgr.add(self.update_position, "update_position_task")

    def center_mouse(self):
        """Устанавливаем курсор в центр окна."""
        window_center_x = base.win.getProperties().getXSize() / 2
        window_center_y = base.win.getProperties().getYSize() / 2
        base.win.movePointer(0, int(window_center_x), int(window_center_y))

    def update_camera(self, task):
        """Обновляем поворот камеры на основе движения мыши."""
        mouse_x = base.win.getPointer(0).getX()
        mouse_y = base.win.getPointer(0).getY()

        window_width = base.win.getProperties().getXSize()
        window_height = base.win.getProperties().getYSize()

        # Вычисляем смещение мыши от центра
        delta_x = (mouse_x - window_width / 2) * 0.1
        delta_y = (mouse_y - window_height / 2) * 0.1

        # Обновляем углы поворота камеры
        self.angle_h -= delta_x
        self.angle_v -= delta_y

        # Ограничиваем вертикальный угол
        self.angle_v = max(-89, min(89, self.angle_v))

        # Центрируем курсор
        self.center_mouse()

        # Применяем вращение к камере
        base.camera.setH(self.angle_h)
        base.camera.setP(self.angle_v)

        return Task.cont

    def set_move(self, direction, value):
        """Устанавливаем направление движения."""
        if direction == "forward":
            self.move_direction.setY(self.speed_x if value else 0)
        elif direction == "backward":
            self.move_direction.setY(-self.speed_x if value else 0)
        elif direction == "left":
            self.move_direction.setX(-self.speed_x if value else 0)
        elif direction == "right":
            self.move_direction.setX(self.speed_x if value else 0)
        elif direction == "up":
            self.move_direction.setZ(self.speed_y if value else 0)
        elif direction == "down":
            self.move_direction.setZ(-self.speed_y if value else 0)

    def update_position(self, task):
        """Обновляем позицию камеры на основе направления движения."""
        dt = globalClock.getDt()
        base.camera.setPos(base.camera.getPos() + self.move_direction * dt)
        return Task.cont