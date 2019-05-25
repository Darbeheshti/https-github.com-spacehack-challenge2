import transform
import unittest

import numpy as np
import sys
sys.path.insert(0, '../')


import rotateCorrection as rc


# another crude transformation computer
def _angle(x1, y1, x2, y2):

    # inputs are in angle
    dx = x2 - x1
    dy = y2 - y1
    
    if dy < 0:
        return np.arctan(abs(dy)/dx)
    else:
        return -np.arctan(abs(dy)/dx)

def simple_angle_converter(pointpx, top_right, top_left, bottom_left, bottom_right, imagesize):
    """
    All coordinate tuples are in (x, y) i.e. (lon, lat) convention.
    pointpx (x, y): pixel coordinates counted from top left corner.
    top_right, top_left, bottom_left, bottom_right: (lon, lat) pairs

    imagesize: (width, height) tuple
    """
    # first wrangle inputs
    image_width, image_height  = imagesize
    px, py = pointpx
    tr, tl, bl, br = top_right, top_left, bottom_left, bottom_right
    # now start converting
    image_width_in_lon = (tr[0] - tl[0] + br[0] - bl[0])/2
    image_height_in_lat = (tl[1] - bl[1] + tr[1] - br[1])/2
    
    top_left_lon, top_left_lat = tl
        
    # 2. now convert (px, py) -> (dlon, dlat)
    dlon = px*image_width_in_lon/image_width
    dlat = py*image_height_in_lat/image_height
    
    # compute the angle via simple trig.
    angle_est1 = _angle(tl[0], tl[1], tr[0], tr[1])
    angle_est2 = _angle(bl[0], bl[1], br[0], br[1])
    
    angle = (angle_est1+angle_est2)/2
        
    rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                           [np.sin(angle), np.cos(angle)]])
    
    # apply reverse rotation: x2, y2 (unit: meter)
    x2, y2 = np.dot(rot_matrix, np.array([dlon, dlat]))
        
    # convert x2, y2 to lon, lat
    actual_lon = top_left_lon + x2
    actual_lat = top_left_lat - y2
    
    return actual_lon, actual_lat



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
		res = simple_angle_converter(np.array([0, 0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, top_left))
	
		# check that top right is sane
		res = simple_angle_converter(np.array([width,0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, top_right))

		# check that bottom left is sane
		res = simple_angle_converter(np.array([0,height]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_left))
	
		# check that bottom right is sane
		res = simple_angle_converter(np.array([width,height]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_right))




class TestTransformVectorTransform(unittest.TestCase):
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
		res = rc.vector_converter(np.array([0, 0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, top_left))
	
		# check that top right is sane
		res = rc.vector_converter(np.array([width,0]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, top_right))

		# check that bottom left is sane
		res = rc.vector_converter(np.array([0,height]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_left))
	
		# check that bottom right is sane
		res = rc.vector_converter(np.array([width,height]), top_right, top_left,
			bottom_left, bottom_right, np.array([width, height]))
		self.assertTrue(np.allclose(res, bottom_right))

	def test_fourtyFive_deg(self):
		width = 100
		height = 100

		top_left = np.array([50,50])
		bottom_left = np.array([40,40])
		bottom_right = np.array([50,30])
		top_right = np.array([60,40])

		res = rc.vector_converter((50,50),top_right,top_left, bottom_left, bottom_right, (width,height))
		self.assertTrue(np.allclose(res, (50,40)))

    def test_10_deg(self):
		width = 100
		height = 100

		top_left = np.array([50,50])
		bottom_left = np.array([50,40])
		bottom_right = np.array([60,40])
		top_right = np.array([60,50])

		res = rc.vector_converter((50, 50), top_right, top_left, bottom_left, bottom_right, (width, height))
		self.assertTrue(np.allclose(res, (46.350258, 53.86699865)))


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
