"""kvcheetah - Matrix API"""

from math import cos, radians, sin, tan

from .vector import Vec4


#Classes
#==============================================================================
cdef class Mat4(object):
    """A 4x4 matrix."""
    cdef float data[16]

    @staticmethod
    def identity():
        """Return a 4x4 identity matrix."""
        m = Mat4()

        for i in range(4):
            m[i, i] = 1

        return m

    @staticmethod
    def translate(x, y, z):
        """Return a 4x4 translation matrix."""
        m = Mat4.identity()
        m[3, 0] = x
        m[3, 1] = y
        m[3, 2] = z
        return m

    @staticmethod
    def rotate(x, y, z):
        """Return a 4x4 rotation matrix."""
        #Build the rotation matrix for the X axis.
        mx = Mat4.identity()
        theta = radians(x)
        mx[1, 1] = cos(theta)
        mx[2, 1] = -sin(theta)
        mx[1, 2] = sin(theta)
        mx[2, 2] = cos(theta)

        #Build the rotation matrix for the Y axis.
        my = Mat4.identity()
        theta = radians(y)
        my[0, 0] = cos(theta)
        my[2, 0] = sin(theta)
        my[0, 2] = -sin(theta)
        my[2, 2] = cos(theta)

        #Build the rotation matrix for the Z axis.
        mz = Mat4.identity()
        theta = radians(z)
        mz[0, 0] = cos(theta)
        mz[1, 0] = -sin(theta)
        mz[0, 1] = sin(theta)
        mz[1, 1] = cos(theta)

        #Return the final rotation matrix
        return mz * my * mx

    @staticmethod
    def scale(x, y, z):
        """Return a 4x4 scaling matrix."""
        m = Mat4.identity()
        m[0, 0] = x
        m[1, 1] = y
        m[2, 2] = z
        return m

    @staticmethod
    def ortho(left, right, top, bottom, near, far):
        """Return a 4x4 orthographic projection matrix."""
        m = Mat4()
        m[0, 0] = 2 / (right - left)
        m[3, 0] = -(right + left) / (right - left)
        m[1, 1] = 2 / (top - bottom)
        m[3, 1] = -(top + bottom) / (top - bottom)
        m[2, 2] = -2 / (far - near)
        m[3, 2] = -(far + near) / (far - near)
        m[3, 3] = 1
        return m

    @staticmethod
    def perspective(fov, aspect, near, far):
        """Return a 4x4 perspective projection matrix."""
        m = Mat4()
        f = 1 / tan(radians(fov / 2))
        m[0, 0] = f / aspect
        m[1, 1] = f
        m[2, 2] = (far + near) / (near - far)
        m[3, 2] = (2 * far * near) / (near - far)
        m[2, 3] = -1
        return m

    def __cinit__(self, *args):
        """Setup this matrix."""
        #Init data
        if len(args) == 0:
            for i in range(16):
                self.data[i] = 0

        #Copy matrix
        elif isinstance(args[0], Mat4):
            m = args[0]

            for i in range(4):
                self.data[i] = m.data[i]

        #Copy data
        else:
            m = args[0]

            for y in range(4):
                for x in range(4):
                    self[x, y] = m[y][x]

    def __getitem__(self, i):
        """Get an element of this matrix."""
        x, y = i
        return self.data[x * 4 + y]

    def __setitem__(self, i, value):
        """Set an element of this matrix."""
        x, y = i
        self.data[x * 4 + y] = value

    def __str__(self):
        """Return the string representation of this matrix."""
        return "Mat4([\n\t[{}, {}, {}, {}],\n\t[{}, {}, {}, {}],\n\t[{}, {}, {}, {}],\n\t[{}, {}, {}, {}]\n])".format(
            self[0, 0], self[1, 0], self[2, 0], self[3, 0],
            self[0, 1], self[1, 1], self[2, 1], self[3, 1],
            self[0, 2], self[1, 2], self[2, 2], self[3, 2],
            self[0, 3], self[1, 3], self[2, 3], self[3, 3])

    def __repr__(self):
        """Return the representation of this matrix."""
        return str(self)

    def __mul__(self, b):
        """Multiply this matrix with another matrix or a vector."""
        #Multiply 2 matrices
        if isinstance(b, Mat4):
            res = Mat4()

            for y in range(4):
                for x in range(4):
                    for i in range(4):
                        res[x, y] += self[i, y] * b[x, i]

            return res

        #Multiply a matrix and a vector
        elif isinstance(b, Vec4):
            res = Vec4()
            res.x = self[0, 0] * b.x + self[1, 0] * b.y + self[2, 0] * b.z + self[3, 0] * b.w
            res.y = self[0, 1] * b.x + self[1, 1] * b.y + self[2, 1] * b.z + self[3, 1] * b.w
            res.z = self[0, 2] * b.x + self[1, 2] * b.y + self[2, 2] * b.z + self[3, 2] * b.w
            res.w = self[0, 3] * b.x + self[1, 3] * b.y + self[2, 3] * b.z + self[3, 3] * b.w
            return res
