import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image
from cStringIO import StringIO
import os
import sys
import collections


## Get user inputs and check if they are entered correctly
parser = argparse.ArgumentParser()
parser.add_argument("--movieName", default="Movie1.mp4")
parser.add_argument("--MBHx", default="MBHxAggFeatures.npy")
parser.add_argument("--MBHy", default="MBHyAggFeatures.npy")
parser.add_argument("--labelFile", default="labels.npy")
parser.add_argument("--clusterFile", default="clusters.npy")
parser.add_argument("--outputDirectory", default="outputVideo")
parser.add_argument("--environ", default="test")
args = parser.parse_args()

def concat_images(imga, imgb):
    """
    Combines two color image ndarrays side-by-side.
    """
    print np.array(imgb).shape
    ha,wa = imga.shape[:2]
    hb,wb = np.array(imgb).shape[:2]
    print imga.shape
    print np.array(imgb).shape
    print (ha,wa,hb,wb)
    max_height = np.max([ha, hb])
    total_width = wa+ wb
    new_img = np.zeros(shape=(max_height, total_width, 3), dtype=np.uint8)
    new_img[:ha,:wa]=imga
    imgb_1 = np.delete(imgb, 2, 2)
    new_img[:hb,wa:wa+wb]=np.array(imgb_1)
    return new_img

def getFrameAttributes(i):
    '''
    Attributes frame labels based on the K-means label provided to it and its neighbouring frames.
    '''
    print i
    #These labels occur at the beginning and end of the video
    if len(labels)-1 <= i:
        return False, None, None
    print labels[i]
    # The features are not stable during the first few seconds of the video.
    if i < 10:
        return False, None, None
    # If the turbulence is high there is either a speedbreaker or bump
    if labels[i] == bumplevel[2]: 
        return True, "Speedbreaker/Bump", (0, 0, 255)
    if labels[i] == bumplevel[0]:
    # If there is a great disparity between the MBHy & MBHx values (disturbance in the x and y-axis)
    # then there is either a turn or a vehicle coming in proximity.
        return True, "Turn/Disturbance", (0, 255, 255)
    start = i - 3
    if start < 0:
        start = 0
    end = i + 4
    nbh = labels[start:end]
    print nbh
    #If the cluster label is between a turn or turbulence we need to check for two conditions:
    # 1. The motion is a part of a turn
    # 2. The motion is regular or there is a minor disturbance.
    if labels[i] == bumplevel[1]: 
        if bumplevel[0] in nbh:
            return True, "Turn/Disturbance", (0, 255, 255)
        else: 
            return True, "Minor Disturbance", (0, 255, 255)
    return False, None, None

if args.environ == "dep":
    # Get the movie and output directories
    filename = args.movieName
    newDirectory = args.outputDirectory + '/'
    if not os.path.exists(newDirectory):
        os.makedirs(newDirectory)

    # Capture the video and get information
    cap = cv2.VideoCapture(filename)
    frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))
    labels = list(np.load(args.labelFile))
    print labels

    print fps
    print frames

    # Label sorting
    print "Getting clusters"
    clusters = np.load(args.clusterFile)
    clusters = np.swapaxes(clusters, 0, 1)
    x_clusters = clusters[0]
    print ("x", x_clusters)
    bumplevel = np.argsort(x_clusters, axis=0)
    print ("bumplevel", bumplevel)
    print "\n"

    fig, ax = plt.subplots(1,1)

    y_MBHy = np.load(args.MBHy)
    y_MBHx = np.load(args.MBHx)
    x_MBHy = range(len(y_MBHy))
    x_MBHx = range(len(y_MBHx))

    idx = 0
    for i in range(frames):
        fig.clf()
        flag, frame = cap.read()
        print i
        if i%fps == 0:
        	idx += 1

        # Put the labels according to the attributes.
        height, width = frame.shape[:2]
        flag1, string, color = getFrameAttributes(idx-1)
        if flag1:
            print string,color
            cv2.putText(frame, string, (width-750, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

        #Prepare the graph
        plt.plot(x_MBHy[:idx],y_MBHy[:idx])
        plt.axis([0, 60, 0, 10])
        plt.plot(x_MBHx[:idx],y_MBHx[:idx])
        plt.axis([0, 60, 0, 10])    
        ax.set_xlabel('time')
        ax.set_ylabel('MBHy/MBHx (Bumpiness Estimate)')
        #Convert a plot into an image
        buffer_ = StringIO()
        plt.savefig(buffer_, format = "png")
        buffer_.seek(0)
        graph = PIL.Image.open(buffer_)
        #Concactenate images
        img = concat_images(frame,graph)
        buffer_.close()
        image = "000"
        image += str(i+1)
        im = Image.fromarray(img)
        #Save the image in the directory provided.
        im.save(newDirectory+"image"+image[-4:]+".jpeg")

        if cv2.waitKey(1) == 27:
            break