import string

from collections import defaultdict
from operator import itemgetter

input_text_path = "train-text.txt"

def tokenize(sentence):
	
	sentence = sentence.translate(None, string.punctuation)
	tokens = sentence.split(" ")

	return tokens[0],[token.lower() for token in tokens[1:] if token != "" ]

documents = defaultdict()
with open(input_text_path) as input_file:
	for sentence in input_file:
		sr_no, tokens = tokenize(sentence.rstrip())
		documents[sr_no] = tokens

words = defaultdict(int)

for sr_no in documents.keys():
	for token in list(set(documents[sr_no])):
		words[token] += 1

# stops = sorted(words.items(), key = itemgetter(1))

# print stops


print [x[0] for x in words.items() if x[1] >= 600]