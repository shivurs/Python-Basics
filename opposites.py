def find_opposites(lst):
    result = []
    new_set = set()
    for word in lst:
        new_set.add(word)
    for word in lst:
        check = word[::-1]
        if check in new_set and check != word:
            result.append((word, check))
            lst.remove(check)
    return result
