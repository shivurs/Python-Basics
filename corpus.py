from nltk.tokenize import word_tokenize

def tokenize(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return tokens

def detokenize(tokens):
    sequence = ''
    for token in tokens:
        sequence += token + ' '
    prettier = make_prettier(sequence)
    return prettier

def make_prettier(sequence):
    sequence = sequence.replace(' .', '.').replace(' ,', ',')
    sequence = sequence.capitalize()
    sequence = sequence.replace(' i ', ' I ')
    return sequence
