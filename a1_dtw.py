from dtw import dtw
from fastdtw import fastdtw
from ast import literal_eval
from math import radians, cos, sin, atan2, sqrt
import gmplot
import operator
import numpy as np
import pandas as pd
import timeit
import errno
import os

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
			'test_set_a1.csv', # replace with the correct path
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

#sub data
#trainSet = trainSet[0:100]

if(answer == '1'):
	path_dir = 'Maps_A1_DTW'
else:
	path_dir = 'Maps_A1_FastDTW'

try:
    os.mkdir(path_dir)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

row_list = []
test_counter = 1

for test in testSet:

	start = timeit.default_timer()

	row = []
	trip = "Trip Id " + str(test_counter)
	row.append(trip)

	trajectories_list = []
	i = 0
	for trajectory in trainSet:
		
		if answer == '1':
			distance, cost, accuracy, path  = dtw(test,trajectory, dist=haversine)
		else:
			distance, path = fastdtw(test, trajectory, dist=haversine)

		trajectories_list.append((i, distance))
		i = i + 1

	trajectories_list.sort(key=operator.itemgetter(1))
	list_map = trajectories_list[1:6]

	timestamp, lons, lats = zip(*test)

	gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 12)
	gmap.plot(lats, lons, 'green', edge_width=3)
	gmap.draw(path_dir +  os.sep + 'TrajectoryID_' + str(test_counter) +'.html')

	n_count = 1
	for map_traj in list_map:
		num_map=map_traj[0]
		timestamp, lons, lats = zip(*trainSet[num_map])

		neighbor_info = "JP_ID: " + trainSet_ids[num_map] + " DTW: " + str(map_traj[1]) + "km"
		row.append(neighbor_info)

		gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 12)
		gmap.plot(lats, lons, 'green', edge_width=3)
		gmap.draw(path_dir + os.sep +'TrajectoryID_' + str(test_counter) + '_Neighbor_' + str(n_count) + '.html')
		n_count = n_count + 1

	test_counter = test_counter + 1

	stop = timeit.default_timer()
	row.insert(1, stop-start)
	row_list.append(row)

#print results in a1_results_dtw.csv or a1_results_fastdtw.csv depending on choice of the user
df = pd.DataFrame(row_list, columns = [ 'TripId', 'Time', 'Neighbor1', 'Neighbor2', 'Neighbor3', 'Neighbor4', 'Neighbor5' ])

if answer == '1':
	df.to_csv('a1_results_dtw.csv', sep='\t', encoding='utf-8')
else:
	df.to_csv('a1_results_fastdtw.csv', sep='\t', encoding='utf-8')
