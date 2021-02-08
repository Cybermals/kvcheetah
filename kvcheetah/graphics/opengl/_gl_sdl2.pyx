"""kvcheetah - OpenGL SDL Backend API"""

#SDL OpenGL Definitions
cdef extern:
    cdef void *SDL_GL_GetProcAddress(const char *proc) nogil

from libc.string cimport strcpy, strcat
from ._gl cimport *
from . cimport _gl


#Functions
#===============================================================================
def init():
    """Initialize this OpenGL backend."""
    #Import OpenGL functions
    _gl.glDrawArraysInstanced = <GLDRAWARRAYSINSTANCEDPROC>get_gl_func(
        "glDrawArraysInstanced")


cdef void *get_gl_func(const char *proc) except *:
    """Get a pointer to an OpenGL function and handle any errors that occur."""
    #Try to get the core version of the function
    cdef char name_buf[256]
    cdef void *gl_proc = SDL_GL_GetProcAddress(proc)

    if gl_proc is NULL:
        #Try to get the ARB version of the function
        strcpy(name_buf, proc)
        strcat(name_buf, "ARB")
        gl_proc = SDL_GL_GetProcAddress(name_buf)

        if gl_proc is NULL:
            #Try to get the EXT version of the function
            strcpy(name_buf, proc)
            strcat(name_buf, "EXT")
            gl_proc = SDL_GL_GetProcAddress(name_buf)

            if gl_proc is NULL:
                #Report the exception
                raise ImportError(
                    "GL: Failed to import OpenGL function '{}'.".format(
                        proc.decode("utf-8")))

    return gl_proc
