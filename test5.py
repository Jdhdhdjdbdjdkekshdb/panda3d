from panda3d.core import WindowProperties, Vec3
from direct.task import Task
import sys

class CameraController():
    def __init__(self):
        # Инициализация параметров
        self.angle_h = 0  # Горизонтальный угол
        self.angle_v = 0  # Вертикальный угол
        self.speed = 50.0  # Скорость движения (по горизонтали)
        self.vertical_speed = 20.0  # Скорость движения по оси Z (вверх/вниз)
        self.movement = {"forward": 0, "backward": 0, "left": 0, "right": 0, "up": 0, "down": 0}  # Направления движения

        # Скрытие курсора и его блокировка в центре экрана
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.center_mouse()

        # Отключаем стандартное управление камерой
        base.disableMouse()

        # Привязка клавиш
        base.accept('escape', sys.exit)
        base.accept('w', self.set_movement, ["forward", 1])
        base.accept('w-up', self.set_movement, ["forward", 0])
        base.accept('s', self.set_movement, ["backward", 1])
        base.accept('s-up', self.set_movement, ["backward", 0])
        base.accept('a', self.set_movement, ["left", 1])
        base.accept('a-up', self.set_movement, ["left", 0])
        base.accept('d', self.set_movement, ["right", 1])
        base.accept('d-up', self.set_movement, ["right", 0])
        base.accept('space', self.set_movement, ["up", 1])
        base.accept('space-up', self.set_movement, ["up", 0])
        base.accept('shift', self.set_movement, ["down", 1])
        base.accept('shift-up', self.set_movement, ["down", 0])

        # Задачи для обновления камеры и движения
        base.taskMgr.add(self.update_camera, "update_camera_task")
        base.taskMgr.add(self.update_movement, "update_movement_task")

    def center_mouse(self):
        """Устанавливает курсор в центр экрана."""
        window_center_x = base.win.getProperties().getXSize() // 2
        window_center_y = base.win.getProperties().getYSize() // 2
        base.win.movePointer(0, window_center_x, window_center_y)

    def update_camera(self, task):
        """Обновление направления камеры по движению мыши."""
        mouse_x = base.win.getPointer(0).getX()
        mouse_y = base.win.getPointer(0).getY()

        window_width = base.win.getProperties().getXSize()
        window_height = base.win.getProperties().getYSize()

        # Вычисление смещения мыши
        delta_x = (mouse_x - window_width / 2) * 0.1
        delta_y = (mouse_y - window_height / 2) * 0.1

        # Обновление углов
        self.angle_h -= delta_x
        self.angle_v = max(-89, min(89, self.angle_v - delta_y))

        # Применение углов к камере
        base.camera.setH(self.angle_h)
        base.camera.setP(self.angle_v)

        # Центрирование курсора
        self.center_mouse()

        return Task.cont

    def set_movement(self, direction, value):
        """Установка значения движения в заданном направлении."""
        self.movement[direction] = value

    def update_movement(self, task):
        """Обновление позиции камеры с учетом направления движения."""
        dt = globalClock.getDt()

        # Получаем вектор направления камеры по горизонтали
        heading_matrix = base.camera.getMat().getUpper3().getRow(0)
        forward_vec = Vec3(heading_matrix[0], heading_matrix[1], 0)
        forward_vec.normalize()

        # Перпендикулярный вектор для движения вправо/влево
        right_vec = Vec3(forward_vec.getY(), -forward_vec.getX(), 0)
        right_vec.normalize()

        # Направление вверх/вниз (по оси Z)
        up_vec = Vec3(0, 0, 1)

        # Вычисляем итоговый вектор перемещения
        move_vec = (
            forward_vec * (self.movement["forward"] - self.movement["backward"]) +  # Это теперь forward/backward
            right_vec * (self.movement["right"] - self.movement["left"]) +  # Это теперь right/left
            up_vec * (self.movement["up"] - self.movement["down"])  # Это теперь up/down
        )
        # Нормализация вектора и обновление позиции камеры
        if move_vec.length_squared() > 0:
            move_vec.normalize()  # Нормализация для равномерной скорости
            base.camera.setPos(base.camera.getPos() + move_vec * self.speed * dt)

        # Обновление вертикальной скорости (взлет/падение)
        if self.movement["up"]:
            base.camera.setPos(base.camera.getPos() + up_vec * self.vertical_speed * dt)
        if self.movement["down"]:
            base.camera.setPos(base.camera.getPos() - up_vec * self.vertical_speed * dt)

        return Task.cont