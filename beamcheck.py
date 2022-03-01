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

print(lang.gram_next)
#print(lang.p_next([]))
# generate = lang.greedy_generate()
# print(generate)
