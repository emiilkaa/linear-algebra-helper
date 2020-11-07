import functools
from sys import stdin


class Matrix:
    def __init__(self, array):
        self.array = [row.copy() for row in array]

    def __str__(self):
        rows = ['\t'.join(map(str, x)) for x in self.array]
        return '\n'.join(rows)

    def size(self):
        return len(self.array), len(self.array[0])

    def __add__(self, m):
        if self.size() != m.size():
            raise Exception('The matrices are of different sizes.')
        s = [[sum(el) for el in zip(*row)] for row in zip(self.array, m.array)]
        return Matrix(s)

    def __sub__(self, m):
        return self + (-1 * m)

    def __mul__(self, a):
        if isinstance(a, int) or isinstance(a, float):
            new = [list(map(lambda x: a * x, row)) for row in self.array]
            return Matrix(new)
        elif isinstance(a, Matrix):
            if self.size()[1] != a.size()[0]:
                raise Exception('These matrices cannot be multiplied.')
            prod = [[functools.reduce(
                lambda x, y: x + y[0] * y[1], zip(row, column), 0)
                for column in list(zip(*a.array))] for row in self.array]
            return Matrix(prod)

    __rmul__ = __mul__

    def transpose(self):
        self.array = [list(column) for column in zip(*self.array)]
        return Matrix(self.array)

    def solve(self, vector):
        if len(self.array) != len(vector):
            raise Exception('The number of left and right sides of the equations is different.')
        var = self.size()[1]
        eq = list(map(list, zip(self.array, vector)))
        eq.sort(key=lambda x: list(map(abs, x[0])), reverse=True)
        while eq and not any(eq[-1][0]):
            if eq[-1][1] != 0:
                raise Exception('This system of linear equations has no solutions.')
            eq.pop()
        if not eq:
            raise Exception('This system of linear equations has infinitely many solutions.')
        n = 0
        for i in range(var):
            if n >= len(eq):
                break
            if eq[n][0][i] == 0:
                for k in range(n + 1, len(eq)):
                    if eq[k][0][i] != 0:
                        eq[n], eq[k] = eq[k], eq[n]
                        break
                if eq[n][0][i] == 0:
                    continue
            for j in range(n + 1, len(eq)):
                c = -eq[j][0][i] / eq[n][0][i]
                for k in range(var):
                    eq[j][0][k] += eq[n][0][k] * c
                eq[j][1] += eq[n][1] * c
            n += 1
        while eq and not any(eq[-1][0]):
            if eq[-1][1] != 0:
                raise Exception('This system of linear equations has no solutions.')
            eq.pop()
        if len(eq) < var:
            raise Exception('This system of linear equations has infinitely many solutions.')
        for i in range(len(eq)):
            k = 0
            while eq[i][0][k] == 0:
                k += 1
            c = eq[i][0][k]
            eq[i][0] = list(map(lambda x: x / c, eq[i][0]))
            eq[i][1] /= c
        solution = [0] * var
        solution[-1] = eq[-1][1]
        for i in range(-2, -var - 1, -1):
            solution[i] = eq[i][1] - functools.reduce(
                lambda x, y: x + y[0] * y[1],
                zip(solution, eq[i][0]),
                0
            )
        return solution


def transposed(m):
    return Matrix([list(column) for column in zip(*m.array)])


class SquareMatrix(Matrix):
    def __init__(self, array):
        if len(array) != len(array[0]):
            raise Exception('This matrix is not square.')
        self.array = [row.copy() for row in array]

    def __pow__(self, n):
        if n == 0:
            s = len(self.array)
            new = [[0] * s for i in range(s)]
            for i in range(s):
                new[i][i] = 1
            return SquareMatrix(new)
        if n % 2 != 0:
            return self ** (n - 1) * self
        else:
            p = self ** (n // 2)
            return p * p


if __name__ == '__main__':
    exec(stdin.read())
