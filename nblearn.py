import math
import string
from collections import defaultdict
from operator import itemgetter

stop_words = ['', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cannot', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'hel', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shel', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'your']

def tokenize(sentence):
	
	sentence = sentence.translate(None, string.punctuation)
	tokens = sentence.split(" ")

	return tokens[0],[token for token in tokens[1:] if token.lower() not in stop_words ]





# my_string = "07I2RiEXiuvkfEkSiByp Just returned from a one night stay at the Knickerbocker, and I will not return. It came nowhere near being worth the price I paid. Hotel Burnham is twice the hotel at half the price! The bathroom was unbelieveably small and smelled terribly. We had to call the front desk twice before towels that we requested were delivered (which frankly may as well have been paper towels, nothing plush about them at all). We didn't have enough pillows and when we requested an extra it was never delivered. Room service cart was left outside our door all night. All in all, it was a very disappointing stay. The only redeeming quality of this hotel seems to be its location. And for me, it's just not worth it. "

# print tokenize(my_string)


documents = defaultdict()
with open("train-text.txt") as input_file:
	for sentence in input_file:
		sr_no, tokens = tokenize(sentence.strip("\n"))
		documents[sr_no] = tokens

labels = {}
document_count = {"positive":0.0, "negative":0.0, "truthful":0.0, "deceptive":0.0}
with open("train-labels.txt") as input_file:
	for sentence in input_file:
		sentence = sentence.strip("\n").split(" ")
		document_count[sentence[2]] += 1
		document_count[sentence[1]] += 1
		labels[sentence[0]] = {"sentiment": sentence[2], "truthfulness": sentence[1]}

print labels
scores = defaultdict(lambda: {"positive":1.0, "negative":1.0, "truthful":1.0, "deceptive":1.0})
vocab = []

for sr_no in documents.keys():
	for token in documents[sr_no]:
		scores[token][labels[sr_no]["sentiment"]] += 1
		scores[token][labels[sr_no]["truthfulness"]] += 1
		vocab.append(token)

words_in_positive = 0
words_in_negative = 0
words_in_truthful = 0
words_in_deceptive = 0

positive = document_count["negative"]/(document_count["positive"]+document_count["negative"])
negative = document_count["positive"]/(document_count["positive"]+document_count["negative"])
truthful = document_count["truthful"]/(document_count["truthful"]+document_count["deceptive"])
deceptive = document_count["deceptive"]/(document_count["truthful"]+document_count["deceptive"])

print len(vocab) + 2*len(set(vocab))



for key in scores.keys():
	words_in_positive += scores[key]["positive"]
	words_in_negative += scores[key]["negative"]
	words_in_truthful += scores[key]["truthful"]
	words_in_deceptive += scores[key]["deceptive"]

# print "Positive: {} Negative: {} Truthful: {} Deceptive: {}\nTotal in sentiments: {} \nTotal in truthfulness: {}".format(a,b,c,d,a+b,c+d)


with open("nbmodel.txt","w") as f:

	f.write(str(math.log(positive)) + " " + str(math.log(negative)) + " " + str(math.log(truthful)) + " " + str(math.log(deceptive)) + "\n")
	f.write(str(math.log(1.0/words_in_positive)) + " " + str(math.log(1.0/words_in_negative)) + " " + str(math.log(1.0/words_in_truthful)) + " " + str(math.log(1.0/words_in_deceptive)) + "\n")
	for key in scores.keys():
		f.write(key + " ")
		scores[key]["positive"] = math.log(scores[key]["positive"]/words_in_positive)
		f.write(str(scores[key]["positive"]) + " ")
		scores[key]["negative"] = math.log(scores[key]["negative"]/words_in_negative)
		f.write(str(scores[key]["negative"]) + " ")
		scores[key]["truthful"] = math.log(scores[key]["truthful"]/words_in_truthful)
		f.write(str(scores[key]["truthful"]) + " ")
		scores[key]["deceptive"] = math.log(scores[key]["deceptive"]/words_in_deceptive)
		f.write(str(scores[key]["deceptive"]) + "\n")


positive = []
negative = []
for key in scores.keys():
	positive.append((key, scores[key]["positive"]))
	negative.append((key, scores[key]["negative"]))

positive = sorted(positive, key = itemgetter(1))
negative = sorted(negative, key = itemgetter(1))

print document_count

