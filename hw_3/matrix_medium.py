import numbers

import numpy as np


class WriteableToFileMixin:
    def write_to_file(self, f):
        f.write(str(self))


class TwoDimensionalArrayStrMixin:
    def __str__(self):
        return "\n".join([" ".join(map(lambda i: str(i), row)) for row in self._values])


class ValuePropertyMixin:
    @property
    def values(self):
        return self._values.tolist()

    @values.setter
    def values(self, values):
        self._values = np.asarray(values)


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, WriteableToFileMixin, TwoDimensionalArrayStrMixin, ValuePropertyMixin):
    def __init__(self, *args):
        if len(args) == 1:
            values = args[0]
            if isinstance(values, np.ndarray):
                self._values = values
            elif not isinstance(values, list) or \
                    not (len(values) == 0 or
                         (isinstance(values[0], list) and
                          all(map(lambda el: isinstance(el, numbers.Number), values[0])))):
                raise ValueError("Matrix values should be a two-dimensional array of numbers.")
            self._values = np.asarray(values)
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self._values = np.asarray([[0 for _ in range(args[1])] for _ in range(args[0])])
        else:
            raise ValueError("Cannot initialize matrix. Valid arguments: "
                             "a two-dimensional numeric array or two integer numbers, row and column sizes")

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if any(map(lambda m: not isinstance(m, Matrix), inputs)):
            return NotImplemented

        inputs = tuple(x._values for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return type(self)(result)

    def __getitem__(self, item):
        return self._values[item]
