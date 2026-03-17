class Vector:
    def __init__(self, d):
        if isinstance(d, int):
            if d < 0:
                raise ValueError('Dimension must be non-negative.')
            self._coords = [0] * d
        else:
            try:
                data = list(d)
            except TypeError:
                raise TypeError('Vector constructor expects int or iterable.')
            self._coords = [x for x in data]

    def __len__(self):
        return len(self._coords)

    def __getitem__(self, j):
        return self._coords[j]

    def __setitem__(self, j, val):
        self._coords[j] = val

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError('Dimensions must agree.')
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result

    def __eq__(self, other):
        return self._coords == other._coords

    def __ne__(self, other):
        return not self == other

    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError('Dimensions must agree.')
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] - other[j]
        return result

    def __neg__(self):
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = -self[j]
        return result

    def __str__(self):
        return '<' + ', '.join(str(x) for x in self._coords) + '>'

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('Dimensions must agree.')
            total = 0
            for j in range(len(self)):
                total += self[j] * other[j]
            return total

        try:
            result = Vector(len(self))
            for j in range(len(self)):
                result[j] = self[j] * other
            return result
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    @classmethod
    def from_list(cls, data):
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