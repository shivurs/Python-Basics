from big_letters import *

def build_headline(text):
    headline = ''
    charlist = []
    for char in text:
        if char.upper() in letters:
            charlist.append(letters[char.upper()].split('\n'))
    
    for row in range(0, len(charlist[0])):
        for l in charlist:
            headline += l[row]
        headline += '\n'
    return headline