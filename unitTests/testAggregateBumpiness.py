import sys
sys.path.insert(0, '/Users/Akshita/Desktop/Applications/Codes/Bumpiness_Detector/')
import numpy as np
from aggregateBumpiness import createCollection, aggregate, scaleAggregates
import unittest

class TestAggregateBumpiness(unittest.TestCase):

	def test_createCollection(self):
		#Create testing data
		a = range(11)
		b = range(12)
		c = range(10)
		reality = [a, b]
		test = [c, c]
		#Test for null case
		self.assertEquals(createCollection(np.empty(0)),[])
		#Test with testing data
		self.assertEquals(createCollection(reality), test)

	def test_aggregate(self):
		#Create testing data
		a = range(10)
		reality = [a, a]
		test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9]
		#Test for null case
		self.assertEquals(aggregate(np.empty(0)), [])
		#Test with testing data
		self.assertEquals(aggregate(reality), test)

	def test_scaleAggregates(self):
		#Create testing data
		test = [0, 375.0, 775.0, 1175.0, 1575.0, 1975.0, 2375.0, 2775.0, 3175.0, 3575.0]
		reality = range(10)
		#Test for null case
		self.assertEquals(scaleAggregates(np.empty(0)), None)
		#Test with testing data
		self.assertEquals(scaleAggregates(reality), test)

if __name__ == '__main__':
	unittest.main()