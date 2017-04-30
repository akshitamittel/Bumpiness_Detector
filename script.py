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
		cmd_y =  "python bumpiness.py --videoName=" + filename + " --featureFile=" + featureName + " --featureOutputFile==MBHyFeatures.npy --feature=0 --environ=dep"
		cmd_x =  "python bumpiness.py --videoName=" + filename + " --featureFile=" + featureName + " --featureOutputFile==MBHxFeatures.npy --feature=1 --environ=dep"
		subprocess.check_call([cmd_y], shell=True)
		subprocess.check_call([cmd_x], shell=True)

def getMBHAggregate():
	cmd_y = "python aggregateBumpiness.py --featureFile=MBHyFeatures.npy --outputFile=MBHyAggFeatures.npy --environ=dep"
	cmd_x = "python aggregateBumpiness.py --featureFile=MBHxFeatures.npy --outputFile=MBHxAggFeatures.npy --environ=dep"
	subprocess.check_call([cmd_y], shell=True)
	subprocess.check_call([cmd_x], shell=True)

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
    cmd = "python clusterBumpiness.py --MBHx=MBHxAggFeatures.npy --MBHy=MBHyAggFeatures.npy --labelFile=labels.npy --clusterOutfile=clusters.npy --environ=dep"
    subprocess.check_call([cmd], shell=True)
    #Get video labels
    if not os.path.exists("outputVideo"):
    	os.makedirs("outputVideo")
    cmd = "python videoGraphs.py --movieName=" + sys.argv[3] + " --MBHx=MBHxAggregateFeatures.npy --MBHy=MBHyAggregateFeatures.npy --labelFile=labels.npy --outputDirectory=outputVideo --environ=dep"
    subprocess.check_call([cmd], shell=True)
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