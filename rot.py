def rotated(lst, n):    #take list and integer as input
    if n >= 1:          #positive number = shift to right end of list
        i = lst[0:n]    #store list slice
        del lst[0:n]    #delete that slice from original list
        lst = lst + i   #attach slice to end
    elif n < 1:         #negative number = shift to left end of list
        newn = len(lst) + n #to make the correct index
        i = lst[0:newn] #same process as above
        del lst[0:newn]
        lst = lst + i
    return lst
