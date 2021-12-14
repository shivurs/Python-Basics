def word2dict(word):
    word = word.lower()             # lower to handle uppercase letters
    word_dict = {}                  # empy dictionary for result
    for lttr in word:               # iterate over the letters in the word
        if lttr in word_dict:       # if the letter matches a key in the result dict
            word_dict[lttr] += 1    # add one to the value
        else:                       # if it's not in the result dict
            word_dict[lttr] = 1     # add letter to dict with 1 as starting value
    return word_dict                # return the result dict

def can_be_composed(word1, word2):
    result = False                  # default result is False
    dict1 = word2dict(word1)        # dict of letters and frequency of word1
    dict2 = word2dict(word2)        # dict of letters and frequency of word2
    for (k, v) in dict1.items():    # iterate over key-value tuples in dict1
        if  (k, v) in dict2.items() and dict1[k] <= dict2[k]: # if dict1's tuple is in dict2
            result = True           # the result updates to True
        elif k in dict2 and dict1[k] <= dict2[k]:   # if dict1's key is in dict2 & dict1's val is <= dict2's val
             result = True          # the result updates to True
        else:                       # if neither above are True
            result = False          # the result is False
            break                   # break the loop if one False result
    return result