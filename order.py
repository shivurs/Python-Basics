def find_min(s1, s2):   #find the minimum value
    if s1 < s2:
        return s1
    return s2

def sort(lst):
    l_len = len(lst)    #store the length of the list
    j = 1               #start counting at 1
    while j < (l_len**2):#keep looping while count is less than the square of the length
        k = 1           #start index k at 1
        for i in range(0, l_len):   
            if k < l_len:           #if k is less than the length of the list
                min = find_min(lst[i], lst[k])  #find the minimum between items at indeces i and k
                if min != lst[i]:   #if the min is not the item at index i
                    lst[k] = lst[i] #update item at index k to be index i
                    lst[i] = min    #update item at index i to be the minimum
            k +=1
        j += 1
    #return lst         #sort in place (no return statement)
