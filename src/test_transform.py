import transform
import unittest

import numpy as np

class TestTransform(unittest.TestCase):
	def test_unrotated_picture(self):
		width = 10
		height = 60
		
		lon_min = 20
		lon_max = 30
		lat_min = 10
		lat_max = 70
		
	
		top_left = np.array([lon_min, lat_max])
		top_right = np.array([lon_max, lat_max])
		bottom_left = np.array([lon_min, lat_min])
		bottom_right = np.array([lon_max, lat_min])
		
		# check that top left is sane
		res = transform.transform(np.array([0, height]), top_right, top_left,
			bottom_left, bottom_right, np.array([height, width]))
		self.assertTrue(np.allclose(res, top_left))
	
		# check that top right is sane
		res = transform.transform(np.array([width,height]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, top_right))

		# check that bottom left is sane
		res = transform.transform(np.array([0,0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_left))
	
		# check that bottom right is sane
		res = transform.transform(np.array([width,0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_right))

#	def test_north_poll_edge_case(self):
#		self.fail()
#
#	def test_south_poll_edge_case(self):
#		self.fail()
#
#	def test_zero_crossing_edge_case(self):
#		self.fail()
#
#	def test_360_crossing_edge_case(self):
#		self.fail()
