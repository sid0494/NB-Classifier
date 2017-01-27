import sys
import math
import string
from collections import defaultdict
from operator import itemgetter

stop_words = ['', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cannot', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'hel', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shel', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'your']
input_text_path = sys.argv[1]

def tokenize(sentence):
	
	sentence = sentence.translate(None, string.punctuation)
	tokens = sentence.split(" ")

	return tokens[0],[token for token in tokens[1:] if token.lower() not in stop_words ]

def calculate_probability(tokens, label, priors, conditional_probability):
	
	probability = priors[label]

	for token in tokens:
		probability += conditional_probability[token][label]

	return probability

def classify(documents, priors, conditional_probability):

	assigned_labels = {}

	for sr_no in documents.keys():
		tp = calculate_probability(documents[sr_no], "truthful&positive", priors, conditional_probability)
		tn = calculate_probability(documents[sr_no], "truthful&negative", priors, conditional_probability)
		dp = calculate_probability(documents[sr_no], "deceptive&positive", priors, conditional_probability)
		dn = calculate_probability(documents[sr_no], "deceptive&negative", priors, conditional_probability)

		assigned_labels[sr_no] = sorted([(tp,"truthful positive"),(tn, "truthful negative"),(dp, "deceptive positive"),(dn, "deceptive negative")], key = itemgetter(0))[-1][1]

	return assigned_labels


documents = defaultdict()
priors = {}
conditional_probability = defaultdict(lambda: {"truthful&positive":0.0, "truthful&negative":0.0, "deceptive&positive":0.0, "deceptive&negative":0.0})
tp = 0.0
tn = 0.0
dp = 0.0
dn = 0.0

with open(input_text_path) as input_file:
	for sentence in input_file:
		sr_no, tokens = tokenize(sentence.rstrip())
		documents[sr_no] = tokens

with open("nbmodel.txt") as f:
	data = f.readline().rstrip().split(" ")
	priors = {"truthful&positive": float(data[0]), "deceptive&negative": float(data[1]), "truthful&negative": float(data[2]), "deceptive&positive": float(data[3])}
	data = f.readline().rstrip().split(" ")
	# positive = float(data[0])
	# negative = float(data[1])
	# truthful = float(data[2])
	# deceptive = float(data[3])
	conditional_probability = defaultdict(lambda: {"truthful&positive": tp, "deceptive&negative": dn, "truthful&negative": tn, "deceptive&positive": dp})
	count = 0
	for sentence in f:
		count += 1
		# print str(count) + sentence 
		# raw_input()
		data = sentence.rstrip().split(" ")
		conditional_probability[data[0]] = {"truthful&positive": float(data[1]), "deceptive&negative": float(data[2]), "truthful&negative": float(data[3]), "deceptive&positive": float(data[4])}

classified_data = classify(documents, priors, conditional_probability)

with open("nboutput.txt","w") as f:
	for key in classified_data.keys():
		f.write(key + " " + str(classified_data[key]) + "\n")

