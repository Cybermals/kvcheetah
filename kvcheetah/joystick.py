"""kvcheetah - Joystick API"""

from math import atan2, cos, sin, sqrt

from kivy.factory import Factory
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


#Classes
#==============================================================================
class VirtualJoystick(Widget):
    """Base class for a virtual joystick."""
    def __init__(self, **kwargs):
        """Setup this virtual joystick."""
        super(VirtualJoystick, self).__init__(**kwargs)

        self._joy_pos = (0, 0)

        with self.canvas:
            Color(.5, .5, .5, .5)
            self.bg = Ellipse(pos = self.pos, size = self.size)
            Color(.75, .75, .75, 1)
            x, y = self.pos
            w, h = self.size
            self.thumb = Ellipse(pos = (x + w / 4, y + h / 4), 
                size = (w / 2, h / 2))

        self.bind(
            pos = self.update,
            size = self.update
        )

    def get_joy_pos(self):
        """Get the current joystick pos as coordinates within the range -1 to 1.
        """
        return self._joy_pos

    joy_pos = property(get_joy_pos)

    def update(self, *args):
        """Handle pos change."""
        x, y = self.pos
        w, h = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.thumb.pos = (x + w / 4, y + h / 4)
        self.thumb.size = (w / 2, h / 2)

    def on_touch_up(self, touch):
        """Handle touch up event."""
        #Reset thumb and joy pos
        x, y = self.pos
        w, h = self.size
        self.thumb.pos = (x + w / 4, y + h / 4)
        self._joy_pos = (0, 0)

    def on_touch_move(self, touch):
        """Handle dragging."""
        #Calculate the distance between the touch point and the joystick center
        cx, cy = self.center
        dx = touch.x - cx
        dy = touch.y - cy
        dist = sqrt(dx ** 2 + dy ** 2)

        #Calculate the angle between the touch point and the joystick center
        angle = atan2(dy, dx)

        #Cap the distance to ensure the thumb stays within the joystick radius
        w, h = self.size
        radius = w / 2
        dist = min(dist, radius)

        #Set the new thumb position
        dx = dist * cos(angle)
        dy = dist * sin(angle)
        self.thumb.pos = (
            cx + dx - w / 4, 
            cy + dy - h / 4
        )

        #Set new joystick pos
        self._joy_pos = (
            dx / (w / 2),
            dy / (h / 2)
        )


#Register Widgets
#===============================================================================
Factory.register("VirtualJoystick", VirtualJoystick)
