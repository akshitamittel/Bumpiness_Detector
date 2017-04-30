import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

x_data = np.load('Movie1/MBHxAggFeatures.npy')
y_data = np.load('Movie1/MBHyAggFeatures.npy')
bach = 3

def f(x, num, den):
	return x * 1.0 * num / den

f = np.vectorize(f)

def loadData(x_data,y_data):
	x = x_data
	y = y_data
	x_data = np.delete(x_data,0,0)
	x_data = np.delete(x_data,len(x_data)-1,0)
	y_data = np.delete(y_data,0,0)
	y_data = np.delete(y_data,len(y_data)-1,0)
	# x_cond = all(elem <= 8 for elem in x_data.tolist())
	# y_cond = all(elem <= 8 for elem in y_data.tolist())
	# print (x_cond, y_cond)
	# print x_data
	# if x_cond and y_cond:
	# 	print max(x_data)
	# 	x_data = f(x_data, 9, 7)
	# 	y_data = f(y_data, 9, 7)
	# 	print x_data
	X = np.asarray([x_data.tolist(), y_data.tolist()])
	X = np.swapaxes(X,0,1)
	return X, x, y

def kMeans(X,i):
	kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
	# if i == 0:
	# 	np.save("kmeans.npy", kmeans)
	labels = list(kmeans.labels_)
	clusters = list(kmeans.cluster_centers_)
	labels.insert(0, -1)
	labels.append(-1)
	X = np.vstack((np.asarray([0,0]),X))
	X = np.vstack((X,np.asarray([0,0])))
	print labels
	print len(labels)
	return clusters, labels, X

def plot_kMeans(X,labels):
	for (idx,i) in enumerate(X):
		if labels[idx] == 0:
			# print str(idx) + " :0 Here"
			plt.scatter(i[0],i[1],c='r',marker='o')
		elif labels[idx] == 1:
			# print str(idx) + " :1 Here"
			plt.scatter(i[0],i[1],c='b',marker='o')
		elif labels[idx] == 2:
			# print str(idx) + " :2 Here"
			plt.scatter(i[0],i[1],c='g',marker='o')
	plt.show()


def smoothen(elem, idx, arr, rng):
	start = idx - rng
	if start < 0:
		start = 0
	end = idx + rng
	arr1 = arr[start:end]
	return sum(arr1)*1.0/len(arr1)

#Error: Append -1 to end and begining of labels.
def smoothenPlot(x, y, labels):
	x_data = []
	y_data = []
	for (idx,i) in enumerate(labels):
		if i == 1:
			x_data.append(smoothen(x[idx],idx,x,3))
			y_data.append(smoothen(y[idx],idx,y,3))
		elif i == 2: 
			x_data.append(smoothen(x[idx],idx,x,2))
			y_data.append(smoothen(y[idx],idx,y,2))
		else:
			x_data.append(x[idx])
			y_data.append(y[idx])
	return x_data, y_data

def plot_Bumpiness(x,y):
	plt.clf()
	x = np.asarray(x)
	y = np.asarray(y)
	x_axis = range(len(x))
	plt.plot(x_axis,x)
	plt.plot(x_axis,y)
	plt.axis([0, 60, 0, 10])
	plt.show()

for i in range(bach):
	X, MBHx, MBHy = loadData(x_data,y_data)
	print ("kMeans", i)
	clusters, labels, X = kMeans(X,i)
	if i == 0:
		np.save("Movie1/labels.npy", labels)
		np.save("Movie1/clusters.npy", clusters)
		print ("cluster centres", clusters)
	plot_kMeans(X,labels)
	print("smoothen", i)
	x, y = smoothenPlot(MBHx.tolist(), MBHy.tolist(), labels)
	x_data = np.asarray(x)
	y_data = np.asarray(y)
	plot_Bumpiness(x,y)