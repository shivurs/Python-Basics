def last(list):
    return list[-1]

def middle(list):
    return list[(len(list)//2)]

def product(list):
    product = 1
    for i in range(len(list)):
        product = product * list[i]
    return product

def mean(list):
    sum = 0
    for i in range(len(list)):
        sum = sum + list[i]
    return sum/len(list)

def even_sum(list):
    sum = 0
    for i in range(len(list)):
        if i % 2 == 0:
            sum = sum + list[i]
    return sum

