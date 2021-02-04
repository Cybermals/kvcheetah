"""kvcheetah - Testing Framework"""

from math import cos, sin, degrees
import os
from random import randint, random

from kivy.app import App, Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

try:
    #Try to import from the package folder
    from __init__ import __version__
    from sprite import Sprite
    from tilemap import TileMap

except ImportError:
    #Try to import with fully-qualified package name
    import kvcheetah
    from kvcheetah import __version__
    from kvcheetah.sprite import Sprite
    from kvcheetah.tilemap import TileMap

    #Ensure that the current working directory is the kvcheetah package folder
    os.chdir(os.path.dirname(kvcheetah.__file__))


#Globals
#==============================================================================
KVLANG = """
<DemoBase>:
    demo_area: DemoArea

    BoxLayout:
        orientation: "vertical"

        Button:
            text: "Menu"
            size_hint_y: .1
            on_release: self.parent.parent.menu()

        StencilView:
            id: DemoArea


<JoystickDemo>:
    pos_lbl: PosLabel
    joystick: Joystick

    Label:
        id: PosLabel
        text: "Joystick Pos: (0, 0)"
        center: self.center

    VirtualJoystick:
        id: Joystick
        size_hint: (None, None)
        pos: (50, 50)
        size: (100, 100)


<MainScreen>:
    Screen:
        name: "Menu"

        BoxLayout:
            orientation: "vertical"

            Label:
                text: "Choose a demo below:"
                size_hint_y: .1

            ScrollView:
                BoxLayout:
                    orientation: "vertical"

                    Button:
                        text: "Sprite Demo"
                        on_release: root.switch_screen("SpriteDemo")

                    Button:
                        text: "Sprite Color Demo"
                        on_release: root.switch_screen("SpriteColorDemo")

                    Button:
                        text: "TileMap Demo"
                        on_release: root.switch_screen("TileMapDemo")

                    Button:
                        text: "Joystick Demo"
                        on_release: root.switch_screen("JoystickDemo")

    SpriteDemo:
        name: "SpriteDemo"

    SpriteColorDemo:
        name: "SpriteColorDemo"

    TileMapDemo:
        name: "TileMapDemo"

    JoystickDemo:
        name: "JoystickDemo"
"""
POP_SND = SoundLoader.load("data/sfx/bubble-pop.wav")


#Classes
#==============================================================================
class Bubble(Sprite):
    """Base class for a bubble."""
    def __init__(self, **kwargs):
        """Setup this bubble."""
        super(Bubble, self).__init__(**kwargs)
        self.pos = (
            randint(32, int(self.parent.width) - 32),
            randint(32, int(self.parent.height) - 32)
        )
        self.size = (64, 64)
        self.origin = (32, 32)
        self.source = "atlas://data/images/sprites/bubble"
        self.velocity = (
            2 * cos(degrees(randint(0, 359))),
            2 * sin(degrees(randint(0, 359)))
        )
        self._hp = 10
        self._destroy_cb = None

        #Process keyword args
        if "destroy_cb" in kwargs:
            self.destroy_cb = kwargs["destroy_cb"]

    def get_hp(self):
        """Get the HP of this bubble."""
        return self._hp

    def set_hp(self, value):
        """Set the HP of this bubble."""
        self._hp = value

        if value <= 0:
            try:
                POP_SND.seek(0)
                POP_SND.play()

            except Exception:
                pass

            self.source = "atlas://data/images/sprites/bubble-pop"
            self.velocity = (0, 0)
            Clock.schedule_once(self.destroy, .5)

    hp = property(get_hp, set_hp)

    def get_destroy_cb(self):
        """Get the destroy callback for this bubble."""
        return self._destroy_cb

    def set_destroy_cb(self, value):
        """Set the destroy callback for this bubble."""
        self._destroy_cb = value

    destroy_cb = property(get_destroy_cb, set_destroy_cb)

    def invert_velocity(self):
        """Invert the velocity of this bubble."""
        vx, vy = self.velocity
        self.velocity = (-vx, -vy)

    def destroy(self, t):
        """Destroy this bubble."""
        try:
            self.destroy_cb(self)

        except Exception:
            pass

    def update(self):
        """Update this bubble."""
        #Update velocity
        x, y = self.pos
        vx, vy = self.velocity

        if x < 32 or x > self.parent.width - 33:
            vx = -vx

        if y < 32 or y > self.parent.height - 33:
            vy = -vy

        self.velocity = (vx, vy)
        super(Bubble, self).update()


