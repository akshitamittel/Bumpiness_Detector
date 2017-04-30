import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.font_manager
from scipy.io import *
import cv2
import math
import sys

## Get user inputs and check if they are entered correctly
arg_names = ['code', 'videoName', 'featureFile', 'outputFile', 'feature']
args = dict(zip(arg_names, sys.argv))
Arg_list = collections.namedtuple('Arg_list', arg_names)
args = Arg_list(*(args.get(arg, None) for arg in arg_names))

for (idx,arg) in enumerate(args):
	if arg == None:
		print "Error: "+ arg_names[idx] + " is None."
		print "Correct usage: $python bumpiness.py videoName featureFile outputFile feature"
		sys.exit()

# Get the input video and feature file names
videoDirectory = "/media/sdj/Akshita/"
featureDirectory = "/media/sdj/Akshita/"
vid = videoDirectory + args[1]
denseFeatures = featureDirectory + args[2]

# Set variables
thresholdAgg = -10
thresholdFrames = -10
feature = int(sys.argv[4])
getFeats = [0,0,0,1,0]
if feature == 0:
	getFeats = [0,0,1,0,0]
seconds = 10

# Get video information
cap = cv2.VideoCapture(vid)
numFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
fps = math.ceil(cap.get(cv2.cv.CV_CAP_PROP_FPS))
print ("FPS", fps)


'''
Returns the set of features alond with the frame numbers of the interest points.
Takes as input the dense-trajectory features and returns user-specified features.
Usage: get_data(filename,[x1,x2,x3,x4,x5])
xi are binary values where:
- x1:TRAJ
- x2:HOG
- x3:HOF
- x4:MBHx
- x5:MBHy
'''
def getData(filename, features):
	print "In getData:"
	print "-----------"
	X = np.loadtxt(filename)
	print "Features loaded."
	TRAJ = X[0: ,10:40]
	NaNs = np.isnan(TRAJ)
	TRAJ[NaNs] = 0
	HOG = X[0: ,40:136]
	NaNs = np.isnan(HOG)
	HOG[NaNs] = 0
	HOF = X[0: ,136:244]
	NaNs = np.isnan(HOF)
	HOF[NaNs] = 0
	MBHx = X[0: ,244:340]
	NaNs = np.isnan(MBHx)
	MBHx[NaNs] = 0
	MBHy = X[0: ,340:436]
	NaNs = np.isnan(MBHy)
	MBHy[NaNs] = 0
	feats = [TRAJ, HOG, HOF, MBHx, MBHy]

	print "Collected features."
	result = np.empty((TRAJ.shape[0],1))
	for idx,feature in enumerate(features):
		if feature == 1:
			result = np.hstack((result,feats[idx]))
	result = np.delete(result,0,1)
	frames = X[0: ,0:1]
	print ("frames", frames)
	return result,frames

'''
For each frame the descriptors return a set of values for interest points.
getFeatureAggregates aggregates the interest point values for each frame.
It returns as a list the value of the aggregate per frame.
'''
def getFeatureAggregates(descriptors,frames,thres):
	print "In getFeatureAggregates:"
	print "------------------------"
	frameValues = {}
	for idx,frameFeats in enumerate(descriptors):
		if int(frames[idx][0]) not in frameValues:
			frameValues[int(frames[idx][0])] = []
		aggVal = sum(descriptors[idx])/len(descriptors[idx])
		if aggVal >= thres:
			frameValues[int(frames[idx][0])].append(aggVal)
	frameAgg = []
	for idx in range(numFrames):
		if idx not in frameValues:
			frameAgg.append(0)
		else:
			frameAgg.append(sum(frameValues[idx])/len(frameValues[idx]))
	print ("FrameAgg", frameAgg)
	print len(frameAgg)
	return frameAgg

'''
Find a value of bumpiness for each second of the input video.
'''
def getBumpiness(frameAgg,thres,fps):
	print "In getBumpiness:"
	print "----------------"
	bumpiness = []
	temp = []
	for idx,frame in enumerate(frameAgg):
		if idx%fps==0:
			if idx!=0:
				bumpiness.append(sum(temp)/len(temp))
			temp = []
		temp.append(frame)
	bumpiness.append(sum(temp)/len(temp))
	print ("Bumpiness", bumpiness)
	return bumpiness

'''
Take the value of the aggregate for each second and plot it.
'''
def drawGraph(bumpinessAggregate):
	print "In drawGraph:"
	print "-------------"
	plt.plot(bumpinessAggregate)
	plt.ylabel('Bumpiness Value')
	plt.xlabel('Time (seconds)')
	plt.show()

def getCollectedFeatureAggregates(denseFeatures, getFeats):
	print "In getCollectedFeatureAggregates:"
	print "---------------------------------"
	frameAggregates = []
	i = 1
	for feats in denseFeatures:
		print "(" + str(i) +"/" + str(len(denseFeatures)) + ")"
		i += 1
		descriptors, frames = getData(feats, getFeats)
		aggregates = getFeatureAggregates(descriptors,frames,thresholdAgg)
		frameAggregates.extend(aggregates)
	return frameAggregates

def writeDenseFeatures(outputFile, bumpinessAggregate):
	agg = []
	try:
    	with open(filename) as file:
        	agg = np.load(filename)
        	agg = np.stack((agg,addArray[:seconds]))
		except IOError:
			agg = np.asarray(addArray[:seconds])
	np.save(outputFile,agg)

#Get the MBHy/MBHx descriptor.
descriptors, frames = getData(denseFeatures, getFeats)
#Find the bumpiness per frame.
frameAggregates = getFeatureAggregates(descriptors,frames,thresholdAgg)
#Find the bumpiness per second.
bumpinessAggregate = getBumpiness(frameAggregates,thresholdFrames,fps)
#Append the features into the numpy file.
writeDenseFeatures(sys.argv[3],bumpinessAggregate)