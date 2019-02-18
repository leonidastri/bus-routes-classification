# Data Mining Techniques -- Dublin's Bus Routes Classification
## About

This is the second project of the course Data Mining Techniques developed by **Ritsogianni Argyro** and **Triantafyllou Leonidas** in the Spring semester of 2018. In this project we learned about the Dynamic Time Warping (DTW) tεchnique and Longest Common Subsequence (LCSS) technique by applying them in order to find the nearest neighbboring bus routes in Dublin. This project is written in the programming language Python.

## Project Structure
  * Visualization of data
  * Nearest Neighbors using Dynamic Time Warping (DTW or FastDTW)
  * Nearest routes using Longest Common Subsequence (LCSS)
  * Routes Classification using Dynamic Time Warping (DTW)
  * Calculating geographical distances between 2 GPS points by using Harversine Distance Formula

## Part 1 - Visualization of Data :
Visualization of 5 different bus routes using Python gmplot and storing them in Random_Maps directory.
```
python vis_of_data.py
```

## Part 2a - Nearest Neighbors using Dynamic Time Warping :
Using Dynamic Time Warping (DTW or FastDTW) to find for every route in test_set_a1.csv the 5 nearest neighboring routes in train_set.csv. Results are stored in Maps_A1_DTW or Maps_A1_FastDTW directory respectively.
```
python a1_dtw.py
```

## Part 2b - Nearest routes using Longest Common Subsequence:
Using Longest Common Subsequence (LCSS) technique to find for every route in test_set_a2.csv the k parts of routes in train_set.csv that are similar. Results are stored in Maps_A2_LCSS directory.
```
python a2_lcss.py
```
## Part 3 - Classification of routes:
Classification of bus routes using k-nn(k=5) and Dynamic Time Warping (DTW or FastDTW) and prediction of the bus routes that the trips in test_set.csv are part of. Results are stored in testSet_JourneyPatternIDs.csv.
```
python classification.py
```

![Alt text](pictures/bus_route.png?raw=true "Title")

## Team Members and Contact Details

* Ritsogianni Argyro: sdi1400171@di.uoa.gr
* Triantafyllou Leonidas: sdi1400202@di.uoa.gr
