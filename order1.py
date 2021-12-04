def find_min(s1, s2):
    if s1 < s2:
        return s1
    return s2

def sort(words):
    sorted = []
    j = 0
    oglen = len(words)          # store original length bc length will change
    while j < oglen:            # iterate until through the whole list
        min = words[0]          # initialize min as first item in list
        for i in range(0, len(words)):  # iterate over the items
            min = find_min(min, words[i])   # compare each two items
        words.remove(min)       # remove the min from original list to avoid repeats
        sorted.append(min)      # add the min to the new list
        j +=1                   # increase for countdown on while loop
    return sorted
        
         


    