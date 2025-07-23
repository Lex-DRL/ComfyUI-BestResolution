# encoding: utf-8
"""
"""

import typing as _t

from inspect import cleandoc as _cleandoc
from math import sqrt as _sqrt

from frozendict import deepfreeze as _deepfreeze

from comfy.comfy_types.node_typing import IO as _IO

from ._funcs import simple_result_from_approx_wh as _simple_result_from_approx_wh
from . import _meta
from .docstring_formatter import format_docstring as _format_docstring
from .slot_types import (
	type_dict_res as _type_dict_res,
	type_dict_step_default as _type_dict_step_default,
	upscale_in_type as _upscale_in_type
)

_return_types = (_IO.INT, _IO.INT, _IO.FLOAT)
_return_names = ('width', 'height', 'scale')
_scale_type_dict = {k: v for k, v in _upscale_in_type[1].items() if k != 'tooltip'}
_scale_type_dict['min'] = 0.001

_input_types = _deepfreeze({
	'required': {
		'width': (_IO.INT, _type_dict_res),
		'height': (_IO.INT, _type_dict_res),
		'step': (_IO.INT, _type_dict_step_default),
		'scale': (_IO.FLOAT, _scale_type_dict),
		'direction': (_IO.BOOLEAN, {'default': True, 'label_on': 'res * scale', 'label_off': 'res / scale', 'tooltip': (
			"Sometimes it's easier to specify scale by it's inverse: how much to scale DOWN by. This toggle controls that."
		)}),
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',  # used for text display at the bottom of the node
	},
})


class BestResolutionScale:
	"""
	Scale width and height by the same value + round them.
	"""
	NODE_NAME = 'BestResolutionScale'
	CATEGORY = _meta.category
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types
	RETURN_NAMES = _return_names

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types

	@staticmethod
	def main(
		width: int, height: int, step: int, scale: float, direction: bool,
		# show: bool,
		unique_id: str = None
	) -> _t.Tuple[int, int, float]:
		scale = float(scale)
		if not direction:
			scale = 1.0 / scale
		width_f = scale * width
		height_f = scale * height
		out_width, out_height = _simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=unique_id, target_square_size=_sqrt(width_f * height_f),
			status_suffix=f"\n({width}/{height}) * {scale:.3f} scale"
		)
		return out_width, out_height, scale
