def find_message(txt, words_filename):
    hidden = open(txt, 'r')
    msg = hidden.read()
    msg = msg.lower()
    msg = msg.replace('.', '').replace(',', '').replace('"', '').replace('!', '').replace('\n', ' ')
    txt_words = msg.split()
    hidden.close()

    file = open(words_filename, 'r')
    file_words = []
    for word in file:
        word = word.strip()
        file_words.append(word)
    file_words = set(file_words)
    file.close()
    
    check = ''
    for idx in range(len(txt_words)):
        check += txt_words[idx][0]

    candidates = []
    for word in file_words:
        if check.find(word) != -1:
            candidates.append(word)
    
    best = ''
    for idx in range(len(candidates)):
        if len(candidates[idx]) > len(best):
            best = candidates[idx]
    return best
