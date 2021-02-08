"""kvcheetah - Low-Level OpenGL Wrapper API"""


#Globals
#===============================================================================
cdef int is_init = False
cdef GLDRAWARRAYSINSTANCEDPROC glDrawArraysInstanced


#Entry Point
#===============================================================================
#Initialize just once
if not is_init:
    #Try to import the SDL2 backend
    try:
        from ._gl_sdl2 import init
        init()

    except ImportError:
        #Try to import the GLX backend
        from ._gl_glx import init
        init()
