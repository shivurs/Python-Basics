import random
import corpus
import math

class LanguageModel:
    def __init__(self, n):
        self.n = n
        self.token_list = []
        self.token_counts = {}
        self.padded_tokens = []
        self.gram_list = []
        self.gram_counts = {}
        self.start_words = {}

    def train(self, token_sequences): 
        self.token_list = token_sequences
        self.token_counts = self.make_count_dict(token_sequences)
        self.gram_list = self.make_ngrams(token_sequences)
        self.gram_counts = self.make_count_dict(self.gram_list)
        self.padded_tokens = self.add_padding(token_sequences)
        self.start_words = self.set_start_words()
        
    def make_count_dict(self, token_sequence):
        """Return a dictionary of strings and their quantities."""
        count_dict = {}
        for token in token_sequence:
            if token in count_dict:
                count_dict[token] += 1
            else:
                count_dict[token] = 1
        return count_dict

    def add_padding(self, token_sequence):
        """Return a list of strings starting and ending with 'PAD'."""
        padded = []
        pads = self.n
        while pads > 1:
            padded.append('PAD')
            pads -= 1
        padded = padded + token_sequence + padded
        return padded

    def make_ngrams(self, token_sequence):
        """Return a list of tuples (of strings) of length n from the text."""
        padded_list = self.add_padding(token_sequence)
        for idx1 in range(len(padded_list) - int(self.n) + 1):
            start_gram = []
            for idx2 in range(int(self.n)):
                start_gram.append(padded_list[idx1 + idx2])
            end_gram = tuple(start_gram)
            self.gram_list.append(end_gram)
        return self.gram_list
        
    def find_next(self, tokens):
        """Return a dict of words that appear after the tokens and their quantities."""
        next_dict = {}
        window = len(tokens)
        for i in range(len(self.padded_tokens) - window ):
            if self.padded_tokens[i: i + window] == tokens:
                next_word = self.padded_tokens[i + window]
                if next_word in next_dict:
                    next_dict[next_word] += 1
                else:
                    next_dict[next_word] = 1
        if 'PAD' in next_dict:
            next_dict.pop('PAD')
        if 'sos' in next_dict:
            next_dict.pop('sos')
        return next_dict

    def calc_probs(self, next_dict):
        """Return a dict with the same keys as returned by find_next 
        but the values are divided by total words.
        """
        total = 0
        for key in next_dict:
            if key in self.token_counts:
                total += next_dict[key]
        for key in next_dict:
            next_dict[key] = round((next_dict[key] / total), 3)
        return next_dict

    def p_next(self, tokens):
        """Return a dict of tokens and their probability of appearance in the text.
        Takes a list of strings as the argument.
        """
        next_dict = self.find_next(tokens)
        probs_dict = self.calc_probs(next_dict)
        return probs_dict

    def set_start_words(self):
        """Create and merge dictionaries of words that appear after punctuation."""
        self.start_words |= self.p_next(['.'])
        self.merge_dict_sum_values(self.start_words, self.p_next(['!']))
        self.merge_dict_sum_values(self.start_words, self.p_next(['?']))
        self.merge_dict_sum_values(self.start_words, self.p_next(['\n']))
        self.merge_dict_sum_values(self.start_words, self.p_next(['sos']))
        for key in self.start_words:
            self.start_words[key] = self.start_words[key] / len(self.start_words)
        return self.start_words

    def merge_dict_sum_values(self, dict1, dict2):
        for key in dict2:
            if key in dict1:
                dict1[key] += dict2[key]
            else:
                dict1[key] = dict2[key]
        return dict1

    def get_sample_start(self):
        """Return a sample word from the dictionary of words that appear after punctuation."""
        start = random.sample(sorted(self.start_words), 1)
        if start[0] == '\n':
            start = random.sample(sorted(self.start_words), 1)
        startword = start[0]
        return startword

    def find_gram(self, token):
        """Return a list of n-grams that start with the given token."""
        possible_list = []
        for gram in self.gram_list:
            if gram[0] == token:
                possible_list.append(gram)
        return possible_list
    
    def generate(self):
        """Create a string that is added to until \n is encountered."""
        eos = '\n'
        line = [self.get_sample_start()]
        possible = self.find_gram(line[0])
        choice = random.sample(possible, 1)
        sample = list(sum(choice,())) # Flatten choice into list of strings
        if self.n > 1:
            line.append(sample[1])
            line = self.append_next(eos, line, sample)
        else:
            line = self.append_next(eos, line, sample)
        result = corpus.detokenize(line)
        return result

    def append_next(self, eos, line, sample):
        """Add words to list until \n is encountered or the dict is empty.
        The last n words are fed back into p_next to create the sample dictionary.
        """
        while line[-1] != eos:
            nexttokens = self.p_next(sample)
            if nexttokens == {}:
                break
            if len(sample) > 1:
                del sample[0]
            nextlist = random.sample(sorted(nexttokens), 1)
            nextword = nextlist[0]
            add = sample[-1]
            if len(line) < self.n:
                line.append(add)
                line.append(nextword)
            else:
                line.append(nextword)
            sample = line[-self.n:]
        return line

    def most_common_token(self):
        """Return the most common token of the text and the quantity."""
        most_common = ''
        checked = 0
        for key in self.token_counts:
            if self.token_counts[key] > checked:
                checked = self.token_counts[key]
                most_common = key
        result = f'{most_common} occurs {checked} times.'
        return result

    def most_common_gram(self):
        """Return the most common ngram of the text and the quantity."""
        most_common = ()
        checked = 0
        for key in self.gram_counts:
            if self.gram_counts[key] > checked:
                checked = self.gram_counts[key]
                most_common = key
        result = f'{most_common} occurs {checked} times.'
        return result

    def make_probs_list(self, text):
        """Return list of probabilities for each word that appears."""
        new_tokens = corpus.tokenize(text)
        probs_list = []
        sequence = []
        for token in new_tokens[1:]:
            sequence = sequence[-self.n:]            
            get_from = self.p_next(sequence)
            if token in get_from:  
                prob = get_from[token]
            else:
                prob = 0
            probs_list.append(prob)
            sequence.append(token)
        return probs_list

    def calc_perplexity(self, probs_list):
        """Calculate arithmetic mean of log probabilities from list."""
        score = 0
        log_list = []
        for prob in probs_list:
            log_prob = math.log(prob)
            log_list.append(log_prob)
        for prob in log_list:
            score += prob
        score = score / len(log_list)
        score = math.exp(score)
        return score 

    def get_perplexity_score(self, text):
        probs_list = self.make_probs_list(text)
        score = self.calc_perplexity(probs_list)
        return score