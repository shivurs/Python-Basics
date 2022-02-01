def decipher(msg, perm):
    perm_dict = {}
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    idx = 0
    for idx in range(len(perm)):
        perm_dict[perm[idx]] = alpha[idx]
        idx += 1

    deciphered = ''
    for char in msg:
        if char == ' ':
            deciphered += ' '
        elif char in perm_dict:
            deciphered += perm_dict[char]

    return deciphered
