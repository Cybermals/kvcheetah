"""kvcheetah - Vector API"""


#Classes
#================================================================================================
cdef class Vec4(object):
    """A 4-component vector."""
    cdef float data[4]

    def __cinit__(self, *args):
        """Setup this vector."""
        #Init data
        if len(args) == 0:
            for i in range(4):
                self.data[i] = 0

        #Copy data
        elif len(args) == 4:
            self.x, self.y, self.z, self.w = args

        #Copy data
        else:
            v = args[0]

            for i in range(4):
                self[i] = v[i]

    def __getitem__(self, i):
        """Get an element of this vector."""
        return self.data[i]

    def __setitem__(self, i, value):
        """Set an element of this vector."""
        self.data[i] = value

    def __str__(self):
        """Return the string representation of this vector."""
        return "Vec4([{}, {}, {}, {}])".format(self.x, self.y, self.z, self.w)

    def __repr__(self):
        """Return the representation of this vector."""
        return str(self)

    def __add__(self, b):
        """Add 2 vectors."""
        v = Vec4()
        v.x = self.x + b.x
        v.y = self.y + b.y
        v.z = self.z + b.z
        v.w = self.w + b.w
        return v

    def __sub__(self, b):
        """Subtract 2 vectors."""
        v = Vec4()
        v.x = self.x - b.x
        v.y = self.y - b.y
        v.z = self.z - b.z
        v.w = self.w - b.w
        return v

    def __mul__(self, b):
        """Multiply 2 vectors."""
        v = Vec4()
        v.x = self.x * b.x
        v.y = self.y * b.y
        v.z = self.z * b.z
        v.w = self.w * b.w
        return v

    def __truediv__(self, b):
        """Divide 2 vectors."""
        v = Vec4()
        v.x = self.x / b.x
        v.y = self.y / b.y
        v.z = self.z / b.z
        v.w = self.w / b.w
        return v

    def get_x(self):
        """Get the X component of this vector."""
        return self.data[0]

    def set_x(self, value):
        """Set the X component of this vector."""
        self.data[0] = value

    x = property(get_x, set_x)

    def get_y(self):
        """Get the Y component of this vector."""
        return self.data[1]

    def set_y(self, value):
        """Set the Y component of this vector."""
        self.data[1] = value

    y = property(get_y, set_y)

    def get_z(self):
        """Get the Z component of this vector."""
        return self.data[2]

    def set_z(self, value):
        """Set the Z component of this vector."""
        self.data[2] = value

    z = property(get_z, set_z)

    def get_w(self):
        """Get the W component of this vector."""
        return self.data[3]

    def set_w(self, value):
        """Set the W component of this vector."""
        self.data[3] = value

    w = property(get_w, set_w)