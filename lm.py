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
        self.common_word = ''

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
        for i in range(len(self.padded_tokens) - window):
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
            next_dict[key] = next_dict[key] / total
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
        line = self.append_next(eos, sample)
        result = corpus.detokenize(line)
        return result

    def make_copy(self, reference):
        """Returns a new object with the same values but different reference."""
        copy = []
        for element in reference:
            copy.append(element)
        return copy

    def append_next(self, eos, sample):
        """Add words to list until eos is encountered or the dict is empty.
        The last n words are fed back into p_next to create the sample dictionary.
        """
        line = []
        line.extend(sample)
        while line[-1] != eos:
            nexttokens = self.p_next(sample)
            if nexttokens == {}:
                break
            if len(sample) > 1:
                del sample[0]
            nextlist = random.sample(sorted(nexttokens), 1)
            nextword = nextlist[0]
            line.append(nextword)
            sample = line[-self.n:]
        return line

    def most_common_word(self):
        """Return the most common token of the text and the quantity."""
        leave_out = set([',','.','!','\n'])
        checked = 0
        for key in self.token_counts:
            if key not in leave_out and self.token_counts[key] > checked:
                checked = self.token_counts[key]
                self.common_word = key
        result = f'\'{self.common_word}\' occurs {checked} times.'
        return result

    def most_common_word_gram(self):
        most_common = ()
        checked = 0
        for gram in self.gram_counts:
            if self.common_word == gram[0] and self.gram_counts[gram] > checked:
                checked = checked = self.gram_counts[gram]
                most_common = gram
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

    def add_oov_tokens(self, test_tokens):
        """Sum quantity of unseen tokens (will equal V in smoothing)."""
        self.token_counts['UNK'] = 0
        for token in test_tokens:
            if token not in set(self.token_list):
                self.token_counts['UNK'] +=1

    def calc_smooth_probs(self, next_dict):
        """Add one to all counts and divide by unique vocab total."""
        total = 0
        if 'UNK' in self.token_counts:
            v = self.token_counts['UNK']
            next_dict['UNK'] = 0
        else:
            v = 1
        for key in next_dict:
            if key in self.token_counts:
                total += next_dict[key]
        for key in next_dict:
            next_dict[key] = (next_dict[key] + 1) / (total + v)
        return next_dict
    
    def get_smooth_probs(self, test_tokens):
        probs_list = []
        sequence = test_tokens[1:self.n +1]
        prob = 0
        for i in range(1,len(test_tokens) - self.n):
            sequence = sequence[-self.n:]
            next_dict = self.find_next(sequence)
            probs_dict = self.calc_smooth_probs(next_dict)
            next = test_tokens[i + self.n]
            if next in probs_dict:  
                prob = probs_dict[next]
            else:
                prob = probs_dict['UNK']
            probs_list.append(prob)
            sequence.append(next)
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

    def get_smooth_perplexity(self, test_text):
        test_tokens = corpus.tokenize(test_text)
        self.add_oov_tokens(test_tokens) # 1. store OOV in UNK token # 2. count # of UNKs
        smooth_probs = self.get_smooth_probs(test_tokens) # 3. calc smooth probabilities (V = # UNKs)
        score = self.calc_perplexity(smooth_probs) # 4. calc perplexity        
        return score

    def get_probs_list(self, new_tokens):
        """Create list of probabilities from p_next dictionaries."""
        probs_list = []
        sequence = new_tokens[1:self.n +1]
        prob = 0
        for i in range(1,len(new_tokens) - self.n):
            sequence = sequence[-self.n:]
            probs_dict = self.p_next(sequence)
            next = new_tokens[i + self.n]
            if next in probs_dict:  
                prob = probs_dict[next]
            probs_list.append(prob)
            sequence.append(next)
        return probs_list
        
    def get_perplexity_score(self, generated):
        new_tokens = corpus.tokenize(generated)
        probs = self.get_probs_list(new_tokens)
        score = self.calc_perplexity(probs)
        return score

    def get_highest_one(self, dict):
        high_key = ''
        prob = 0
        for key in dict:
            if dict[key] > prob:
                high_key = key
        return high_key

    def greedy_generate(self):
        eos = '\n'
        next = ''
        line = [self.get_sample_start()]
        while next != eos:
            next = self.get_highest_one(self.p_next(line[-self.n:]))
            line.append(next)
        generated = corpus.detokenize(line)
        return generated