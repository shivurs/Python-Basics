def find_opposites(lst):
    result = []
    for word in lst:
        check = word[::-1]
        if check in lst and check != word:
            result.append((word, check))
            lst.remove(check)
    return result

print(find_opposites([ "according", "deer", "net", "ten", "reed", "refer",
"raw", "war", "addition", "frequency", "platform" ]))