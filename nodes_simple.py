# encoding: utf-8
"""
Simple (aka no-upscale) versions of nodes.
"""

import typing as _t

from inspect import cleandoc as _cleandoc
from math import sqrt as _sqrt
import sys as _sys

from frozendict import deepfreeze as _deepfreeze

from comfy.comfy_types.node_typing import IO as _IO

from ._funcs import (
	aspect_ratios_sorted as _aspect_ratios_sorted,
	number_to_int as _number_to_int,
	float_width_height_from_area as _float_width_height_from_area,
	simple_result_from_approx_wh as _simple_result_from_approx_wh
)
from . import _meta
from .slot_types import (
	type_dict_res as _type_dict_res,
	type_dict_step_init as _type_dict_step_init
)

# ----------------------------------------------------------

# _return_types_simple = (_IO.INT, _IO.INT, _IO.STRING)
# _return_names_simple = ('width', 'height', 'report')
_return_types_simple = (_IO.INT, _IO.INT)
_return_names_simple = ('width', 'height')

# A tiny optimization by reusing the same immutable dict:
_input_types_simple = _deepfreeze({
	'required': {
		'width': (_IO.INT, dict(_type_dict_res, **{'tooltip': "Approximate width"})),
		'height': (_IO.INT, dict(_type_dict_res, **{'tooltip': "Approximate height"})),
		'step': (_IO.INT, dict(_type_dict_step_init, **{'tooltip': (
			"Both width and height will be divisible by this value - by rounding them "
			"to the closest appropriate resolution.\n\n"
			"The default 48 is (8 * 3 * 2), so it's a safe choice because:\n"
			"- it's compatible with SD1.5/XL downsampling factor (divisible by 8),\n"
			"- it can be upscaled by x1.5 or x1.333 at the first iteration, which is optimal for latent-upscale,\n"
			"- after x1.5 upscale, if you only do x2 later (it's OK for already high resolutions) - it will be divisible "
			"by 3 AND 9, which might become handy at that point, where you'll probably use UltimateSDUpscale.\n\n"
			"Other values worth trying first: 64, 96, 128."
		)})),
		# 'show': (_IO.BOOLEAN, {
		# 	'default': True,
		# 	# 'label_on': 'on', 'label_off': 'off',
		# 	'tooltip': "Show the result on the node itself?",
		# }),
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',  # used for text display at the bottom of the node
	},
	# 'optional': {},
})


class BestResolutionSimple:
	"""
	The simplest node for easier selection of an optimal resolution:
	only rounding performed, desired image size specified directly.
	"""
	NODE_NAME = 'BestResolutionSimple'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_simple
	# OUTPUT_TOOLTIPS = {}
	RETURN_NAMES = _return_names_simple

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_simple

	def main(
		self, width: int, height: int, step: int,
		# show: bool,
		unique_id: str = None
	):
		return _simple_result_from_approx_wh(
			float(width), height, step,
			# show,
			unique_id=unique_id, target_square_size=_sqrt(width * height)
		)

# ----------------------------------------------------------

_tooltip_aspect = (
	"Two aspects together define an aspect ratio (16:9, 4:3, etc).\n"
	"Order doesn't matter: image orientation is defined by the 'landscape' toggle.\n\n"
	"The specified aspect ratio is APPROXIMATE: step parameter has priority over the exact image proportions."
)

