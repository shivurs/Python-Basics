import corpus
import lm

path = 'C:/Users/siobh/Desktop/Stutt/PCL Project Data/data/shakespeare/test_shakespeare.txt'
file = open(path, 'r')
test_text = file.read()
file.close()

tokens3 = corpus.tokenize(test_text)

train_path = 'C:/Users/siobh/Desktop/Stutt/PCL Project Data/data/shakespeare/train_shakespeare.txt'
train_file = open(train_path, 'r')
train_text = train_file.read()
train_file.close()

train_tokens = corpus.tokenize(train_text)



lang = lm.LanguageModel(3)
lang.train(train_tokens)

print(lang.get_test_perplexity(test_text)) 

