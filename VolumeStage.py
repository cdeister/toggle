# VolumeStage
import logging
from gi.repository import Clutter, Mx, Mash, Toggle

class VolumeStage(Clutter.Actor):
    def __init__(self, ui):
        super(VolumeStage, self).__init__()
        self.ui = ui
        self.p = self.ui.get_object("volume-stage")
        self.p.set_pivot_point (0.5, 0.5)
        self.p.set_pivot_point_z(0.5)
        self.p.set_reactive (True)

        self.stage = self.ui.get_object("stage")
        self.stage.connect("button-press-event", self.click)
        self.stage.connect("button-release-event", self.release)
        self.stage.connect("motion-event", self.move)
        self.stage.connect("touch-event", self.touch)
        self.clicked = False

        self.last_x = 0
        self.last_y = 0
        self.start_x = self.p.get_rotation_angle(Clutter.RotateAxis.Y_AXIS)
        self.start_y = self.p.get_rotation_angle(Clutter.RotateAxis.X_AXIS)

    def click(self, actor, event):
        self.last_x = event.x
        self.last_y = event.y
        self.start_x = self.p.get_rotation_angle(Clutter.RotateAxis.Y_AXIS)
        self.start_y = self.p.get_rotation_angle(Clutter.RotateAxis.X_AXIS)
        self.clicked = True

    def release(self, actor, event):
        self.clicked = False

    def move(self, actor, event):
        if self.clicked:
            dmx = event.x-self.last_x
            dmy = event.y-self.last_y
            rot_x = self.start_x+dmx
            rot_y = self.start_y+dmy
            self.p.set_rotation_angle(Clutter.RotateAxis.X_AXIS, rot_x)
            self.p.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, rot_y)

    def touch(self, actor, event):
        (x, y) = event.get_coords()
        event.x = x
        event.y = y
        #logging.debug("(x, y, evt):"+str(x)+", "+str(y)+", "+str(event.type()))
        if event.type() == Clutter.EventType.TOUCH_UPDATE:
            self.move(actor, event)
        elif event.type() == Clutter.EventType.TOUCH_BEGIN:
            self.click(actor, event)
        elif event.type() == Clutter.EventType.TOUCH_END:
            self.release(actor, event)

