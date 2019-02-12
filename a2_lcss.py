from ast import literal_eval
from math import radians, cos, sin, atan2, sqrt
import gmplot
import operator
import numpy as np
import pandas as pd
import timeit
import errno
import os

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

def haversine(x, y):

	timestamp1, lons1, lats1 = x
	timestamp2, lons2, lats2 = y

	lons1, lats1, lons2, lats2 = map(radians, [lons1, lats1, lons2, lats2])

	dif_lons = lons2 - lons1 
	dif_lats = lats2 - lats1

	a = sin(dif_lats/2)**2 + cos(lats1) * cos(lats2) * sin(dif_lons/2)**2

	c = 2 * atan2(sqrt(a),sqrt(1-a)) 
	r = 6371

	return c * r

#LCSS algirithm
def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if haversine(X[i-1] ,Y[j-1]) <= 0.2 : 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def backTrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return []
    elif haversine(X[i-1] ,Y[j-1]) <= 0.2 :
        return backTrack(C, X, Y, i-1, j-1) + [X[i-1]]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)

#creating a directory to save the maps
path_dir = 'Maps_A2_LCSS'
try:
    os.mkdir(path_dir)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

row_list = []
trip_counter = 1
for X in testSet:

	start = timeit.default_timer()

	row = []
	sub_traj = []
	i = 0

	trip = "Trip Id " + str(trip_counter)
	row.append(trip)

	for Y in trainSet:
		m = len(X)
		n = len(Y)
		C = LCS(X, Y)

		b = backTrack(C, X, Y, m, n)
		sub_traj.append( ( b, len(b), i ) )
		i = i + 1

	sub_traj.sort(key=operator.itemgetter(1), reverse=True)
	sub_traj = sub_traj[0:5]

	timestamp, lons, lats = zip(*X)
	gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 12)
	gmap.plot(lats, lons, 'green', edge_width=3)
	gmap.draw(path_dir +  os.sep + 'TrajectoryID_' + str(trip_counter) + '.html')

	n_count = 1
	for map_traj in sub_traj:

		num_map=map_traj[2]

		timestamp, lons, lats = zip(*trainSet[num_map])
		gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 12)
		gmap.plot(lats, lons, 'green', edge_width=3)

		timestamp, lons, lats = zip(*map_traj[0])
		gmap.plot(lats, lons, 'red', edge_width=3)
		gmap.draw(path_dir + os.sep +'TrajectoryID_' + str(trip_counter) + '_SubRoute_' + str(n_count) + '.html')

		neighbor_info = "JP_ID: " + trainSet_ids[num_map] + " #Matching points: " + str(map_traj[1])
		row.append(neighbor_info)

		n_count = n_count + 1

	stop = timeit.default_timer()
	row.insert(1, stop-start)

	print "Time for trip " + str(trip_counter) + ": " + str(stop-start)
	trip_counter = trip_counter + 1

	row_list.append(row)

#print results in a2_results.csv
df = pd.DataFrame(row_list, columns = [ 'TripId', 'Time', 'Neighbor1', 'Neighbor2', 'Neighbor3', 'Neighbor4', 'Neighbor5' ])
df.to_csv('a2_results.csv', sep='\t', encoding='utf-8')
