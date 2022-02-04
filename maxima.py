def find_maxima(lst):
    newlst = []
    newlst.append(lst[0])
    for i in range(1, len(lst)):
        if lst[i] > newlst[-1]:
            newlst.append(lst[i])
    return newlst
