import corpus
import lm

path = 'C:/Users/siobh/Desktop/Stutt/PCL Project Data/data/shakespeare/test_shakespeare.txt'
file = open(path, 'r')
text = file.read()
file.close()

tokens3 = corpus.tokenize(text)

path2 = 'C:/Users/siobh/Desktop/Stutt/PCL Project Data/data/shakespeare/comedy/asyoulikeit.txt'
file2 = open(path2, 'r')
text2 = file2.read()
file2.close()

tokens4 = corpus.tokenize(text2)

train_path = 'C:/Users/siobh/Desktop/Stutt/PCL Project Data/data/shakespeare/train_shakespeare.txt'
train_file = open(train_path, 'r')
train_text = train_file.read()
train_file.close()

train_tokens = corpus.tokenize(train_text)



lang = lm.LanguageModel(3)
lang.train(train_tokens)

beam = lang.beam_generate()
print(beam)
print(lang.get_test_perplexity(beam)) 

