import lm
import corpus

text = """I am a boy. 
I was a girl.
"""

tokens = corpus.tokenize(text)
lang = lm.LanguageModel(2)
lang.train(tokens)

generate = lang.greedy_generate()
print(generate)
