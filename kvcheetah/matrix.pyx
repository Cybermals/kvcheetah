"""kvcheetah - Matrix API"""


#Classes
#==============================================================================
cdef class Mat4(object):
    """A 4x4 matrix."""
    cdef float data[16]

    def __cinit__(self, *args):
        """Setup this matrix."""
        #Init data
        for i in range(16):
            self.data[i] = 0

        #TODO: Allow initialization from list, matrix, etc.

    def __getitem__(self, i):
        """Get an element of this matrix."""
        x, y = i
        return self.data[x * 4 + y]

    def __setitem__(self, i, value):
        """Set an element of this matrix."""
        x, y = i
        self.data[x * 4 + y] = value
