"""kvcheetah - Sprite API"""

from math import sqrt

from kivy.graphics import (
    Color,
    InstructionGroup,
    PopMatrix,
    PushMatrix,
    Rectangle,
    Rotate,
    Translate
)
from kivy.logger import Logger


#Classes
#==============================================================================
class Sprite(object):
    """Base class for a sprite."""
    def __init__(self, **kwargs):
        """Setup this sprite."""
        self._parent = None
        self._visible = False
        self._velocity = (0, 0)

        self._ig = InstructionGroup()
        self._pos = Translate(0, 0)
        self._rot = Rotate(0)
        self._origin = Translate(0, 0)
        self._color = Color(1, 1, 1, 1)
        self._rect = Rectangle(pos = (0, 0), size = (1, 1))
        
        self._ig.add(PushMatrix())
        self._ig.add(self._pos)
        self._ig.add(self._rot)
        self._ig.add(self._origin)
        self._ig.add(self._color)
        self._ig.add(self._rect)
        self._ig.add(PopMatrix())

        #Process keyword args
        if "parent" in kwargs:
            self.parent = kwargs["parent"]

        if "pos" in kwargs:
            self.pos = kwargs["pos"]

        if "size" in kwargs:
            self.size = kwargs["size"]

        if "origin" in kwargs:
            self.origin = kwargs["origin"]

        if "rot" in kwargs:
            self.rot = kwargs["rot"]

        if "color" in kwargs:
            self.color = kwargs["color"]

        if "source" in kwargs:
            self.source = kwargs["source"]

        if "texture" in kwargs:
            self.texture = kwargs["texture"]

    def __del__(self):
        """Destroy this sprite."""
        #Ensure that this sprite is hidden before destroying it
        try:
            self.show(False)

        except ReferenceError:
            pass

    def get_parent(self):
        """Get the parent of this sprite."""
        return self._parent

    def set_parent(self, value):
        """Set the parent of this sprite."""
        #Ensure that this sprite is hidden
        if self.visible:
            self.show(False)

        #Change the parent
        self._parent = value

    parent = property(get_parent, set_parent)

    def get_visible(self):
        """Is this sprite visible?"""
        return self._visible

    visible = property(get_visible)

    def get_pos(self):
        """Get the position of this sprite."""
        #Adjust current pos based on parent pos
        x, y = self._pos.xy

        if self.parent is not None:
            px, py = self.parent.pos
            x -= px
            y -= py

        return (x, y)

    def set_pos(self, value):
        """Set the position of this sprite."""
        #Adjust new pos based on parent pos
        if self.parent is not None:
            px, py = self.parent.pos
            x, y = value
            x += px
            y += py
            value = (x, y)

        self._pos.xy = value
    
    pos = property(get_pos, set_pos)

    def get_size(self):
        """Get the size of this sprite."""
        return self._rect.size

    def set_size(self, value):
        """Set the size of this sprite."""
        self._rect.size = value

    size = property(get_size, set_size)

    def get_origin(self):
        """Get the origin of this sprite."""
        x, y = self._origin.xy
        return (-x, -y)

    def set_origin(self, value):
        """Set the origin of this sprite."""
        x, y = value
        self._origin.xy = (-x, -y)

    origin = property(get_origin, set_origin)

    def get_center(self):
        """Get the center of this sprite."""
        x, y = self.pos
        ox, oy = self.origin
        w, h = self.size
        return (x - ox + w / 2, y - oy + h / 2)

    center = property(get_center)

    def get_rot(self):
        """Get the rotation of this sprite."""
        return self._rot.angle

    def set_rot(self, value):
        self._rot.angle = value

    rot = property(get_rot, set_rot)

    def get_velocity(self):
        """Get the velocity of this sprite."""
        return self._velocity

    def set_velocity(self, value):
        """Set the velocity of this sprite."""
        self._velocity = value

    velocity = property(get_velocity, set_velocity)

    def get_color(self):
        """Get the color of this sprite."""
        return self._color.rgba

    def set_color(self, value):
        """Set the color of this sprite."""
        self._color.rgba = value

    color = property(get_color, set_color)

    def get_source(self):
        """Get the source image for this sprite."""
        return self._rect.source

    def set_source(self, value):
        """Set the source image for this sprite."""
        self._rect.source = value

    source = property(get_source, set_source)

    def get_texture(self):
        """Get the texture for this sprite."""
        return self._rect.texture

    def set_texture(self, value):
        """Set the texture for this sprite."""
        self._rect.texture = value

    texture = property(get_texture, set_texture)

    def show(self, do_show):
        """Show/hide this sprite."""
        #Ensure that this sprite has a parent
        if self.parent is None:
            Logger.warning("Sprite: No parent assigned to sprite.")
            return

        #Show this sprite
        if do_show and not self.visible:
            self.parent.canvas.add(self._ig)

        #Hide this sprite
        elif not do_show and self.visible:
            self.parent.canvas.remove(self._ig)

        #Update visibility state
        self._visible = do_show

    def hit(self, sprite, type = "box"):
        """Check if this sprite has collided with the given sprite.
        Valid collision types are: "box" and "circle".
        """
        #Skip collision detection between a sprite and itself
        if sprite == self:
            return False

        #Gather data needed for collision detection
        cx, cy = self.center
        w, h = self.size
        cx2, cy2 = sprite.center
        w2, h2 = sprite.size
        dx = abs(cx2 - cx)
        dy = abs(cy2 - cy)

        #Do bounding box collision detection
        if type == "box":
            return (dx < (w + w2) / 2 and dy < (h + h2) / 2)

        #Do circle-based collision detection
        elif type == "circle":
            r = max(w, h) / 2
            r2 = max(w2, h2) / 2
            dist = sqrt(dx ** 2 + dy ** 2)
            return dist < r + r2

        #Handle unknown collision type
        else:
            Logger.warning("Sprite: No such collision type '{}'".format(type))
            return False

    def update(self):
        """Update this sprite. Override this method in a derived class."""
        #Apply velocity
        x, y = self.pos
        vx, vy = self.velocity
        self.pos = (x + vx, y + vy)
        