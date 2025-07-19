# encoding: utf-8
"""
Supporting primitive nodes for the pack.
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from . import _meta
from .docstring_formatter import (
	format_docstring as _format_docstring,
	format_object_docstring as _format_object_docstring
)
from .enums import *

# ----------------------------------------------------------

_res_priority_data_type = RoundingPriority.all_values()
_res_priority_data_type_set = set(_res_priority_data_type)
_res_priority_in_type = (
	_res_priority_data_type,
	{
		'default': RoundingPriority.DESIRED.value,
		'tooltip': _format_object_docstring(RoundingPriority),
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
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

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

_up_strategy_data_type = UpscaledCropPadStrategy.all_values()
_up_strategy_data_type_set = set(_up_strategy_data_type)
_up_strategy_in_type = (
	_up_strategy_data_type,
	{
		'default': UpscaledCropPadStrategy.EXACT_UPSCALE.value,
		'tooltip': _format_object_docstring(UpscaledCropPadStrategy),
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
	'strategy' selector for "Upscaled Crop/Pad" node in "Best Resolution" pack.
	"""
	NODE_NAME = 'BestResolutionPrimUpStrategy'
	CATEGORY = _meta.category
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

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
