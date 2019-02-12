import pandas as pd
from ast import literal_eval
import numpy
import random
import gmplot
import errno
import os

trainSet = pd.read_csv(
			'train_set.csv', # replace with the correct path
			converters={"Trajectory": literal_eval},
			index_col='tripId'
		)

#making directory for saving htmls
path_dir = 'Random_Maps'
try:
    os.mkdir(path_dir)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

#set of unique journeyPatternIds for random selection
jpid = set(trainSet['journeyPatternId'])
random_jpid_list = random.sample(jpid,5)

#5-plot itteration 
for r_jpid in random_jpid_list:

    #find all data with same journeyPatternId
    data = trainSet[trainSet['journeyPatternId'] == r_jpid]
    data = numpy.array(data['Trajectory'])

    #pick random trajectory from data with same journeyPatternId
    random_num = random.randint(0, (len(data)-1))
    timestamp, lons, lats = zip(*data[random_num])

    #coordinates of Dublin (with zoom 12)
    gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 12)
    gmap.plot(lats, lons, 'green', edge_width=3)
    gmap.draw(path_dir + os.sep + 'JourneyPatternId_' + str(r_jpid) + '.html')