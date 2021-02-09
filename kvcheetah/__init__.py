"""kvcheetah

A lightweight game engine based on Kivy.
"""

#Globals
#==============================================================================
__author__ = "Eric Snyder"
__copyright__ = "Copyright (c) 2021 by Eric Snyder"
__license__ = "MIT"
__version__ = "2.0.1"


#Make sure widget classes get imported and initialized
#==============================================================================
try:
    from .uix import joystick

except ImportError:
    from uix import joystick
