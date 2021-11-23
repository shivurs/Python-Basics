n = int(input())

for i in range(n*3):
    if i < n or i > ((2 * n) - 1):
        print((' ' * n) + ('#' * n))
    else:
        print('#'*(n*3))