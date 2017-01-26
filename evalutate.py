from collections import defaultdict

labels = {}
with open("test-labels.txt") as input_file:
	for sentence in input_file:
		sentence = sentence.strip("\n").split(" ")
		labels[sentence[0]] = [sentence[1], sentence[2]]

assigned_labels = {}

with open("answers.txt") as input_file:
	for sentence in input_file:
		sentence = sentence.strip("\n").split(" ")
		assigned_labels[sentence[0]] = [sentence[1], sentence[2]]

correct_count = 0.0
total = 0.0

for key in assigned_labels.keys():
	if assigned_labels[key][1] == labels[key][1] and assigned_labels[key][0] == labels[key][0]:
		correct_count += 1
	total += 1

print "Accuracy = " + str(correct_count/total * 100) + "%"
# correct_count_sentiments = 0.0
# correct_count_truthfulness = 0.0
# total = 0.0

# for key in assigned_labels.keys():
# 	if assigned_labels[key][1] == labels[key][1]:
# 		correct_count_sentiments += 1
# 	if assigned_labels[key][0] == labels[key][0]:
# 		correct_count_truthfulness += 1
# 	total += 1

# print "Accuracy (Sentiments) = "+str(correct_count_sentiments/total * 100) + "%"
# print "Accuracy (Truthfulness) = "+str(correct_count_truthfulness/total * 100) + "%"
