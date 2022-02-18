from spacy.lang.en import English

nlp = English()
nlp.max_length = 2500000

def tokenize(text):
    text = 'sos ' + text
    text = text.lower()
    doc = nlp(text, disable=['ner', 'parser'])
    token_list = []
    for token in doc:
        token_list.append(token.text)
    return token_list

def detokenize(tokens):
    sequence = ''
    for token in tokens:
        sequence += token + ' '
    prettier = make_prettier(sequence)
    return prettier

def make_prettier(sequence):
    sequence = sequence.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?').replace(' ;', ';').replace(' :', ':')
    sequence = sequence.capitalize()
    sequence = sequence.replace(' i ', ' I ')
    return sequence
