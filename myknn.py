import math
import operator
from dtw import dtw
from fastdtw import fastdtw
from math import radians, cos, sin, atan2, sqrt


def haversine(x, y):

	timestamp1, lons1, lats1 = x
	timestamp2, lons2, lats2 = y

	lons1, lats1, lons2, lats2 = map(radians, [lons1, lats1, lons2, lats2])

	dif_lons = lons2 - lons1 
	dif_lats = lats2 - lats1

	a = sin(dif_lats/2)**2 + cos(lats1) * cos(lats2) * sin(dif_lons/2)**2

	c = 2 * atan2(sqrt(a),sqrt(1-a)) 
	r = 6371     #Km

	return c * r

def getMjVotes(neighbors, y):
	classVotes = {}
	nhbrs = y[neighbors]
	for x in range(len(nhbrs)):
		response = nhbrs[x]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]


def myKnn(testdata, traindata, y, k, answer):
	responses = []
	for test in testdata:
		distances = []
		position = 0
		for trajectory in traindata:

			#dtw or fastdtw for computing the distance
			if answer == '1':
				dist, cost, accuracy, path = dtw(test, trajectory, dist=haversine)
			else:
				dist, path = fastdtw(test, trajectory, dist=haversine)

			distances.append((position, dist))
			position += 1
		distances.sort(key=operator.itemgetter(1))
		neighbors = []
		for x in range(k):
			neighbors.append(distances[x][0])
		response = getMjVotes(neighbors,y)
		responses.append(response)
	return responses
