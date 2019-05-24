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
		
	
		top_left = (lon_min, lat_max)
		top_right = (lon_max, lat_max)
		bottom_left = (lon_min, lat_min)
		botom_right = (lon_max, lat_min)
		
		# check that top left is sane
		res = transform.transform((0,0), top_left, top_right,
			lower_left, lower_right, width, height)
		self.assertTrue(np.allclose(res, [lon_min, lat_max]))
	
		# check that top right is sane
		res = transform.transform((0, width), top_right, top_left,
			lower_left, lower_right, width, height)
		self.assertTrue(np.allclose(res, [lon_max, lat_max]))

		# check that bottom left is sane
		res = transform.transform((height,0), top_left, top_right,
			lower_left, lower_right, width, height)
		self.assertTrue(np.allclose(res, [lon_min, lat_min]))
	
		# check that bottom right is sane
		res = transform.transform((height, width), top_right, top_left,
			lower_left, lower_right, width, height)
		self.assertTrue(np.allclose(res, [lon_max, lat_min]))

	def test_north_poll_edge_case(self):
		self.fail()

	def test_south_poll_edge_case(self):
		self.fail()

	def test_zero_crossing_edge_case(self):
		self.fail()

	def test_360_crossing_edge_case(self):
		self.fail()
