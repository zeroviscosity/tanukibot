import datetime as dt
import markovify
import nltk
import os
import re
import random
import time
from .scored_sentence import ScoredSentence

STOP_WORDS = set([' ', 'a', 'about', 'an', 'and', 'are', 'be', 'been', 'can', 'could', 'do', 'done', 'for', 'he', 'here', 'hes', 'i', 'id', 'if', 'im', 'in', 'me', 'my', 'no', 'not', 'on', 'or', 'she', 'shes', 'so', 'talk', 'tell', 'the', 'their', 'them', 'there', 'them', 'they', 'us', 'we', 'were', 'you', 'your', 'youre'])
NON_ALPHA_REGEX = r'[^a-z\s]'
MULTI_SPACE_REGEX = r'\s{2,}'

class Core:
    def __init__(self, corpus='tanuki.txt', stop_words=STOP_WORDS, stemmer_lang='english', sentence_min=50, sentence_max=250, initial_size=10000):
        self.corpus = corpus
        self.stop_words = stop_words
        self.stemmer = nltk.stem.SnowballStemmer(stemmer_lang)
        self.sentence_min = sentence_min
        self.sentence_max = sentence_max
        self.model = None
        self.sentences = {}
        self.lexicon = {}

        self.load_model()
        self.generate_sentences(initial_size)

    def load_model(self):
        with open(self.corpus) as f:
            corpus = f.read()
        self.model = markovify.NewlineText(corpus)

    def sentence_to_words(self, sentence):
        lowered = sentence.lower()
        alphaed = re.sub(NON_ALPHA_REGEX, '', lowered)
        trimmed = re.sub(MULTI_SPACE_REGEX, ' ', alphaed).strip()
        words = trimmed.split(' ')
        stemmed = [self.stemmer.stem(word) for word in words]
        return set(stemmed).difference(self.stop_words)

    def generate_sentences(self, n=1000):
        for i in range(n):
            sentence = self.model.make_short_sentence(self.sentence_max, self.sentence_min)
            if not sentence:
                continue
            key = hash(sentence.lower())
            if key in self.sentences:
                continue
            self.sentences[key] = ScoredSentence(sentence)
            # Determine the relevant words
            words = self.sentence_to_words(sentence)
            # Add the word to the lexicon for quick look up
            for word in words:
                if word not in self.lexicon:
                    self.lexicon[word] = set()
                self.lexicon[word].add(key)

    def get_sentence(self, prompt):
        words = self.sentence_to_words(prompt)
        keys = set()
        sentence = None
        for word in words:
            if word not in self.lexicon:
                continue
            keys = keys.union(self.lexicon[word])
        print('Potential matches:', len(keys))
        for key in keys:
            if key not in self.sentences:
                continue
            sentence = self.sentences[key].compare(sentence)
        if not sentence:
            print('No match found')
            return None
        else:
            sentence.last_used = dt.datetime.now()
            return sentence.text
