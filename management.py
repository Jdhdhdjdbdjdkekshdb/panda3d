from panda3d.core import *
from direct.task import Task
import sys

class MovementController():
    def __init__(self):

        base.disableMouse()
        #base.cam.lookAt(0, 0, 0)
        base.accept('escape', sys.exit)

        self.speed_x = 100.0
        self.speed_y = 30.0

        base.accept('w', self.set_move_forward, [True])
        base.accept('w-up', self.set_move_forward, [False])
        base.accept('s', self.set_move_backward, [True])
        base.accept('s-up', self.set_move_backward, [False])
        base.accept('a', self.set_move_left, [True])
        base.accept('a-up', self.set_move_left, [False])
        base.accept('d', self.set_move_right, [True])
        base.accept('d-up', self.set_move_right, [False])
        base.accept('space', self.set_move_up, [True])
        base.accept('space-up', self.set_move_up, [False])
        base.accept('shift', self.set_move_down, [True])
        base.accept('shift-up', self.set_move_down, [False])

        self.move_direction = Vec3(0, 0, 0)
        taskMgr.add(self.update_position, "update_position_task")


    def set_move_forward(self, value):
        self.move_direction.setY(self.speed_x if value else 0)

    def set_move_backward(self, value):
        self.move_direction.setY(-self.speed_x if value else 0)

    def set_move_left(self, value):
        self.move_direction.setX(-self.speed_x if value else 0)

    def set_move_right(self, value):
        self.move_direction.setX(self.speed_x if value else 0)

    def set_move_up(self, value):
        self.move_direction.setZ(self.speed_y if value else 0)

    def set_move_down(self, value):
        self.move_direction.setZ(-self.speed_y if value else 0)


    def update_position(self, task):
        dt = globalClock.getDt()
        base.cam.setPos(base.cam.getPos() + self.move_direction * dt)
        return Task.cont
