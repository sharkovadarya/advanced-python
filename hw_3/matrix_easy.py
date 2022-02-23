import numbers


class Matrix:
    def __init__(self, *args):
        if len(args) == 1:
            values = args[0]
            if not isinstance(values, list) or \
                    not (len(values) == 0 or
                         (isinstance(values[0], list) and
                          all(map(lambda el : isinstance(el, numbers.Number), values[0])))):
                raise ValueError("Matrix values should be a two-dimensional array of numbers.")
            self._values = values
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self._values = [[0 for _ in range(args[1])] for _ in range(args[0])]
        else:
            raise ValueError("Cannot initialize matrix. Valid arguments: "
                             "a two-dimensional numeric array or two integer numbers, row and column sizes")

    @property
    def values(self):
        return self._values

    def rows_size(self):
        return len(self._values)

    def columns_size(self):
        return 0 if self.rows_size() == 0 else len(self._values[0])

    def __getitem__(self, item):
        if isinstance(item, int) and item < self.rows_size():
            return self.values[item]
        raise ValueError(f"Can't access row {item}")

    def __add__(self, other):
        if (not (isinstance(other, Matrix))) or \
                not (other.rows_size() == self.rows_size() and other.columns_size() == self.columns_size()):
            raise ValueError("Can't add two matrices of different dimensions")
        new_matrix = Matrix(self.rows_size(), self.columns_size())
        for i in range(other.rows_size()):
            for j in range(other.columns_size()):
                new_matrix[i][j] = self.values[i][j] + other.values[i][j]
        return new_matrix

    def __mul__(self, other):
        if (not (isinstance(other, Matrix))) or \
                not (other.rows_size() == self.rows_size() and other.columns_size() == self.columns_size()):
            raise ValueError("Can't multiply (element-wise) two matrices of different dimensions")
        new_matrix = Matrix(self.rows_size(), self.columns_size())
        for i in range(other.rows_size()):
            for j in range(other.columns_size()):
                new_matrix[i][j] = self.values[i][j] * other.values[i][j]
        return new_matrix

    def __matmul__(self, other):
        if (not (isinstance(other, Matrix))) or not (other.columns_size() == self.rows_size()):
            raise ValueError("Can't multiply two matrices of incorrect dimensions")
        new_matrix = Matrix(self.rows_size(), other.columns_size())
        for i in range(self.rows_size()):
            for j in range(other.columns_size()):
                for k in range(other.rows_size()):
                    new_matrix[i][j] += self.values[i][k] * other.values[k][j]
        return new_matrix
