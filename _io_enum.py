# encoding: utf-8
"""
Pre-defined combo-inputs for Node-v3, shared between nodes.
"""

from comfy_api.latest import io as _io

from .enums import *
from .docstring_formatter import format_object_docstring as _format_object_docstring


res_priority_in = _io.Combo.Input(
	'priority', options=RoundingPriority.all_values(),
	default=RoundingPriority.ORIGINAL,
	tooltip=_format_object_docstring(RoundingPriority),
)
res_priority_out = _io.Combo.Output(
	# In v3 schema, IDs must be unique between BOTH lists: inputs and outputs, so uppercase ID + `display_name`:
	'PRIORITY', display_name='priority', options=RoundingPriority.all_values(),
)

crop_pad_strategy_in = _io.Combo.Input(
	'strategy', options=UpscaledCropPadStrategy.all_values(),
	default=UpscaledCropPadStrategy.PAD, tooltip=_format_object_docstring(UpscaledCropPadStrategy)
)
crop_pad_strategy_out = _io.Combo.Output(
	'STRATEGY', display_name='strategy', options=UpscaledCropPadStrategy.all_values(),
)
