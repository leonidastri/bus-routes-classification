import myknn
from sklearn.model_selection import KFold
from sklearn.metrics import *
from ast import literal_eval
import numpy as np
import pandas as pd
import csv
import timeit

#User chooses fast or simple dtw
answer = ''

while (answer != '1' and answer != '2'):
	answer = raw_input("Press 1 for DTW\nPress 2 for Fast DTW\nAnswer: ")

if answer == '1':
	print "Running with DTW"
else:
	print "Running with Fast DTW"

trainSet = pd.read_csv(
			'train_set.csv', # replace with the correct path
			converters={"Trajectory": literal_eval},
			index_col='tripId'
		)

testSet = pd.read_csv(
			'test_set_a2.csv', # replace with the correct path
			converters={"Trajectory": literal_eval},
			sep='\t'
			)

trainSet_ids = np.array(trainSet["journeyPatternId"])
trainSet = np.array(trainSet["Trajectory"])
testSet = np.array(testSet["Trajectory"])

#sample of data
trainSet = trainSet[0:300]


kf = KFold(n_splits=10)
ac = 0
kf_counter = 1

for train_index, test_index in kf.split(trainSet):
	start = timeit.default_timer()
	#print("TRAIN:", train_index, "TEST:", test_index)
	X_train, X_test = trainSet[train_index], trainSet[test_index]
	y_train, y_test = trainSet_ids[train_index], trainSet_ids[test_index]
	predicted = myknn.myKnn(X_test, X_train, y_train, 5, answer)

	ac += accuracy_score(y_test, predicted)
	stop = timeit.default_timer()

	print "Time for kfold " + str(kf_counter) + ": " + str(stop-start) 
	kf_counter = kf_counter + 1

print "Average accuracy: " + str(ac/10)

y_predicted = myknn.myKnn(testSet, trainSet, trainSet_ids, 5, answer)

rows = [['Test_Trip_ID', 'Predicted_JourneyPatternID']]
count_id = 1
for y in y_predicted:
	rows.append([count_id , y])
	count_id = count_id + 1

if answer == '1':
	myCsv= open('testSet_JourneyPatternIDs_dtw.csv', 'w')
	print 'Writing to csv file \'testSet_JourneyPatternIDs_dtw.csv\' the metric results'
else:
	myCsv= open('testSet_JourneyPatternIDs_fastdtw.csv', 'w')
	print 'Writing to csv file \'testSet_JourneyPatternIDs_fastdtw.csv\' the metric results'

CsvData = rows

with myCsv:
	writer = csv.writer(myCsv)
	writer.writerows(CsvData)
