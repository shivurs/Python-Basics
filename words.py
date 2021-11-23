wordlist = [] 
while True:
    print('Enter a word')       # ask user for word
    word = input()              # take input (always string unless modified) 
    if word != 'done':          # check for 'done' to quit asking for words
        wordlist.append(word)   # if not 'done' add word to wordlist
    else:                       # if 'done'
        wordlist.sort()         # sort wordlist
        print(str(wordlist[0]) + ' comes first in the dictionary')  # print first word
        print(str(wordlist[-1]) + ' comes last in the dictionary')  # print last word
        break                   # exit loop, finish program
