import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
import sys
import collections
import argparse


## Get user inputs and check if they are entered correctly
parser = argparse.ArgumentParser()
parser.add_argument("--featureFile", default="MBHxFeatures.npy")
parser.add_argument("--outputFile", default="MBHxAggFeatures.npy")
parser.add_argument("--environ", default="test")
args = parser.parse_args()
print args

global bumpiness
global aggBumpiness

bumpiness = []
aggBumpiness = []

# Lamda functions to scale the bumpiness values.
f = lambda a: a if (a > 0) else 0
g = lambda a: a*10000/25

def addArray(arr):
	'''
	The following two funcions assist in adding the bumpiness value per second.
	They overlap the second values to get an aggregated and continous value.
	'''
	for i in arr:
		aggBumpiness.append(i)

def addArrayAverage(arr1, arr2):
	for idx,item in enumerate(arr1):
		aggBumpiness.append(max(arr1[idx], arr2[idx]))

def createCollection(collection):
	'''
	This function ensures that each clip used for overlapping is only 10 seconds.
	'''
	for item in collection:
		bumpiness.append(item[:10])
	return bumpiness

def writeAggregatedFeatures(outputFile, bumpinessAggregate):
	'''
	This function writes the aggregated values to a new featureFile for clustering.
	'''
	agg = np.asarray(bumpinessAggregate)
	np.save(outputFile,agg)

def aggregate(bumpiness):
	'''
	This funciton is where the main overlapping takes place. 
	Each video sentence is overlapped by 5 seconds.
	'''
	global aggBumpiness
	aggBumpiness = []
	for idx,bumps in enumerate(bumpiness):
		if idx == 0:
			addArray(bumpiness[idx][:5])
		if idx == len(bumpiness)-1:
			addArray(bumpiness[idx][5:])
		else:
			addArrayAverage(bumpiness[idx][5:], bumpiness[idx+1][:5])
	return aggBumpiness

def scaleAggregates(arr):
	'''
	This function scales up the aggregates using tha lambda functions defined above.
	'''
	try:
		minVal = min(arr)
	except ValueError:
		return None
	print minVal
	thres = minVal + 0.0625
	arr[:] = [x - thres for x in arr]
	arr = map(f,arr)
	arr = map(g,arr)
	print arr
	return arr

if args.environ == "dep":
	print "Deploying algorithm..."	
	#Load the feature files
	createCollection(np.load(args.featureFile))
	print bumpiness
	#Aggregate the features by overlap.
	aggregate(bumpiness)
	#Scale the aggregates to 1-10
	aggBumpiness = scaleAggregates(aggBumpiness)
	print aggBumpiness
	#Write the aggregated features to feature file to be used for clustering.
	writeAggregatedFeatures(args.outputFile, aggBumpiness)
	print ("Here", aggBumpiness)