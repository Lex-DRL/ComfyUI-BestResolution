# encoding: utf-8
"""
Supporting primitive nodes for the pack.
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from . import _meta
from .enums import *

# ----------------------------------------------------------

_res_priority_data_type = RoundingPriority.all_values()
_res_priority_data_type_set = set(_res_priority_data_type)
_res_priority_in_type = (
	_res_priority_data_type,
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
		),
	}
)
_input_types_res_priority = _deepfreeze({
	'required': {
		'priority': _res_priority_in_type,
	},
	# 'hidden': {
	# 	'unique_id': 'UNIQUE_ID',
	# },
	# 'optional': {},
})


def _res_priority_verify(priority: _t.Union[RoundingPriority, str]) -> str:
	if priority not in _res_priority_data_type_set:
		raise ValueError(f"Invalid value for resolution priority: {priority!r}\nExpected one of: {_res_priority_data_type!r}")
	return str(priority)


class BestResolutionPrimResPriority:
	"""
	'priority' selector for "Best Resolution" upscale-nodes.
	"""
	NODE_NAME = 'BestResolutionPrimResPriority'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = False

	FUNCTION = 'main'
	RETURN_TYPES = (_res_priority_data_type, )
	RETURN_NAMES = ('priority', )
	# OUTPUT_TOOLTIPS = ('', )

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_res_priority

	def main(
		self, priority: _t.Union[RoundingPriority, str],
		# show: bool,
		# unique_id: str = None
	):
		return (_res_priority_verify(priority), )

# ----------------------------------------------------------

_up_strategy_data_type = UpscaleTweakStrategy.all_values()
_up_strategy_data_type_set = set(_up_strategy_data_type)
_up_strategy_in_type = (
	_up_strategy_data_type,
	{
		'default': UpscaleTweakStrategy.PAD.value,
		'tooltip': (
			"If the upscaled resolution can't be achieved by uniform scaling of the initial-res, "
			"how to tweak the image to get there:\n\n"
			"• pad - upscale the image to fit it into the desired frame on one side, "
			"then add missing pixels on the other one for outpaint.\n"
			"• crop - upscale the image to fill the entire frame, then crop extra pixels on one side.\n"
			"• nearest - automatically choose one of the above, to crop/pad the least number of pixels.\n"
			"• exact-upscale - follow the provided upscale-value precisely. This is the only option that uses it. "
			"Also, it's the only one that might require both outpainting and crop."
		),
	}
)
_input_types_up_strategy = _deepfreeze({
	'required': {
		'strategy': _up_strategy_in_type,
	},
	# 'hidden': {
	# 	'unique_id': 'UNIQUE_ID',
	# },
	# 'optional': {},
})


def _up_strategy_verify(strategy: _t.Union[RoundingPriority, str]) -> str:
	if strategy not in _up_strategy_data_type_set:
		raise ValueError(f"Invalid value for upscale strategy: {strategy!r}\nExpected one of: {_up_strategy_data_type!r}")
	return str(strategy)


class BestResolutionPrimUpStrategy:
	"""
	'strategy' selector for "Upscale Tweaks" node in "Best Resolution" pack.
	"""
	NODE_NAME = 'BestResolutionPrimUpStrategy'
	CATEGORY = _meta.category
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = False

	FUNCTION = 'main'
	RETURN_TYPES = (_up_strategy_data_type, )
	RETURN_NAMES = ('strategy', )
	# OUTPUT_TOOLTIPS = ('', )

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_up_strategy

	def main(
		self, strategy: _t.Union[RoundingPriority, str],
		# show: bool,
		# unique_id: str = None
	):
		return (_up_strategy_verify(strategy), )
