import re
from nltk.util import ngrams
from glob import glob
import os
# from Tkinter import *

trigrams = []
GRAMS = 3
aleph_to_yaa_regex = '[\u0621-\u064A]'
arabic_letters_sequence = aleph_to_yaa_regex + '+'

files = glob(os.path.join(os.getcwd(), 'data', '*.txt'))
for file in files:
    cur_file = open(file)
    arabic_words_tokens = re.findall(arabic_letters_sequence, cur_file.read())
    trigrams.append(list(ngrams(arabic_words_tokens, GRAMS)))

print(trigrams)