class Pin(Sprite):
    """Base class for a pin."""
    def __init__(self, **kwargs):
        """Setup this pin."""
        super(Pin, self).__init__(**kwargs)
        self.size = (10, 64)
        self.origin = (5, 64)
        self.source = "atlas://data/images/sprites/pin"


class Egg(Sprite):
    """Base class for an egg."""
    def __init__(self, **kwargs):
        """Setup this egg."""
        super(Egg, self).__init__(**kwargs)
        self.size = (48, 64)
        self.origin = (24, 32)
        self.source = "atlas://data/images/sprites/egg"


class Ball(Sprite):
    """Base class for a ball."""
    def __init__(self, **kwargs):
        """Setup this ball."""
        super(Ball, self).__init__(**kwargs)
        self.pos = (self.parent.width / 2, self.parent.height)
        self.size = (64, 64)
        self.origin = (32, 32)
        self.velocity = (0, -2)
        self.source = "atlas://data/images/sprites/ball"

    def update(self):
        """Update this ball."""
        #Update velocity
        vx, vy = self.velocity
        vy -= 1
        
        if vy > 16:
            vy = 16

        if self.parent.parent.parent.tilemap.hit(self) > 0:
            vy = -vy

        self.velocity = (vx, vy)
        super(Ball, self).update()


class DemoBase(Screen):
    """Base class for a demo screen."""
    def menu(self):
        """Return to the main menu."""
        self.parent.switch_screen("Menu")


class SpriteDemo(DemoBase):
    """A simple sprite demo."""
    def __init__(self, **kwargs):
        """Setup this demo."""
        super(SpriteDemo, self).__init__(**kwargs)
        self.spawn_tmr = 0

    def on_enter(self):
        """Handle enter event."""
        #Creat the pin
        self.pin = Pin(parent = self.demo_area)

        #Init bubble collection
        self.bubbles = []

        #Start the demo
        self.frame_event = Clock.schedule_interval(self.update, 1 / 60)

    def on_leave(self):
        """Handle leave event."""
        #Stop the demo
        self.frame_event.cancel()

        #Destroy bubbles
        self.bubbles = None

        #Destroy pin
        self.pin = None

    def on_touch_down(self, touch):
        """Handle touch down event."""
        super(SpriteDemo, self).on_touch_down(touch)
        self.pin.pos = (touch.x, touch.y)
        self.pin.show(True)

    def on_touch_up(self, touch):
        """Handle touch up event."""
        super(SpriteDemo, self).on_touch_up(touch)
        self.pin.show(False)

    def on_touch_move(self, touch):
        """Handle touch move event."""
        super(SpriteDemo, self).on_touch_move(touch)
        self.pin.pos = (touch.x, touch.y)

    def spawn_bubble(self):
        """Spawn a new bubble."""
        #Update spawn timer
        self.spawn_tmr -= 1

        #Spawn a new bubble if the timer has expired and there are less than 10
        #bubbles.
        if self.spawn_tmr <= 0 and len(self.bubbles) < 10:
            self.bubbles.append(Bubble(
                parent = self.demo_area,
                destroy_cb = self.destroy_bubble
            ))
            self.bubbles[-1].show(True)
            self.spawn_tmr = 100

    def destroy_bubble(self, bubble):
        """Destroy the given bubble."""
        self.bubbles.remove(bubble)

    def update(self, t):
        """Update this demo."""
        #Spawn a new bubble
        self.spawn_bubble()

        #Update bubbles
        for bubble in self.bubbles:
            #Update bubble
            bubble.update()

            #Do collision detection
            if bubble.hit(self.pin):
                bubble.hp = 0
                continue

            for bubble2 in self.bubbles:
                if bubble2.hp > 0 and bubble.hit(bubble2, "circle"):
                    bubble.invert_velocity()
                    bubble.hp -= 1


