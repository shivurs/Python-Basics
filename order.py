def find_min(s1, s2):
    if s1 < s2:
        return s1
    return s2

def sort(lst):
    l_len = len(lst)
    j = 1
    while j < (l_len**2):
        k = 1   
        for i in range(0, l_len):
            if k < l_len:
                min = find_min(lst[i], lst[k])
                if min != lst[i]:
                    lst[k] = lst[i]
                    lst[i] = min
            k +=1
        j += 1
    #return lst
