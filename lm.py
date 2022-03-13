import random
from typing import Dict, List
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
        token_sequences = self.add_unk_counts(token_sequences, 1)
        self.gram_list = self.make_ngrams(token_sequences)
        self.gram_counts = self.make_count_dict(self.gram_list)
        self.padded_tokens = self.add_padding(token_sequences)
        self.start_words = self.set_start_words()
        self.gram_next = self.get_all_gram_next()
        # Sort gram_list by last key for binary search.
        self.gram_list.sort(key=lambda x:(x[-1]))
        # Make a dictionary with the last token as keys to reuse.
        self.gram_next_merge_end: dict = self.makeGramNextMergeWithEnd()
   
    def makeGramNextMergeWithEnd(self):
        """Return a dictionary where keys are final token of ngrams, 
        values are dictionaries of next words and probabilities.
        """
        res = dict()
        for key in self.gram_next:
            if key[-1] not in res:
                res[key[-1]] = dict()
            res[key[-1]] = self.merge_dict_sum_values(res[key[-1]], self.gram_next[key])
        return res

    def add_unk_counts(self, token_sequences, cutoff=1):
        self.token_counts['UNK'] = 0
        delete = set()
        for token in self.token_counts:
            if token == 'sos' or token == '\n':
                pass
            elif self.token_counts[token] <= cutoff:
                self.token_counts['UNK'] += 1
                delete.add(token)
        for i in range(len(token_sequences)):
            check = token_sequences[i]
            if check in delete:
                if check in self.token_counts:
                    self.token_counts.pop(check)
                token_sequences[i] = 'UNK'
        return token_sequences

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

    def p_next(self, tokens=[]):
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
            else:
                return self.find_gram_next(gram[-1])

    def find_gram_next(self, token):
        """Return a dictionary of tokens that appear after the ngram
        including their probabilities.
        """
        token_dict = self.gram_next_merge_end[token]
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
        if 'UNK' in self.start_words:
            self.start_words.pop('UNK')
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

    def find_gram_start(self, token):
        """Return a list of n-grams that start with the given token."""
        possible_list = []
        for gram in self.gram_list:
            if gram[0] == token and 'UNK' not in gram:
                possible_list.append(gram)
        return possible_list


    def find_gram_end(self, token):
        """Return a list of n-grams that end with the given token."""
        possibleList = []
        left = 0
        right = len(self.gram_list)-1
        idx = -1
        while left < right:
            mid = (int)((left+right)/2)
            if self.gram_list[mid][-1] == token:
                idx = mid
                break
            elif self.gram_list[mid][-1] > token:
                right = mid
            else :
                left = mid+1
        if idx < 0:
            return []
        
        possibleList.append(self.gram_list[idx])
        leftIdx = idx - 1
        rightIdx = idx + 1
        while leftIdx >= 0 and self.gram_list[idx][-1] == self.gram_list[leftIdx][-1]:
            possibleList.append(self.gram_list[leftIdx])
            leftIdx -= 1
        while rightIdx < len(self.gram_list) and self.gram_list[idx][-1] == self.gram_list[rightIdx][-1]:
            possibleList.append(self.gram_list[rightIdx])
            rightIdx += 1
        return possibleList
    
    def generate(self):
        """Create a string that is added to until \n is encountered."""
        eos = '\n'
        line = [self.get_sample_start()]
        possible = self.find_gram_start(line[0])
        choice = random.sample(possible, 1)
        sample = list(sum(choice,())) # Flatten choice into list of strings
        line = self.append_next(eos, sample)
        result = corpus.detokenize(line)
        return result

    def append_next(self, eos, sample):
        """Add words to list until eos is encountered or the dict is empty.
        The last n words are fed back into p_next to create the sample dictionary.
        """
        line = []
        line.extend(sample)
        while line[-1] != eos:
            nexttokens = self.p_next(sample)
            if 'UNK' in nexttokens:
                nexttokens.pop('UNK')
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
        leave_out = set([',', '.', '!', '\n', 'UNK'])
        checked = 0
        for key in self.token_counts:
            if key not in leave_out and self.token_counts[key] > checked:
                checked = self.token_counts[key]
                self.common_word = key
        result = f'\'{self.common_word}\' occurs {checked} times.'
        return result

    def most_common_word_gram(self):
        """Return the common ngram starting with the common word."""
        most_common = ()
        checked = 0
        for gram in self.gram_counts:
            if self.common_word == gram[0] and self.gram_counts[gram] > checked:
                checked = self.gram_counts[gram]
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
            avg_score = num / len(score_list)
        else:
            avg_score = score_list[0]
        return avg_score 

    def make_probs_list(self, new_tokens):
        """Take a list of strings and return a list of probabilities."""
        new_tokens.append('eos')
        new_tokens.remove('sos')
        all_lists= []
        bookmark = 0
        nextword = ''
        while nextword != 'eos':
            prob = 0
            probs_list = []
            get_next = [new_tokens[0]]
            for i in range(len(new_tokens)):
                nextword = new_tokens[i+1]
                if nextword == '\n ':
                    nextword = nextword[:-1]
                if nextword == 'eos':
                    break
                next_dict = self.p_next(get_next)
                if nextword not in next_dict:
                    if 'UNK' in next_dict:
                        prob = next_dict['UNK']
                    else:
                        next_dict = self.p_next([get_next[-1]])     
                if nextword in next_dict:
                    prob = next_dict[nextword]
                elif 'UNK' in next_dict:
                        prob = next_dict['UNK']
                elif next_dict == {}:
                    break
                get_next.append(nextword)
                probs_list.append(prob)
                bookmark += 1
        all_lists.append(probs_list)
        new_tokens = new_tokens[(bookmark + self.n):]
        return all_lists
        
    def get_perplexity_score(self, generated):
        new_tokens = corpus.tokenize(generated)
        probs = self.make_probs_list(new_tokens)
        score = round(self.calc_perplexity(probs), 2)
        return score

    def get_test_perplexity(self, test_text):
        test_tokens = corpus.tokenize(test_text)
        new_tokens = self.replace_unk(test_tokens)
        probs = self.make_probs_list(new_tokens)
        score = round(self.calc_perplexity(probs), 2)
        return score

    def replace_unk(self, test_tokens):
        """Replace OOV tokens with 'UNK' tokens."""
        new_tokens = []
        check_set = set(self.token_list)
        for token in test_tokens:
            if token in check_set:
                new_tokens.append(token)
            else:
                new_tokens.append('UNK')
        return new_tokens

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
            next_dict = self.p_next(line)
            if next_dict == None:
                break
            if 'UNK' in next_dict:
                next_dict.pop('UNK')
            next = self.get_highest_one(next_dict)
        generated = corpus.detokenize(line)
        return generated

    def beam_generate(self, beam_width=1):
        """Generate sequences following the most probable beam_width paths."""
        startword = self.get_sample_start()
        que = Queue()
        que.put([startword])
        results = []
        while que.qsize() > 0:
            parent = que.get()
            if parent[-1] in set(results):
                break
            if parent[-1] == '\n':
                results.append(corpus.detokenize(parent[:-1]))
                continue
            # Get the top beam_width priority children.
            children = self.get_children(parent, beam_width)
            if children == []:
                results.append(corpus.detokenize(parent))
                break
            for child in children: 
                if child[-1] in parent and child[-2] in parent: 
                    results.append(corpus.detokenize(parent))
                    break
                else:
                    que.put(child)
        return results[0] # Only one result is needed.

    def get_children(self, parent, beam_width):
        """Return a list of children of length beam_width from the parent list."""
        all_child_dict = self.p_next(parent)
        if 'UNK' in all_child_dict:
            all_child_dict.pop('UNK')
        # Sort to get the top priority beam_width elements.
        sorted_child_dict = sorted(all_child_dict.items(), key=lambda x: x[1], reverse=True)
        
        sorted_child_list = [tuple[0] for tuple in sorted_child_dict]

        results = []
        for i in range(0, beam_width):
            if i >= len(sorted_child_list):
                break
            row = []
            row.extend(parent)
            row.append(sorted_child_list[i])
            results.append(row)
        return results