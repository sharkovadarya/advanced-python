def fib(n):
    if n == 0:
        return [0]
    if n == 1:
        return [0, 1]
    p = fib(n - 1)
    p.append(p[-2] + p[-1])
    return p