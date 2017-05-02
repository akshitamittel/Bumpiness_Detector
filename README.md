# Bumpiness Detector

Given a video, use the visual cues to detect the bumpiness of the road along with anomalies.

## Getting Started

The project uses dense-trajectory features ([THOTH](https://lear.inrialpes.fr/people/wang/dense_trajectories)) for extracting visual features.

### Prerequisites

For Dense trajectory features:

```
OpenCV-2.4.2 (python)
ffmpeg-0.11.1
```

For Bumpiness-Detector:

```
sklit-learn-0.18.1 (python)
matplotlib (1.3.1 +)
SciPy
Numpy v1.12
```

### Running the code

The following will provide step by step instructions to collect features and running the bumpiness code.


#### Dense Trajectory features

Assuming you have the [THOTH](https://lear.inrialpes.fr/people/wang/dense_trajectories) software installed, go to the directory: 

```
$ cd dense_trajectory_release_v1.2
```

Run the following code to collect features: 

```
./release/DenseTrack ./path_to_video > /path_to_output_directory/out.features
```

#### The Bumpiness Detector

1. Getting the bumpiness values (use this code twice, to get both the MBHx (feature == 0) and MBHy (feature == 1) :

```
$python bumpiness.py videoName featureFile featureOutputFile feature
```

2. Aggregating the bumpiness across the videos (for both X and Y).

```
$python aggregateBumpiness.py featureOutputFile featureAggregateOutputFile
```

3. Getting the labels of the video through K-means clustering:

```
$python clusterBumpiness.py MBHxFeatures MBHyFeatures labelsOutfile clusterOutfile
```

4. Plotting the graph and labels on the video:

```
$python videoGraphs.py movieName MBHxAggregateFeatures MBHyAggregateFeatures labels outputDirectory
```

5. Go to the output Directory of step 4 and run the following command to get the video named "test.mp4":

```
ffmpeg -r 29 -f image2 -s 1920x1080 -i image%04d.jpeg -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
```


## Running the tests

TODO


### And coding style tests

1. Prerequisites: PyLint

2. Run the following command:

```
$pylint filename.py (eg. bumpiness.py)
```

## Deployment

### Initialization
1. Place the video in the working directory.
2. Place the video sentences in a subdirectory.
Each video sentence should follow the following naming convention:

```
movieStartTime_EndTime.mp4
```

Examples:

```
movie0-10.mp4
movie5-14.mp4

...
movie50-60.mp4
```
### Running the script

1. To run the entire script do:

```
$python script.py make videoSentence_directory video

```
Your video should be in the directory outputVideo with the name test.mp4

2. To clean up after the code is used:

```
$python script.py clean
```

## Authors
1. [Akhita Mittel](https://github.com/akshitamittel) (cs13b1040@iith.ac.in)

2. [Naveen Chedeti](https://github.com/chedeti) (cs13b1010@iith.ac.in)

3. [Prashanth Dewangan](https://github.com/Prashant-Dewangan) (cs13b1025@iith.ac.in)

4. [Anudeepthi Koppula](https://github.com/Anudeepthi) (cs13b1019@iith.ac.in)
