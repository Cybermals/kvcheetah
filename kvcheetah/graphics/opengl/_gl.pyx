"""kvcheetah - Low-Level OpenGL Wrapper API"""

cdef extern:
    ctypedef unsigned int GLenum
    ctypedef int GLsizei
    ctypedef void (*glDrawArraysInstanced)(GLenum mode, int first, GLsizei count, 
        GLsizei primcount)

cdef extern:
    cdef void *SDL_GL_GetProcAddress(const char *proc)


print(<int>SDL_GL_GetProcAddress("glDrawArraysInstanced"))