_input_types_orient = _deepfreeze({
	'required': {
		'size': (_IO.INT, dict(_type_dict_res, **{'tooltip': (
			"Approximate size of one of the image sides.\nWhich one - see the 'size_is_big' and 'landscape' toggles."
		)})),
		'step': _input_types_simple['required']['step'],
		'size_is_big': (_IO.BOOLEAN, {
			'default': True, 'label_on': 'bigger', 'label_off': 'smaller',
			'tooltip': "When ON, size parameter represents the bigger image side.\nWhen OFF, it specifies the smaller one."
		}),
		'landscape': (_IO.BOOLEAN, {
			'default': True, 'label_on': 'landscape', 'label_off': 'portrait',
			'tooltip': (
				"Specifies image orientation:\n\n"
				"When ON, width is bigger (image is horizontal).\n"
				"When OFF, height is bigger (image is vertical)."
			),
		}),
		'aspect_a': (_IO.FLOAT, {
			'default': 16.0, 'min': 1.0, 'max': _sys.float_info.max, 'step': 1.0, 'round': 0.001,
			'tooltip': _tooltip_aspect
		}),
		'aspect_b': (_IO.FLOAT, {
			'default': 9.0, 'min': 1.0, 'max': _sys.float_info.max, 'step': 1.0, 'round': 0.001,
			'tooltip': _tooltip_aspect
		}),
		# 'show': _input_types_simple['required']['show'],
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',
	},
	# 'optional': {},
})


class BestResolutionFromAspectRatio:
	"""
	A more advanced node for easier selection of an optimal resolution:
	image size selected indirectly - by one of the sides + aspect ratio.
	"""
	NODE_NAME = 'BestResolutionFromAspectRatio'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_simple
	RETURN_NAMES = _return_names_simple

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_orient

	def main(
		self,
		size: int, step: int, size_is_big: bool, landscape: bool, aspect_a: float, aspect_b: float,
		# show: bool,
		unique_id: str = None
	):
		aspect_big, aspect_small = _aspect_ratios_sorted(aspect_a, aspect_b)

		side_main_f = float(size)
		side_other_f = side_main_f * (
			(aspect_small / aspect_big) if size_is_big else (aspect_big / aspect_small)
		)

		width_f, height_f = (side_other_f, side_main_f) if side_other_f > side_main_f else (side_main_f, side_other_f)
		if not landscape:
			# The opposite: height is bigger
			width_f, height_f = height_f, width_f

		return _simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=unique_id, target_square_size=_sqrt(width_f * height_f)
		)

# ----------------------------------------------------------

_input_types_area = _deepfreeze({
	'required': {
		'square_size': (_IO.INT, dict(_type_dict_res, **{'tooltip': (
			"The total resolution of the image would be the same as of a square with this side.\n"
			"The width and height would be such to respect aspect ratio, but also be as close as possible to the "
			"total number of pixels as in this square image.\n\n"
			"- 512x512 square (SD 1.5): ~0.25 megapixels\n"
			"- 1024x1024 square (SDXL): ~1 megapixel"
		)})),
		'step': _input_types_simple['required']['step'],
		'landscape': _input_types_orient['required']['landscape'],
		'aspect_a': _input_types_orient['required']['aspect_a'],
		'aspect_b': _input_types_orient['required']['aspect_b'],
		# 'show': _input_types_simple['required']['show'],
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',
	},
	# 'optional': {},
})


class BestResolutionFromArea:
	"""
	The most efficient way of selecting an optimal resolution:
	image size selected indirectly - by the total desired resolution (area) + aspect ratio.

	Desired resolution (aka image area/megapixels/pixel count) is specified with a side of a square image. This isn't
	accidental: most models disclose what image resolution they're trained on, and usually they're square:

	- SD 1.5 - 512x512 pixels
	- SDXL - 1024x1024 pixels

	By simply providing this single number and setting your aspect ratio/orientation, you get the width and height to
	produce the closest total resolution to the training set, while also respecting image proportions and step-rounding.
	"""
	NODE_NAME = 'BestResolutionFromArea'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_simple
	RETURN_NAMES = _return_names_simple

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_area

	def main(
		self,
		square_size: int, step: int, landscape: bool, aspect_a: float, aspect_b: float,
		# show: bool,
		unique_id: str = None
	):
		square_size: int = _number_to_int(square_size)
		width_f, height_f = _float_width_height_from_area(square_size, landscape, aspect_a, aspect_b)
		return _simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=unique_id, target_square_size=square_size
		)
