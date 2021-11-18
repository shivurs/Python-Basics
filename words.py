wordlist = [] 
while True:
    print('Enter a word')
    word = str(input())
    if word != 'done':
        wordlist.append(word)
    else:
        wordlist.sort()
        print(str(wordlist[0]) + ' comes first in the dictionary')
        print(str(wordlist[-1]) + ' comes last in the dictionary')
        break
