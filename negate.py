def negate(l):
    head = l[0]
    tail = l[1:]
    if len(tail) == 0:
        return [-head]
    else:
        return [-head] + negate(tail)

print(negate([1, 2, -3, 4, -5]))
