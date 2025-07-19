# encoding: utf-8
"""
Nodes to calculate crop / padding values (for out-paint).
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze, frozendict as _frozendict

from comfy.comfy_types.node_typing import IO as _IO

from ._funcs_crop_pad import upscaled_crop_pad as _upscaled_crop_pad
from . import _meta
from .docstring_formatter import format_docstring as _format_docstring
from .enums import *
from .nodes_prims import _up_strategy_in_type, _up_strategy_verify
from .nodes_upscale import _return_ttips_upscale
from .slot_types import (
	type_dict_res as _type_dict_res,
	rel_pos_in_type as _rel_pos_in_type,
	upscale_in_type as _upscale_in_type
)

# ----------------------------------------------------------

_return_types_crop_pad = (
	_IO.FLOAT,
	_IO.BOOLEAN, _IO.INT, _IO.INT, _IO.INT, _IO.INT,
	_IO.BOOLEAN, _IO.INT, _IO.INT, _IO.INT, _IO.INT,
)
_return_ttips_crop_pad = _frozendict({
	'upscale': "The actual uniform upscale value to do.",

	'do_crop': "Whether post-upscale crop needs to be done to get the specified resolution.",
	'crop_width': "Width for the post-upscale crop.",
	'crop_height': "Height for the post-upscale crop.",
	'crop_x': "X-offset for the post-upscale crop.",
	'crop_y': "Y-offset for the post-upscale crop.",

	'do_padding': "Whether post-upscale padding and out-paint need to be done to get the specified resolution.",
	'pad_left': "Left padding for the post-upscale out-paint.",
	'pad_top': "Top padding for the post-upscale out-paint.",
	'pad_right': "Right padding for the post-upscale out-paint.",
	'pad_bottom': "Bottom padding for the post-upscale out-paint.",
})
_input_types_crop_pad = _deepfreeze({
	'required': {
		'upscale': (_IO.FLOAT, dict(_upscale_in_type[1], **{
			'tooltip': f"Only used when {UpscaledCropPadStrategy.EXACT_UPSCALE!r} strategy selected."
		})),
		'init_width': (_IO.INT, dict(_type_dict_res, **{'tooltip': _return_ttips_upscale['init_width']})),
		'init_height': (_IO.INT, dict(_type_dict_res, **{'tooltip': _return_ttips_upscale['init_height']})),
		'HD_width': (_IO.INT, dict(_type_dict_res, **{'tooltip': _return_ttips_upscale['HD_width'], 'default': 1536})),
		'HD_height': (_IO.INT, dict(_type_dict_res, **{'tooltip': _return_ttips_upscale['HD_height'], 'default': 1536})),
		'strategy': _up_strategy_in_type,
		'align_x': (_IO.FLOAT, dict(_rel_pos_in_type[1], **{
			'tooltip': (
				"Where's the image pivot for horizontal alignment (which side stays in place during crop/out-paint):\n"
				"0 - Left\n"
				"0.5 - Center\n"
				"1 - Right"
			),
		})),
		'align_y': (_IO.FLOAT, dict(_rel_pos_in_type[1], **{
			'tooltip': (
				"Where's the image pivot for vertical alignment (which side stays in place during crop/out-paint):\n"
				"0 - Bottom\n"
				"0.5 - Center\n"
				"1 - Top"
			),
			'default': 0.0
		})),
	},
	'hidden': {
		'unique_id': 'UNIQUE_ID',
	},
	# 'optional': {},
})


class BestResolutionUpscaledCropPad:
	"""
	If the original resolution can't be scaled to the higher one uniformly (i.e., without stretching),
	this node detects the appropriate values for cropping/out-painting.
	"""
	NODE_NAME = 'BestResolutionUpscaledCropPad'
	CATEGORY = _meta.category
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

	OUTPUT_NODE = True

	FUNCTION = 'main'
	RETURN_TYPES = _return_types_crop_pad
	RETURN_NAMES = tuple(_return_ttips_crop_pad.keys())
	OUTPUT_TOOLTIPS = tuple(_return_ttips_crop_pad.values())

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_crop_pad

	def main(
		self,
		upscale: float,
		init_width: int, init_height: int, HD_width: int, HD_height: int,
		strategy: _t.Union[UpscaledCropPadStrategy, str],
		align_x: float, align_y: float,
		# show: bool,
		unique_id: str = None
	):
		return _upscaled_crop_pad(
			upscale,
			init_width, init_height, HD_width, HD_height,
			_up_strategy_verify(strategy),
			align_x, align_y,
			# show,
			unique_id=unique_id
		)
