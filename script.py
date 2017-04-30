import subprocess
import os
import sys

def getFeatures(dirName, movie):
	for filename in os.listdir(dirName + "/" + movie):
		if not image.endswith(".mp4"):
			continue
		movieName = "/" + dirName + "/" + movie + "/" + filename
		featureName = "/" + dirName + "/features/" + filename[5:-4] + ".features"
		cmd = "./release/DenseTrack " + movieName + " > " + featureName
		subprocess.call(cmd, cwd="dense_trajectory_release_v1.2", shell=True)
		print "Collected features for file: " + filename

def getMBHfeatures(dirName, movie):
	for filename in os.listdir(dirName + "/" + movie):
		if not image.endswith(".mp4"):
			continue
		number = filename[5:-4]
		featureName = number + ".features"
		subprocess.check_call(['python', 'bumpiness.py', featureName, filename, "MBHxFeatures.npy", "0"])
		subprocess.check_call(['python', 'bumpiness.py', featureName, filename, "MBHyFeatures.npy", "1"])

def getMBHAggregate():
	subprocess.check_call(['python', 'aggregateBumpiness.py', "MBHxFeatures.npy", "MBHxAggFeatures.npy"])
	subprocess.check_call(['python', 'aggregateBumpiness.py', "MBHyFeatures.npy", "MBHyAggFeatures.npy"])

def make(movie):
	#Get the features in the features file
	if not os.path.exists("features"):
    	os.makedirs("features")
    dirName = os.path.dirname(os.path.abspath(__file__))
    getFeatures(dirName, movie)
    #Get MBHx and MBHy features
    getMBHfeatures(dirName, movie)
    #Get aggregate MBH features
    getMBHAggregate()
    #Get k-means labels and clusters
    subprocess.check_call(['python', 'clusterBumpiness.py', "MBHxAggFeatures.npy", "MBHyAggFeatures.npy", "labels.npy", "clusters.npy"])
    #Get video labels
    if not os.path.exists("outputVideo"):
    	os.makedirs("outputVideo")
    subprocess.check_call(['python', 'videoGraphs.py', sys.argv[3], "MBHxAggFeatures.npy", "MBHyAggFeatures.npy", "labels.npy", "clusters.npy", "outputVideo"])
    #Make video
    subprocess.call('ffmpeg -r 29 -f image2 -s 1920x1080 -i image%04d.jpeg -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4', cwd="outputVideo", shell=True)

def clean():
	subprocess.call('rm -r features', shell=True)
	subprocess.call('rm -r outputVideo', shell=True)
	subprocess.call('rm MBHxFeatures.npy', shell=True)
	subprocess.call('rm MBHyFeatures.npy', shell=True)
	subprocess.call('rm MBHxAggFeatures.npy', shell=True)
	subprocess.call('rm MBHyAggFeatures.npy', shell=True)
	subprocess.call('rm labels.npy', shell=True)
	subprocess.call('rm clusters.npy', shell=True)

if sys.argv[1] == "make":
	make(sys.argv[2])
elif sys.argv[1] == "clean":
	clean()
else:
	print "Invalid command, see use of script:"
	print "$python script.py make movieDirectory movieName"
	print "$python script.py clean"