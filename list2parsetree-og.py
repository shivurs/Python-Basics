from constituents import *

def list2parsetree(l):
    checked = ''                            # empty string to store checked tokens
    for item in l[1:]:                      # check after the head
        if type(item[1]) != list:           # if the second ele is not a list
            token = Token(item[0], item[1]) # turn the ele into a Token object
            checked += str(token)           # add it to checked string
        else:                               # if the second ele is a list, that means it's a phrase
            phrase = list2parsetree(item)   # find the tokens again (ignore the head)
            checked += str(phrase)          # add those to the checked string
    final = Phrase(l[0], [checked])         # when it pops back out it adds the head
    return final