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
arg_names = ['code', 'movieName', 'MBHx', 'MBHy', 'labels', 'cluster' 'outputDirectory']
args = dict(zip(arg_names, sys.argv))
Arg_list = collections.namedtuple('Arg_list', arg_names)
args = Arg_list(*(args.get(arg, None) for arg in arg_names))

for (idx,arg) in enumerate(args):
    if arg == None:
        print "Error: "+ arg_names[idx] + " is None."
        print "Correct usage: $python videoGraphs.py movieName MBHx MBHy labels outputDirectory"
        sys.exit()

# Get the movie and output directories
filename = sys.argv[1]
newDirectory = sys.argv[6] + '/'
if not os.path.exists(newDirectory):
    os.makedirs(newDirectory)

# Capture the video and get information
cap = cv2.VideoCapture(filename)
frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))
labels = list(np.load(sys.argv[4]))
print labels

print fps
print frames

# Label sorting
print "Getting clusters"
clusters = np.load(sys.argv[5])
clusters = np.swapaxes(clusters, 0, 1)
x_clusters = clusters[0]
print ("x", x_clusters)
bumplevel = np.argsort(x_clusters, axis=0)
print ("bumplevel", bumplevel)
print "\n"

def concat_images(imga, imgb):
    """
    Combines two color image ndarrays side-by-side.
    """
    print np.array(imgb).shape
    ha,wa = imga.shape[:2]
    hb,wb = np.array(imgb).shape[:2]
    print imga.shape
    print np.array(imgb).shape
    # print np.array(imgb)
    print (ha,wa,hb,wb)
    max_height = np.max([ha, hb])
    total_width = wa+ wb
    new_img = np.zeros(shape=(max_height, total_width, 3), dtype=np.uint8)
    new_img[:ha,:wa]=imga
    imgb_1 = np.delete(imgb, 2, 2)
    new_img[:hb,wa:wa+wb]=np.array(imgb_1)
    return new_img

def getFrameAttributes(i):
    print i
    if len(labels)-1 <= i:
        return False, None, None
    print labels[i]
    if i < 10:
        return False, None, None
    if labels[i] == bumplevel[2]: #bump 2 red = 0
        return True, "Speedbreaker/Bump", (0, 0, 255)
    if labels[i] == bumplevel[0]: #bump 0 blue = 1
        return True, "Turn/Disturbance", (0, 255, 255)
    start = i - 3
    if start < 0:
        start = 0
    end = i + 4
    print "here"
    nbh = labels[start:end]
    print nbh
    if labels[i] == bumplevel[1]: #bump 1 green = 2
        if bumplevel[0] in nbh:
            print "Here 1"
            return True, "Turn/Disturbance", (0, 255, 255)
        else: 
            print "Here 2"
            return True, "Minor Disturbance", (0, 255, 255)
    return False, None, None


fig, ax = plt.subplots(1,1)

y_MBHy = np.load(sys.argv[3])
y_MBHx = np.load(sys.argv[2])
# y_MBHy = [0, 9.922691885676727, 9.711383547802399, 9.776583419233663, 9.805883492579115, 9.610768346134579, 9.138472846510725, 8.724262043067977, 9.799033755717613, 9.936354441315032, 9.465750960344655, 7.499176616861191, 8.91661366426546, 8.05804070263525, 8.512433551813592, 9.195621290780132, 8.145691344913375, 8.463275130845826, 7.767172976651505, 6.225748979987954, 4.846365523733686, 6.036139715430522, 6.928911315448882, 8.175367249209364, 8.918896906850494, 8.73725316551094, 8.688036141057399, 8.820657394184705, 8.454555969160117, 8.816853255669132, 9.068590925276322, 8.93690191166453, 7.438593834121465, 6.429676524857441, 5.37054720253578, 4.79844293748487, 6.833613422543705, 7.694939118063749, 8.267133427917594, 8.460493194411677, 8.407464924346964, 8.224906278620502, 8.315603869810838, 7.83445218469786, 7.160181242513197, 6.929624404368074, 7.626845043141373, 8.285870978280963, 8.793274584610167, 8.984045174627909, 9.446259543916659, 8.80447778782285, 9.377008108247598, 8.659123846268447, 8.595296305945366, 8.69644660768345, 8.113923018401515, 8.666102702973987, 8.47913219415658, 0]
# y_MBHx = [0, 8.808500651552587, 8.61033999571189, 8.771239217161398, 8.653532740903735, 8.687226463768217, 8.682409974043305, 8.638713060488067, 8.642557651391636, 8.80352020679801, 8.317168388176299, 6.462217932365211, 8.548325922428324, 8.616251916953244, 8.75299526614085, 8.647898608617066, 7.583047467190718, 7.1048458081582995, 6.927659758488114, 3.4789005212441215, 2.5484953133906196, 3.2113502045890256, 3.9944056009242335, 6.134321798240827, 8.213506873153742, 8.689070651854003, 8.61169079140941, 8.893422829490627, 8.704445605263622, 8.95404930202718, 8.885287083434134, 8.323483747363836, 6.581570117883163, 5.278872790564537, 3.385903896313347, 3.6410634171719414, 6.277219133414103, 8.421640094320304, 8.39956489824023, 8.33677286273854, 8.43597752062557, 8.192638997635958, 8.24446166045707, 7.818218876862315, 7.377668621194666, 7.244217296417521, 7.8700398921220165, 8.021164534466084, 8.246806194580868, 8.549946917405771, 9.228366492605323, 8.836295370070657, 8.163637828279713, 7.368825668112522, 8.26641185339667, 8.400532283896368, 8.647438435526356, 8.837854486559303, 8.863150632184015, 0]
x_MBHy = range(len(y_MBHy))
x_MBHx = range(len(y_MBHx))

idx = 0
for i in range(frames):
    fig.clf()
    flag, frame = cap.read()
    print i
    if i%fps == 0:
    	idx += 1

    height, width = frame.shape[:2]
    flag1, string, color = getFrameAttributes(idx-1)
    if flag1:
        print string,color
        cv2.putText(frame, string, (width-750, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

    plt.plot(x_MBHy[:idx],y_MBHy[:idx])
    plt.axis([0, 60, 0, 10])

    plt.plot(x_MBHx[:idx],y_MBHx[:idx])
    plt.axis([0, 60, 0, 10])
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
    im.save(newDirectory+"image"+image[-4:]+".jpeg")

    if cv2.waitKey(1) == 27:
        break