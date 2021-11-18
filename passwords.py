from fragments import get_random_text

def easy_password(length):              # length of the password is the argument
    pwd = ''                            # password starts as empty string
    tries = []                          # the chunks of random text are stored in a list
    while len(pwd) < length:            # while the password is shorter than the desired length
        chunk = get_random_text()       # get a chunk of random text from fragments.py
        tries.append(chunk)             # add that chunk to the list of tries
        pwd = pwd + chunk               # add that same chunk to the password string
        if len(pwd) == length:          # if the length of the password matches the desired length
            break                       # finish (exit the loop and return the password)
        elif len(pwd) == length - 1:    # to avoid infinite loop
            pwd = pwd[:-len(tries[-1] + tries[-2])] # remove last two tries
        elif len(pwd) > length:         # if the password is greater than the desired length
            pwd = pwd[:-len(tries[-1])]  # update the password by removing the latest tried chunk
    return pwd

