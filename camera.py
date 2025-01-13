from panda3d.core import WindowProperties
from direct.task import Task

class Camera():
    def __init__(self):
        super().__init__()

        # Устанавливаем начальные углы поворота камеры
        self.angle_h = 0  # Угол поворота по горизонтали
        self.angle_v = 0  # Угол поворота по вертикали

        # Скрываем курсор и фиксируем его
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        # Центрируем курсор
        self.center_mouse()

        # Добавляем задачу для обновления направления камеры
        base.taskMgr.add(self.update_camera_task, "update_camera_task")

    def center_mouse(self):
        # Устанавливаем курсор в центр окна
        window_center_x = base.win.getProperties().getXSize() / 2
        window_center_y = base.win.getProperties().getYSize() / 2
        base.win.movePointer(0, int(window_center_x), int(window_center_y))

    def update_camera_task(self, task):
        # Получаем текущее положение мыши
        mouse_x = base.win.getPointer(0).getX()
        mouse_y = base.win.getPointer(0).getY()

        # Получаем размеры окна
        window_width = base.win.getProperties().getXSize()
        window_height = base.win.getProperties().getYSize()

        # Вычисляем смещение мыши от центра
        delta_x = (mouse_x - window_width / 2) * 0.1  # Уменьшаем чувствительность
        delta_y = (mouse_y - window_height / 2) * 0.1

        # Обновляем углы поворота камеры на основе смещения мыши с инверсией по оси X
        self.angle_h -= delta_x  # Инвертируем угол поворота по горизонтали
        self.angle_v -= delta_y

        # Ограничиваем вертикальный угол поворота
        self.angle_v = max(-89, min(89, self.angle_v))

        # Центрируем курсор снова
        self.center_mouse()

        # Устанавливаем камеру на фиксированную позицию и поворачиваем её
        base.camera.setPos(0, -10, 0)  # Камера стоит на месте (x=0, y=-10, z=0)

        # Поворачиваем камеру в зависимости от углов
        base.camera.lookAt(0, 0, 0)  # Смотрим на центр сцены (куб)

        # Применяем вращение к камере
        base.camera.setH(self.angle_h)  # Угол поворота по горизонтали
        base.camera.setP(self.angle_v)  # Угол поворота по вертикали

        return Task.cont
