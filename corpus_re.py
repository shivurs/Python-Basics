import re

def tokenize(text):
    text = text.lower()
    tokens_list = re.findall("[\w']+", text)
    return tokens_list
