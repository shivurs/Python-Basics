import re

def normalize(word):
    word = word.lower()                 # make lowercase
    word = re.sub('\d', '0', str(word)) # change all digits to 0
    word = word.replace(' ', '')        # remove white space
    word = re.sub(r'[^\w\s]', '', word) # remove punctuation
    return word

my_word = 'Skittles --- 88'
print(normalize(my_word))

