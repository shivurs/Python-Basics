from audioop import avg
import random
import corpus
import math
from queue import Queue

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
        self.gram_next = {}

    def train(self, token_sequences): 
        self.token_list = token_sequences
        self.token_counts = self.make_count_dict(token_sequences)
        self.gram_list = self.make_ngrams(token_sequences)
        self.gram_counts = self.make_count_dict(self.gram_list)
        self.padded_tokens = self.add_padding(token_sequences)
        self.start_words = self.set_start_words()
        self.gram_next = self.get_all_gram_next()

    def get_all_gram_next(self):
        for i in range(len(self.gram_list)-1):
            current_gram = self.gram_list[i]
            next_word = self.gram_list[i+1][self.n-1]
            if current_gram in self.gram_next:
                if next_word in self.gram_next[current_gram]:
                    self.gram_next[current_gram][next_word] += 1
                else:
                    new_dict = self.gram_next[current_gram] | {next_word:1}
                    self.gram_next[current_gram] = new_dict
            else:
                self.gram_next[current_gram] = {next_word:1}
        for gram, counts in self.gram_next.items():
            total = 0
            for key in counts:
                total += counts[key]
            for key in counts:
                counts[key] = counts[key] / total
        return self.gram_next
        
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
        sequence = tokens[-self.n:]
        if len(sequence) == 0:
            return self.find_gram_next('sos')
        elif len(sequence) < self.n:
            gram_list = self.find_gram_end(sequence[-1])
            gram = gram_list[0]
            return self.find_gram_next(gram[-1])
        else:
            gram = tuple(sequence)
            if gram in self.gram_next:
                return self.gram_next[gram]

    def find_gram_next(self, token):
        token_dict = {}
        for key in self.gram_next:
            if key[-1] == token:
                token_dict = self.merge_dict_sum_values(token_dict, self.gram_next[key])
        result = self.calc_probs(token_dict)        
        return result

    def get_next(self, tokens):
        next_dict = self.find_next(tokens)
        probs_dict = self.calc_probs(next_dict)
        return probs_dict

    def set_start_words(self):
        """Create and merge dictionaries of words that appear after punctuation."""
        self.start_words |= self.get_next(['.'])
        self.merge_dict_sum_values(self.start_words, self.get_next(['!']))
        self.merge_dict_sum_values(self.start_words, self.get_next(['?']))
        self.merge_dict_sum_values(self.start_words, self.get_next(['\n']))
        self.merge_dict_sum_values(self.start_words, self.get_next(['sos']))
        if '\n' in self.start_words:
            self.start_words.pop('\n')
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
        startword = start[0]
        return startword

    def find_gram(self, token):
        """Return a list of n-grams that start with the given token."""
        possible_list = []
        for gram in self.gram_list:
            if gram[0] == token:
                possible_list.append(gram)
        return possible_list

    def find_gram_end(self, token):
        """Return a list of n-grams that end with the given token."""
        possible_list = []
        for gram in self.gram_list:
            if gram[-1] == token:
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
        """Raise e to the mean of log probabilities from list."""
        avg_score = 0
        score_list = []
        for small_list in probs_list:
            score = 0
            log_list = []
            for prob in small_list:
                log_prob = math.log(prob)
                log_list.append(log_prob)
            for prob in log_list:
                score -= prob
            score = score / len(log_list)
            score = math.exp(score)
            score_list.append(score)
        if len(score_list) > 1:
            for i in range(len(score_list)-1):
                num = score_list[i] + score_list[i+1]
                print(num)
            avg_score = num / len(score_list)
        else:
            avg_score = score_list[0]
        return avg_score 

    def get_probs_list(self, new_tokens):
        """Create list of probability lists from p_next dictionaries."""
        new_tokens.append('\n\n')
        all_lists= []
        bookmark = 0
        next = ''
        while next != '\n\n':
            sequence = new_tokens[:self.n +1]
            probs_list = []
            prob = 0
            for i in range(1,len(new_tokens) - self.n):
                sequence = sequence[-self.n:]
                probs_dict = self.p_next(sequence)
                next = new_tokens[i + self.n]
                if next == '\n ':
                    next = next[:-1]
                if probs_dict == None or next not in probs_dict:
                    break
                elif next in probs_dict:  
                    prob = probs_dict[next]
                probs_list.append(prob)
                sequence.append(next)
                bookmark += 1
            all_lists.append(probs_list)
            new_tokens = new_tokens[(bookmark + self.n):]
        return all_lists
        
    def get_perplexity_score(self, generated):
        new_tokens = corpus.tokenize(generated)
        probs = self.get_probs_list(new_tokens)
        print(probs)
        score = self.calc_perplexity(probs)
        return score

    def get_smooth_perplexity(self, test_text):
        test_tokens = corpus.tokenize(test_text)
        self.add_oov_tokens(test_tokens) # 1. store OOV in UNK token # 2. count # of UNKs
        smooth_probs = self.get_smooth_probs(test_tokens) # 3. calc smooth probabilities (V = # UNKs)
        score = self.calc_perplexity(smooth_probs) # 4. calc perplexity        
        return score

    def get_highest_one(self, dict):
        """Return string with highest probability from the dictionary."""
        high_key = ''
        prob = 0
        for key in dict:
            if dict[key] > prob:
                high_key = key
                prob = dict[key]
        return high_key

    def greedy_generate(self):
        """Generate only tokens with the highest probabilities."""
        eos = '\n'
        next = self.get_sample_start()
        line = []
        used = set()    # Prevent infinite loop
        while next not in used and next != eos:
            line.append(next)
            used.add(next)
            next = self.get_highest_one(self.p_next(line))
        generated = corpus.detokenize(line)
        return generated

    def beam_generate(self, beam_width=2):
        """Generate sequences following the most probable beam_width paths."""
        startword = self.get_sample_start()
        que = Queue()
        que.put([startword])
        results = []
        while que.qsize() > 0:
            parent = que.get()
            if parent[-1] == '\n':
                results.append(corpus.detokenize(parent[:-1]))
                continue
            # Get the top beam_width priority children.
            children = self.get_children(parent, beam_width)
            for child in children:
                que.put(child)

        return results

    def get_children(self, parent, beam_width):
        """Return a list of children of length beam_width from the parent list."""
        allChildrenDic = self.p_next(parent)
        # sort to get the top priority beam_width elements
        sortAllChildrenDic = sorted(allChildrenDic.items(), key=lambda x: x[1], reverse=True)
        
        sortAllChildren = [tuple[0] for tuple in sortAllChildrenDic]    
        #sortAllChildren = []
        #for tuple in sortAllChildrenDic:
        #    sortAllChildren.append(tuple[0])

        results = []
        for i in range(0,beam_width):
            if i>= len(sortAllChildren):
                break
            row = []
            row.extend(parent)
            row.append(sortAllChildren[i])
            results.append(row)
        return results