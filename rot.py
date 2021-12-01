def shift(lst,k):   
    i = lst[0:k]    #store list slice to move
    j = lst[k:]     #store rest of list in slice
    lst_new = j + i #attach moved slice to end of rest slice
    return lst_new

def rotated(lst, n):
    if len(lst) > 0:    
        num = n % len(lst)
        lst_new = shift(lst, num)
        return lst_new
    return lst
