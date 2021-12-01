import re, string

badgoodlow = {                             #dictionary of words to be replaced and their replacements
    'bad': 'good', 
    'horrible': 'fantastic', 
    'dirty': 'clean', 
    'disgusting': 'sublime', 
    'expensive': 'affordable', 
    'moldy': 'flavourful', 
    'frozen': 'farm-fresh'
}

badgoodup = {                             #dictionary of words to be replaced and their replacements
    'Bad': 'Good', 
    'Horrible': 'Fantastic', 
    'Dirty': 'Clean', 
    'Disgusting': 'Sublime', 
    'Expensive': 'Affordable', 
    'Moldy': 'Flavourful', 
    'Frozen': 'Farm-fresh'
}

def halve_minutes(review):
    review_list = review.split()
    i = 0
    while i < len(review_list):
        check = review_list[i]
        if i < (len(review_list) - 1):
            next = review_list[i + 1]
        else:
            break
        if check.isdigit() == True and next == 'minutes':   
            review_list[i] = str((int(review_list[i]) // 2))
            review_list.insert(i, 'only')
            i += 1
        i += 1
    review = ' '.join(review_list)
    return review

def positivize(review):
    review = str(review)
    i = 0
    while i < len(review):              #keep iterating over the string
        word = ''                       #start with empty string
        for lttr in review[i:]:         #check each character
            if lttr == ' ' or lttr in string.punctuation:   #do not add to 'word' if char is a space or punctuation
                i += 1                  #add one to the index marker to prevent infinite loop
                break                   #leave loop
            word = word + lttr          #concat char onto 'word'
            i += 1                      #add one to the index marker        
        if word in badgoodlow:          #check if 'word' in dictionary
            review = review.replace(word, badgoodlow.get(word))    #if so, replace it with value in dictionary
            word = ''                   #update 'word' to be empty agagin
            continue                    #loop again
        if word in badgoodup:           #check if 'word' in dictionary
            review = review.replace(word, badgoodup.get(word))    #if so, replace it with value in dictionary
            word = ''                   #update 'word' to be empty agagin
            continue                    #loop again
    review = halve_minutes(review)     
    return review                       #return the whole 'review' string