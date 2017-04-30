import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
import sys
import collections

## Get user inputs and check if they are entered correctly
arg_names = ['code', 'featureFile', 'outputFile']
args = dict(zip(arg_names, sys.argv))
Arg_list = collections.namedtuple('Arg_list', arg_names)
args = Arg_list(*(args.get(arg, None) for arg in arg_names))

for (idx,arg) in enumerate(args):
	if arg == None:
		print "Error: "+ arg_names[idx] + " is None."
		print "Correct usage: $python aggregateBumpiness.py featureFile outputFile"
		sys.exit()


bumpiness = []
aggBumpiness = []

# Lamda functions to scale the bumpiness values.
f = lambda a: a if (a > 0) else 0
g = lambda a: a*10000/25

def addArray(arr):
	for i in arr:
		aggBumpiness.append(i)

def addArrayAverage(arr1,arr2):
	for idx,item in enumerate(arr1):
		aggBumpiness.append(max(arr1[idx],arr2[idx]))

def createCollection(collection):
	for item in collection:
		bumpiness.append(item[:10])

def writeAggregatedFeatures(outputFile,bumpinessAggregate):
	agg = np.asarray(bumpinessAggregate)
	np.save(outputFile,agg)

def aggregate(bumpiness):
	for idx,bumps in enumerate(bumpiness):
		if idx == 0:
			addArray(bumpiness[idx][:5])
		if idx == len(bumpiness)-1:
			addArray(bumpiness[idx][5:])
		else:
			addArrayAverage(bumpiness[idx][5:], bumpiness[idx+1][:5])
	return aggBumpiness
	
createCollection(np.load(sys.argv[1]))
aggregate(bumpiness)
print aggBumpiness
print len(aggBumpiness)

minVal = min(aggBumpiness)
print minVal
thres = minVal + 0.0625
aggBumpiness[:] = [x - thres for x in aggBumpiness]
aggBumpiness = map(f,aggBumpiness)
aggBumpiness = map(g,aggBumpiness)
writeAggregatedFeatures(sys.argv[2],aggBumpiness)
print aggBumpiness