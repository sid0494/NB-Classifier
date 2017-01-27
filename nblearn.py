import sys
import math
import string
from collections import defaultdict
from operator import itemgetter

stop_words = ['', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cannot', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'hel', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shel', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'your']
input_text_path = sys.argv[1]
input_label_path = sys.argv[2]

def tokenize(sentence):
	
	sentence = sentence.translate(None, string.punctuation)
	tokens = sentence.split(" ")

	return tokens[0],[token for token in tokens[1:] if token.lower() not in stop_words ]



documents = defaultdict()
with open(input_text_path) as input_file:
	for sentence in input_file:
		sr_no, tokens = tokenize(sentence.rstrip())
		documents[sr_no] = tokens

labels = {}
document_count = {"truthful&positive":0.0, "truthful&negative":0.0, "deceptive&positive":0.0, "deceptive&negative":0.0}
with open(input_label_path) as input_file:
	for sentence in input_file:
		sentence = sentence.rstrip().split(" ")
		document_count[sentence[1]+"&"+sentence[2]] += 1
		labels[sentence[0]] = sentence[1]+"&"+sentence[2]

# print labels
scores = defaultdict(lambda: {"truthful&positive":1.0, "truthful&negative":1.0, "deceptive&positive":1.0, "deceptive&negative":1.0})
vocab = []

for sr_no in documents.keys():
	for token in documents[sr_no]:
		scores[token][labels[sr_no]] += 1
		vocab.append(token)

words_in_tp = 0
words_in_dn = 0
words_in_tn = 0
words_in_dp = 0

tn = document_count["truthful&negative"]/(document_count["truthful&negative"] + document_count["deceptive&positive"] + document_count["truthful&positive"] + document_count["deceptive&negative"])
dp = document_count["deceptive&positive"]/(document_count["truthful&negative"] + document_count["deceptive&positive"] + document_count["truthful&positive"] + document_count["deceptive&negative"])
tp = document_count["truthful&positive"]/(document_count["truthful&negative"] + document_count["deceptive&positive"] + document_count["truthful&positive"] + document_count["deceptive&negative"])
dn = document_count["deceptive&negative"]/(document_count["truthful&negative"] + document_count["deceptive&positive"] + document_count["truthful&positive"] + document_count["deceptive&negative"])

# print len(vocab) + 2*len(set(vocab))



for key in scores.keys():
	words_in_tp += scores[key]["truthful&positive"]
	words_in_dn += scores[key]["deceptive&negative"]
	words_in_tn += scores[key]["truthful&negative"]
	words_in_dp += scores[key]["deceptive&positive"]

# print "Positive: {} Negative: {} Truthful: {} Deceptive: {}\nTotal in sentiments: {} \nTotal in truthfulness: {}".format(a,b,c,d,a+b,c+d)


with open("nbmodel.txt","w") as f:

	f.write(str(math.log(tp)) + " " + str(math.log(dn)) + " " + str(math.log(tn)) + " " + str(math.log(dp)) + "\n")
	f.write(str(math.log(1.0/words_in_tp)) + " " + str(math.log(1.0/words_in_dn)) + " " + str(math.log(1.0/words_in_tn)) + " " + str(math.log(1.0/words_in_dp)) + "\n")
	for key in scores.keys():
		f.write(key + " ")
		scores[key]["truthful&positive"] = math.log(scores[key]["truthful&positive"]/words_in_tp)
		f.write(str(scores[key]["truthful&positive"]) + " ")
		scores[key]["deceptive&negative"] = math.log(scores[key]["deceptive&negative"]/words_in_dn)
		f.write(str(scores[key]["deceptive&negative"]) + " ")
		scores[key]["truthful&negative"] = math.log(scores[key]["truthful&negative"]/words_in_tn)
		f.write(str(scores[key]["truthful&negative"]) + " ")
		scores[key]["deceptive&positive"] = math.log(scores[key]["deceptive&positive"]/words_in_dp)
		f.write(str(scores[key]["deceptive&positive"]) + "\n")