import lm
import corpus

text = """I am a boy. 
I am a girl.
"""
text2 = 'I like dogs.'

tokens = corpus.tokenize(text)
tokens2 = corpus.tokenize(text2)
lang = lm.LanguageModel(2)
lang.train(tokens + tokens2)

# print(lang.token_list)
print(lang.gram_list)
print(lang.gram_next_merge_end)
#print(lang.p_next())
