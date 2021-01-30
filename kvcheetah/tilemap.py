"""kvcheetah - TileMap API"""

from kivy.graphics import (
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
        self._size = (0, 0)
        self._viewport = (800, 600)
        self._tileset = None
        self._map_data = None
        self._ig = InstructionGroup()
        self._pos = Translate(0, 0)
        self._offset = (0, 0)
        self._tiles = None
        self._visible = False

        #Process keyword args
        if "parent" in kwargs:
            self.parent = kwargs["parent"]

        if "size" in kwargs:
            self.size = kwargs["size"]

        if "viewport" in kwargs:
            self.viewport = kwargs["viewport"]

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
        return self._size

    def set_size(self, value):
        """Set the size of this tilemap."""
        self._size = value

    size = property(get_size, set_size)

    def get_viewport(self):
        """Get the viewport size of this tilemap."""
        return self._viewport

    def set_viewport(self, value):
        """Set the viewport size of this tilemap."""
        self._viewport = value
        self.refresh()

    viewport = property(get_viewport, set_viewport)

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
        return self._offset

    def set_offset(self, value):
        """Set the offset of this tilemap."""
        self._offset = value
        self.update()

    offset = property(get_offset, set_offset)

    def refresh(self):
        """Refresh the internal data structures used for rendering."""
        #Clear old tiles and reinitialize them
        w, h = self.viewport
        w = int(w / 32) + 1
        h = int(h / 32) + 1
        self._ig.clear()
        self._tiles = [[Rectangle(pos = (x * 32, y * 32), size = (32, 32)) for x in range(w)] for y in range(h)]
        self._ig.add(PushMatrix())
        self._ig.add(self._pos)

        for row in self._tiles:
            for tile in row:
                self._ig.add(tile)

        self._ig.add(PopMatrix())

        #Update the data too
        self.update()

    def update(self):
        """Update this tilemap."""
        #Skip this if there is no tilset or no map data
        if self.tileset is None:
            Logger.warning("TileMap: No tileset assigned to tilemap.")
            return

        if self.map_data is None:
            Logger.warning("TileMap: No map data assigned to tilemap.")
            return

        #Calulate tilemap position and start tile
        ox, oy = self._offset
        x = ox % 32
        y = oy % 32
        tx = row_start = int(ox / 32)
        ty = int(oy / 32)

        #Update pos
        if self.parent is not None:
            px, py = self.parent.pos
            self._pos.xy = (px - x, py - y)

        else:
            self._pos.xy = (-x, -y)

        #Update the tiles
        vw, vh = self.viewport
        vw = int(vw / 32) + 1
        vh = int(vh / 32) + 1
        w, h = self.size

        for y in range(vh):
            for x in range(vw):
                if tx < 0 or tx > w - 1 or ty < 0 or ty > h - 1:
                    self._tiles[y][x].source = self.tileset[0]

                else:
                    self._tiles[y][x].source = self.tileset[self.map_data[ty][tx]]

                tx += 1

            ty += 1
            tx = row_start

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
            print("Hit Tile: {}".format(self.map_data[ty][tx]))
            return self.map_data[ty][tx]

        else:
            return -1