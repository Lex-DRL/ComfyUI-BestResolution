# encoding: utf-8
"""
Advanced versions of nodes - with upscale.
"""

import typing as _t

from inspect import cleandoc as _cleandoc
import sys as _sys

from frozendict import deepfreeze as _deepfreeze, frozendict as _frozendict

from comfy.comfy_types.node_typing import IO as _IO

from ._funcs import (
	aspect_ratios_sorted as _aspect_ratios_sorted,
	number_to_int as _number_to_int,
	float_width_height_from_area as _float_width_height_from_area,
	upscale_result_from_approx_wh as _upscale_result_from_approx_wh
)
from . import _meta
from .enums import *
from .nodes_simple import _input_types_area
from .nodes_prims import _res_priority_in_type, _res_priority_verify
from .slot_types import (
	type_dict_step_upscale1 as _type_dict_step_upscale1,
	upscale_in_type as _upscale_in_type
)

# ----------------------------------------------------------

_return_types_upscale = (_IO.FLOAT, _IO.INT, _IO.INT, _IO.INT, _IO.INT, _IO.BOOLEAN)
_return_ttips_upscale = _frozendict({
	'upscale': (
		"If 'needs_resize' is FALSE, this would be the actual uniform value to scale your initial-res in order "
		"to get the upscaled-res.\n"
		"If 'needs_resize' is TRUE, this slot simply outputs the same upscale-value you've set on the node."
	),
	'orig_w': "Width for original/initial image",
	'orig_h': "Height for original/initial image",
	'up_w': "Width for the (main) upscaled image",
	'up_h': "Height for the (main) upscaled image",
	'needs_resize': (
		"This will be FALSE if you can get the exact upscaled resolution by simply scaling the initial-res uniformly "
		"(by the value output into 'upscale' slot).\n\n"
		"Otherwise, it will be TRUE — indicating that you'll need to do some cropping/out-painting right AFTER "
		"the actual upscale (increasing the resolution itself) but BEFORE post-upscale sampling (\"HD-fix\")."
	),
})

__extra_inputs_for_upscale_only = {
	'priority': _res_priority_in_type,
	'upscale': _upscale_in_type,
	'up_step': (_IO.INT, dict(_type_dict_step_upscale1, **{
		'tooltip': "Same as the main `step`, but for the upscaled resolution.",
	})),
}

_input_types_area_upscale = _deepfreeze({
	'required': dict(
		(k_v for k_v in _input_types_area['required'].items() if k_v[0] != 'show'),
		**__extra_inputs_for_upscale_only,
		# show=_input_types_area['required']['show'],
	),
	'hidden': {
		'unique_id': 'UNIQUE_ID',
	},
	# 'optional': {},
})


class BestResolutionFromAreaUpscale:
	"""
	The most efficient way of selecting an optimal resolution:
	image size selected indirectly - by the total desired resolution (area) + aspect ratio...

	... PLUS, account for the immediate upscale right away.

	Desired resolution (aka image area/megapixels/pixel count) is specified with a side of a square image. This isn't
	accidental: most models disclose what image resolution they're trained on, and usually they're square:

	- SD 1.5 - 512x512 pixels
	- SDXL - 1024x1024 pixels

	By simply providing this single number and setting your aspect ratio/orientation, you get the width and height to
	produce the closest total resolution to the training set, while also respecting image proportions and step-rounding.
	"""
	NODE_NAME = 'BestResolutionFromAreaUpscale'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_upscale
	RETURN_NAMES = tuple(_return_ttips_upscale.keys())
	OUTPUT_TOOLTIPS = tuple(_return_ttips_upscale.values())

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_area_upscale

	def main(
		self, square_size: int, step: int, landscape: bool, aspect_a: float, aspect_b: float,
		priority: _t.Union[RoundingPriority, str], upscale: float, up_step:int,
		# show: bool,
		unique_id: str = None
	):
		square_size: int = _number_to_int(square_size)
		width_f, height_f = _float_width_height_from_area(square_size, landscape, aspect_a, aspect_b)
		return _upscale_result_from_approx_wh(
			width_f, height_f, step,
			_res_priority_verify(priority), upscale, up_step,
			# show,
			unique_id=unique_id, target_square_size=square_size
		)
