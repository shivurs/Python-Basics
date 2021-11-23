i = 0
j = 1
k = 0
print('Hello')
while i < 10: 
    print('i = ' + str(i) + ', ' + str(j) + ', ' + str(k))
    i += 1
    j *= 2
    k = i % 3
print('Goodbye')