class SpriteColorDemo(DemoBase):
    """A sprite color demo."""
    def __init__(self, **kwargs):
        """Setup this demo."""
        super(SpriteColorDemo, self).__init__(**kwargs)
        self.color_tmr = 0

    def on_enter(self):
        """Handle enter event."""
        #Create the egg
        self.egg = Egg(parent = self.demo_area)
        self.egg.pos = (self.width / 2, self.height / 2)
        self.egg.show(True)

        #Start the demo
        self.frame_event = Clock.schedule_interval(self.update, 1 / 60)

    def on_leave(self):
        """Handle leave event."""
        #Stop the demo
        self.frame_event.cancel()

        #Destroy the egg
        self.egg = None

    def update(self, t):
        """Update this demo."""
        #Update color change timer
        self.color_tmr -= 1

        #Change the egg color if the timer has expired
        if self.color_tmr <= 0:
            self.egg.color = (
                randint(0, 255) / 255,
                randint(0, 255) / 255,
                randint(0, 255) / 255,
                1
            )
            self.color_tmr = 30


class TileMapDemo(DemoBase):
    """A tilemap demo."""
    def on_enter(self):
        """Handle enter event."""
        #Init tileset and map data
        tileset = [
            "atlas://data/images/tiles/blank",
            "atlas://data/images/tiles/dirt",
            "atlas://data/images/tiles/grass",
            "atlas://data/images/tiles/dirt-slope1",
            "atlas://data/images/tiles/dirt-slope2",
            "atlas://data/images/tiles/grass-slope1",
            "atlas://data/images/tiles/grass-slope2",
            "atlas://data/images/tiles/grass-slope-base1",
            "atlas://data/images/tiles/grass-slope-base2"
        ]
        map_data = [[0 for x in range(128)] for y in range(128)]

        #Add dirt tiles
        for y in range(2):
            for x in range(128):
                map_data[y][x] = 1

        #Add grass tiles
        for x in range(128):
            map_data[2][x] = 2

        #Add a small hill
        map_data[2][29] = 7
        map_data[3][29] = 5
        map_data[2][30] = 1
        map_data[3][30] = 7
        map_data[4][30] = 5
        map_data[2][31] = 1
        map_data[3][31] = 1
        map_data[4][31] = 7
        map_data[5][31] = 5

        #Create the tilemap
        self.tilemap = TileMap(
            parent = self.demo_area,
            tileset = tileset,
            map_data = map_data
            )
        self.tilemap.show(True)

        #Create a ball
        self.ball = Ball(parent = self.demo_area)
        self.ball.show(True)

        #Start the demo
        self.frame_event = Clock.schedule_interval(self.update, 1 / 60)

    def on_leave(self):
        """Handle leave event."""
        #Stop the demo
        self.frame_event.cancel()

        #Destroy the ball
        self.ball = None

        #Destroy the tilemap
        self.tilemap = None

    def update(self, t):
        """Update this demo."""
        #Scroll the tilemap horizontally
        x, y = self.tilemap.offset
        x += 2
        self.tilemap.offset = (x, y)

        #Update the ball
        self.ball.update()


class JoystickDemo(DemoBase):
    """A joystick demo."""
    def on_enter(self):
        """Handle enter event."""
        #Start the demo
        self.frame_event = Clock.schedule_interval(self.update, 1 / 60)

    def on_leave(self):
        """Handle leave event."""
        #Stop the demo
        self.frame_event.cancel()

    def update(self, t):
        """Update this demo."""
        self.pos_lbl.text = "Joystick Pos: {}".format(self.joystick.joy_pos)


class MainScreen(ScreenManager):
    """The main screen of this app."""
    def switch_screen(self, name):
        """Switch to the given screen."""
        if name == "Menu":
            self.transition = SlideTransition(direction = "right")

        else:
            self.transition = SlideTransition(direction = "left")

        self.current = name


class KvCheetahApp(App):
    """A basic app class."""
    def build(self):
        """Build the UI for this app."""
        self.title = "KvCheetah v{}".format(__version__)
        Builder.load_string(KVLANG)
        return MainScreen()


#Register classes
#==============================================================================
Factory.register("SpriteDemo", SpriteDemo)


#Entry Point
#==============================================================================
KvCheetahApp().run()