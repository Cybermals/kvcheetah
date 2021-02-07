"""kvcheetah

A lightweight game engine based on Kivy.
"""

#Globals
#==============================================================================
__author__ = "Eric Snyder"
__copyright__ = "Copyright (c) 2021 by Eric Snyder"
__license__ = "MIT"
__version__ = "1.4.0"


#Make sure widget classes get imported and initialized
#==============================================================================
try:
    from . import joystick

except ImportError:
    import joystick
