"""kvcheetah - TileMap API"""

from kivy.graphics import (
    ClearBuffers,
    ClearColor,
    Fbo,
    InstructionGroup,
    PopMatrix,
    PushMatrix,
    Rectangle,
    Translate
)
from kivy.logger import Logger


#Classes
#===============================================================================
class TileMap(object):
    """Base class for a tilemap."""
    def __init__(self, **kwargs):
        """Setup this tilemap."""
        self._parent = None
        self._tileset = None
        self._map_data = None
        self._tiles = None
        self._visible = False
        self._ig = InstructionGroup()
        self._offset = Translate(0, 0)
        self._fbo = Fbo(size = (32, 32))
        self._rect = Rectangle(pos = (0, 0), size = (32, 32), 
            texture = self._fbo.texture)

        self._ig.add(PushMatrix())
        self._ig.add(self._offset)
        self._ig.add(self._rect)
        self._ig.add(PopMatrix())

        #Process keyword args
        if "parent" in kwargs:
            self.parent = kwargs["parent"]

        if "tileset" in kwargs:
            self.tileset = kwargs["tileset"]

        if "map_data" in kwargs:
            self.map_data = kwargs["map_data"]

        if "offset" in kwargs:
            self.offset = kwargs["offset"]

    def __del__(self):
        """Destroy this tilemap."""
        #Ensure that this tilemap is hidden before destroying it
        try:
            self.show(False)

        except ReferenceError:
            pass

        #We must clear the Fbo to prevent a memory leak
        self._fbo.clear()

    def get_parent(self):
        """Get the parent of this tilemap."""
        return self._parent

    def set_parent(self, value):
        """Set the parent of this tilemap."""
        #Ensure that this tilemap is hidden
        if self.visible:
            self.show(False)

        #Set the new parent
        self._parent = value

    def get_visible(self):
        """Get the visibility state of this tilemap."""
        return self._visible

    visible = property(get_visible)

    def get_size(self):
        """Get the size of this tilemap."""
        if self.map_data is None:
            return (0, 0)

        return (len(self.map_data[0]), len(self.map_data))

    size = property(get_size)

    def get_tileset(self):
        """Get the tileset for this tilemap."""
        return self._tileset

    def set_tileset(self, value):
        """Set the tileset for this tilemap."""
        self._tileset = value
        self.update()

    tileset = property(get_tileset, set_tileset)

    def get_map_data(self):
        """Get the map data for this tilemap."""
        return self._map_data

    def set_map_data(self, value):
        """Set the map data for this tilemap."""
        self._map_data = value
        self.update()

    map_data = property(get_map_data, set_map_data)

    def get_offset(self):
        """Get the offset of this tilemap."""
        #Adjust the current offset based on the parent pos
        x, y = self._offset.xy

        if self.parent is not None:
            px, py = self.parent.pos
            x -= px
            y -= py

        return (-x, -y)

    def set_offset(self, value):
        """Set the offset of this tilemap."""
        #Adjust the new offset based on the parent pos
        if self.parent is not None:
            x, y = value
            px, py = self.parent.pos
            x += px
            y += py
            value = (-x, -y)

        self._offset.xy = value

    offset = property(get_offset, set_offset)

    def update(self):
        """Update the tilemap texture."""
        #Skip this if there is no tileset or map data
        if self.tileset is None:
            Logger.warning("TileMap: There is no assigned tileset.")
            return

        if self.map_data is None:
            Logger.warning("TileMap: There is no map data.")
            return

        #Update Fbo size
        w, h = self.size
        w = w * 32
        h = h * 32
        self._fbo.size = (w, h)
        self._rect.size = (w, h)
        self._rect.texture = self._fbo.texture

        #Draw the new tiles
        self._fbo.clear()

        with self._fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()

            #Draw each tile
            x = 0
            y = 0

            for row in self.map_data:
                for tile in row:
                    Rectangle(pos = (x, y), size = (32, 32), 
                        source = self.tileset[tile])
                    x += 32

                y += 32
                x = 0

            #Force a redraw of the Fbo
            self._fbo.draw()

    def show(self, do_show):
        """Show/hide this tilemap."""
        #Ensure that this tilemap has a parent
        if self.parent is None:
            Logger.warning("TileMap: No parent assigned to tilemap.")
            return

        #Show the tilemap
        if do_show and not self.visible:
            self.parent.canvas.add(self._ig)

        #Hide the tilemap
        elif not do_show and self.visible:
            self.parent.canvas.remove(self._ig)

        #Update vibility state
        self._visible = do_show

    def hit(self, sprite):
        """Check what tile on this tilemap was hit by the given sprite. This will
        return -1 if the sprite lies outside the bounds of the tilemap.
        """
        #Calculate the tile the sprite will be over
        ox, oy = self.offset
        x, y = sprite.pos
        vx, vy = sprite.velocity
        x += ox + vx
        y += oy + vy
        tx = int(x / 32)
        ty = int(y / 32)

        #Return the index of the tile
        w, h = self.size

        if tx > 0 and tx < w and ty > 0 and ty < h:
            return self.map_data[ty][tx]

        else:
            return -1