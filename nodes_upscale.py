# encoding: utf-8
"""
Advanced versions of nodes - with upscale.
"""

import typing as _t

from inspect import cleandoc as _cleandoc
from math import sqrt as _sqrt
import sys as _sys

from frozendict import deepfreeze, frozendict

from comfy.comfy_types.node_typing import IO as _IO

from ._funcs import (
	aspect_ratios_sorted as _aspect_ratios_sorted,
	number_to_int as _number_to_int,
	float_width_height_from_area as _float_width_height_from_area,
	simple_result_from_approx_wh as _simple_result_from_approx_wh,
	upscale_result_from_approx_wh as _upscale_result_from_approx_wh
)
from .enums import *
from .node_types import *
from .nodes_simple import _input_types_area

# ----------------------------------------------------------

_return_types_upscale = (_IO.INT, _IO.INT, _IO.INT, _IO.INT)
_return_ttips_upscale = frozendict({
	'orig_w': "Width for original image",
	'orig_h': "Height for original image",
	'up_w': "Width for upscaled image",
	'up_h': "Height for upscaled image"
})
_return_names_upscale = tuple(_return_ttips_upscale.keys())





# __priority_type = (_IO.BOOLEAN, {
# 	'default': True, 'label_on': 'upscaled', 'label_off': 'original',
# 	'tooltip': (
# 		"Which of the resolutions is more important to be as close to the desired as possible:\n\n"
# 		"When ON, the rounded with/height are first calculated for the UPSCALED resolution - and "
# 		"only then the original ones are back-tracked from them.\n"
# 		"When OFF, they're first calculated for the ORIGINAL resolution - and "
# 		"the upscaled ones are tracked forward from them."
# 	)
# })
__priority_type = (
	RoundingPriority.all_values(),
	{
		'default': RoundingPriority.DESIRED.value,
		'tooltip': (
			"Defines what resolution to prioritize, as well as which order to perform rounding in:\n\n"
			"• desired - first, approximate resolutions are calculated for both initial and upscaled size; "
			"then, both are rounded. In both cases, the rounded resolution is closest to the desired one, "
			"but aspect ratio might differ the most between sizes.\n\n"
			"• original - first, initial resolution is calculated and rounded; then, upscaled one is detected from it. "
			"Upscaled resolution might differ the most from the desired aspect ratio, but it follows the ratio from "
			"initial size as much as possible.\n\n"
			"• upscaled - vice versa: first, the rounded upscaled resolution is calculated; then, the initial one "
			"back-tracked from it."
		)
	}
)
__extra_inputs_for_upscale_only = {
	'priority': __priority_type,
	'upscale': (_IO.FLOAT, {
		'default': 1.5, 'min': 1.0, 'max': _sys.float_info.max, 'step': 0.25, 'round': 0.001,
		# 'tooltip': "",  # TODO
	}),
	'up_step': (_IO.INT, dict(type_dict_step_upscale1, **{
		'tooltip': "Same as the main `step`, but for the upscaled resolution.",
	})),
}

_input_types_area_upscale = deepfreeze({
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
	NODE_NAME = 'BestResolutionFromAreaUpscale'
	CATEGORY = "utils/resolution"
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_upscale
	RETURN_NAMES = _return_names_upscale
	RETURN_TYPES_TOOLTIPS = _return_ttips_upscale

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
			priority, upscale, up_step,
			# show,
			unique_id=unique_id, target_square_size=square_size
		)
