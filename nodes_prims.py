# encoding: utf-8
"""
Supporting primitive nodes for the pack.
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from .enums import *

# ----------------------------------------------------------

_res_priority_data_type = RoundingPriority.all_values()
_res_priority_data_type_set = set(_res_priority_data_type)

# _priority_in_type = (_IO.BOOLEAN, {
# 	'default': True, 'label_on': 'upscaled', 'label_off': 'original',
# 	'tooltip': (
# 		"Which of the resolutions is more important to be as close to the desired as possible:\n\n"
# 		"When ON, the rounded with/height are first calculated for the UPSCALED resolution - and "
# 		"only then the original ones are back-tracked from them.\n"
# 		"When OFF, they're first calculated for the ORIGINAL resolution - and "
# 		"the upscaled ones are tracked forward from them."
# 	)
# })
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
		)
	}
)

_input_types_prim_priority = _deepfreeze({
	'required': {
		'priority': _res_priority_in_type
	},
	# 'hidden': {
	# 	'unique_id': 'UNIQUE_ID',
	# },
	# 'optional': {},
})


class BestResolutionPrimResPriority:
	"""
	'priority' selector for "Best Resolution" upscale-nodes.
	"""
	NODE_NAME = 'BestResolutionPrimResPriority'
	CATEGORY = "utils/resolution"
	DESCRIPTION = _cleandoc(__doc__)

	OUTPUT_NODE = False

	FUNCTION = 'main'
	RETURN_TYPES = (_res_priority_data_type,)
	RETURN_NAMES = ('priority', )
	# OUTPUT_TOOLTIPS = ('', )

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_prim_priority

	def main(
		self, priority: _t.Union[RoundingPriority, str],
		# show: bool,
		# unique_id: str = None
	):
		return (_res_priority_verify(priority), )


def _res_priority_verify(priority: _t.Union[RoundingPriority, str]) -> str:
	if priority not in _res_priority_data_type_set:
		raise ValueError(f"Invalid value for resolution priority: {priority!r}\nExpected one of: {_res_priority_data_type!r}")
	return str(priority)
