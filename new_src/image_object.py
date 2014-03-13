# Library imports
import cv2
import numpy as np

# Local imports
import colors
import top_line_detection as tld


class ImageObject():
	# Variables
	_bgr_img = None
	_binary_court_mask = None
	_dominant_colorset = None
	_gray_flooded2 = None
	# Lines
	_sideline = None
	_baseline = None
	_freethrow_line = None
	_close_paint_line = None
	# Points
	_sideline_baseline = None # The far one in the corner
	_close_paint_baseline = None # Intersection between close paintline and baseline
	_close_paint_freethrow = None # Int btw close paintline and freethrow line
	_sideline_freethrow = None # Int btw far sideline and freethrow line



	def __init__(self, image_name):
		self._bgr_img = cv2.imread(image_name)


	# Exported methods
	def get_binary_court_mask(self):
		if self._binary_court_mask is None:
			d_c = self.get_dominant_colorset()
			self._binary_court_mask = \
				colors.create_court_mask(self.get_bgr_img(), d_c, True)
		return self._binary_court_mask.copy()


	def get_bgr_img(self):
		return self._bgr_img.copy()


	def get_dominant_colorset(self):
		if self._dominant_colorset is None:
			self._dominant_colorset = colors.get_dominant_colorset(self.get_bgr_img())
		return self._dominant_colorset.copy()


	def get_gray_flooded2(self):
		if self._gray_flooded2 is None:
			self._gray_flooded2 = \
				colors.get_double_flooded_mask(self.get_binary_court_mask())
		return self._gray_flooded2.copy()


	def get_sideline(self):
		if self._sideline is None:
			lines = tld.find_top_boundary(self.get_binary_court_mask())
			if len(lines) < 2:
				raise Exception('ERROR: Did not find baseline')
			self._sideline = lines[0]
			self._baseline = lines[1]
		return self._sideline


	def get_baseline(self):
		if self._baseline is None:
			_ = self.get_sideline()
		return self._baseline



if __name__ == '__main__':
	image_root = 'images/5993'
	image_ext = '.jpg'
	image_name = image_root + image_ext
	img_obj = ImageObject(image_name)
	colors.show_image(img_obj.get_gray_flooded2())
