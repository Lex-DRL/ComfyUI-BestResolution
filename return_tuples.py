# encoding: utf-8
"""
For readability, the results of all node-functions in this node pack are NamedTuples instead of regular tuples.
"""

import typing as _t


class ResultSimple(_t.NamedTuple):
	"""Returned NamedTuple for simple (non-upscale) nodes."""
	width: int
	height: int


class ResultUpscaled(_t.NamedTuple):
	"""Returned NamedTuple for nodes with upscaling."""
	upscale: float
	init_width: int
	init_height: int
	hd_width: int
	hd_height: int


class ResultUpscaledCropPad(_t.NamedTuple):
	"""Returned NamedTuple for "Upscaled Crop/Pad" node."""
	upscale: float

	do_crop: bool
	crop_width: int
	crop_height: int
	crop_x_origin: int
	crop_y_origin: int

	do_padding: bool
	pad_left: int
	pad_top: int
	pad_right: int
	pad_bottom: int
