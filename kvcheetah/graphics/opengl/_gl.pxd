#OpenGL Definitions
#Types
ctypedef unsigned int GLenum
ctypedef int GLsizei

#Function Types
ctypedef void (__stdcall *GLDRAWARRAYSINSTANCEDPROC)(GLenum mode, int first, 
    GLsizei count, GLsizei primcount) nogil

#Functions
cdef GLDRAWARRAYSINSTANCEDPROC glDrawArraysInstanced
