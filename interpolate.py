def interpolate(l):
    i = 0
    while i < (len(l) - 1):
        avg = (int(l[i]) + int(l[i+1]))/2
        l.insert(i+1, avg)
        i += 2
    return l

print(interpolate([1, 2, 3, 2, 1]))