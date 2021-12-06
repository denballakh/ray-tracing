cdef class Point:
    cdef readonly double x, y
    cdef double _abs, _angle
    cdef Point _norm

    cpdef unicode str(self)
    cpdef unicode repr(self)
    cpdef int hash(self)
    cpdef int bool(self)
    cpdef int eq(self, object other)
    cpdef int ne(self, object other)
    cpdef Point neg(self)
    cpdef Point add(self, Point other)
    cpdef Point sub(self, Point other)
    cpdef Point div(self, double factor)
    cpdef Point mul(self, double factor)
    cpdef double scalar(self, Point other)
    cpdef double abs(self)
    cpdef double angle(self)
    cpdef Point norm(self)
    cpdef double angle_to(self, Point other)
    cpdef Point rotate(self, double angle)
    cpdef double dist(self, Point other)
