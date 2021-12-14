def most_common(dict):
    tag = ''
    most = max(dict.values())   #find max value
    for k, v in dict.items():   #iterate over key-val pairs
        if most == v:           #if max value and val match
            tag = k             #tag is the key for that pair
    return tag                  #return the key of the max value

def lowerlst(lst):
    for i in range(len(lst)):
        lst[i] = lst[i].lower()
    return lst

def clean(line):
    if line == '\n':            #if it's only a new line, 
        return None             #return None
    first = line.split('_')     #split the line by underscores    
    first[0] = first[0].strip() #strip the first element by tabs/spaces
    second = first[0].split('\t') #split the first element by tabs
    first[1] = first[1].strip() #strip the second element by tabs/spaces
    result = (second[-1], first[1]) #create a tuple of the word and the POS tag
    return result               #return the tuple

def read_conllu(filepath):
    f = open(filepath, 'r')
    poslst = []                 #start with an empty list
    for line in f.readlines():  #look at each line of the file
        tup = clean(line)       #get the word-POS tuples
        if tup  == None:        #skip the new line chars
            continue
        poslst.append(tup)      #add the tuple to the list
    f.close()                   
    return poslst               #return the list of tuples

def train_and_tag(train_file, test_words):
    tuplst = read_conllu(train_file)
    test_words = lowerlst(test_words)
    result = []
    for word in test_words:
        is_in = False
        for item in tuplst:
            if word in item:
                result.append(item[1])
                is_in = True
                break
        if is_in == False:
            result.append("UNK")
    return result
