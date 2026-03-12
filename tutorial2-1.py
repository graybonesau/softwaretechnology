# Definition of a Simple Vector Class
class Vector:
    #"""Represent a vector in a multidimensional space."""

    def __init__(self, d):
        """Create a Vector.
        If d is an int, create a d-dimensional zero vector.
        If d is an iterable, create a vector with coordinates from it.
        """
        if isinstance(d, int):
            if d < 0:
                raise ValueError('dimension must be non-negative')
            self._coords = [0] * d
        else:
            try:
                data = list(d)
            except TypeError:
                raise TypeError('Vector constructor expects int or iterable')
            self._coords = [x for x in data]

    def __len__(self):
        #"""Return dimension of the vector."""
        return len(self._coords)

    def __getitem__(self, j):
        #"""Return jth coordinate of vector."""
        return self._coords[j]

    def __setitem__(self, j, val):
        #"""Set jth coordinate of vector to given value."""
        self._coords[j] = val

    def __add__(self, other):
        #"""Return sum of two vectors."""
        if len(self) != len(other):          # relies on len method
            raise ValueError('dimensions must agree')
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result        # start with vector of zeros

    def __eq__(self, other):
        #"""Return True if vector has same coordinates as other."""
        return self._coords == other._coords

    def __ne__(self, other):
        #"""Return True if vector differs from other."""
        return not self == other        # rely on existing __eq__ definition

    def __sub__(self, other):
        #"""Return difference of two vectors."""
        if len(self) != len(other):
            raise ValueError('dimensions must agree')
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] - other[j]
        return result

    def __neg__(self):
        #"""Return a new Vector that is the negation of this vector."""
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = -self[j]
        return result

    def __str__(self):
        #"""Readable string representation, used by print() and str()."""
        return '<' + ', '.join(str(x) for x in self._coords) + '>'

    def __mul__(self, other):
        """If other is a Vector, return the dot product (a scalar).
        Otherwise attempt scalar multiplication and return a new scaled Vector.
        If the operation is not supported, return NotImplemented.
        """
        # Vector dot product
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('dimensions must agree')
            total = 0
            for j in range(len(self)):
                total += self[j] * other[j]
            return total

        # Scalar multiplication
        try:
            result = Vector(len(self))
            for j in range(len(self)):
                result[j] = self[j] * other
            return result
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        # support scalar * v by delegating to __mul__
        return self.__mul__(other)

    @classmethod
    def from_list(cls, data):
        #"""Create a Vector from an iterable of numbers."""
        v = cls(len(data))
        for i, val in enumerate(data):
            v[i] = val
        return v

v = Vector.from_list([5, 2, -1])    # creates <5, 2, -1>
w = Vector.from_list([1, 1, 1])
print(v)                             # <5, 2, -1>
print(v + w)                         # <6, 3, 0>
print(v - w)                         # <4, 1, -2>
print(-v)                            # <-5, -2, 1>
print(v * 3)                         # <15, 6, -3>
print(2 * w)                         # <2, 2, 2>
print(v * w)                         # 5*1 + 2*1 + (-1)*1 == 6
print(Vector(3))                     # <0, 0, 0>
print(Vector([1,2,3]))               # <1, 2, 3>