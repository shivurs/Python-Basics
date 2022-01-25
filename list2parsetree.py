from constituents import *

def list2parsetree(l):
    children =  []                      #empty list to store tokens
    for ele in l[1:]:                   #start from second element
        if type(ele[1]) != list:        #if the second item in the element is not a list (bc that's a phrase)
            token = Token(ele[0], ele[1])   #create a token
            children.append(token)      #add the token to the storage list
        else:                           #if the second item is a list, it's a phrase
            inphrase = list2parsetree(ele)  #check for more tokens as before
            children.append(inphrase)   #add new tokens
    phrase = Phrase(l[0], children)     #assemble phrase
    return phrase                       #as it pops back out, it assembles the sentence