"""kvcheetah - Testing Framework"""

from math import cos, sin, degrees
from random import randint, random

from kivy.app import App, Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

try:
    #Try to import from the package folder
    from sprite import Sprite

except ImportError:
    #Try to import with fully-qualified package name
    from kvcheetah.sprite import Sprite


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

    SpriteDemo:
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
        super(Bubble, self).update()

        #Update velocity
        x, y = self.pos
        vx, vy = self.velocity

        if x < 32 or x > self.parent.width - 33:
            vx = -vx

        if y < 32 or y > self.parent.height - 33:
            vy = -vy

        self.velocity = (vx, vy)


class Pin(Sprite):
    """Base class for a pin."""
    def __init__(self, **kwargs):
        """Setup this pin."""
        super(Pin, self).__init__(**kwargs)
        self.size = (10, 64)
        self.origin = (5, 64)
        self.source = "atlas://data/images/sprites/pin"


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
        self.name = "SpriteDemo"
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
        Builder.load_string(KVLANG)
        return MainScreen()


#Register classes
#==============================================================================
Factory.register("SpriteDemo", SpriteDemo)


#Entry Point
#==============================================================================
KvCheetahApp().run()