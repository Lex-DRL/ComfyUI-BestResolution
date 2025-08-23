# encoding: utf-8
"""
Pre-defined combo-inputs for Node-v3, shared between nodes.
"""

from comfy_api.latest import io as _io

from .enums import *
from .docstring_formatter import format_object_docstring as _format_object_docstring


res_priority_in = _io.Combo.Input(
	"priority", options=RoundingPriority.all_values(),
	default=RoundingPriority.ORIGINAL,
	tooltip=_format_object_docstring(RoundingPriority)
)
# res_priority_out = _io.Combo
crop_pad_strategy_in = _io.Combo.Input(
	"strategy", options=UpscaledCropPadStrategy.all_values(),
	default=UpscaledCropPadStrategy.PAD, tooltip=_format_object_docstring(UpscaledCropPadStrategy)
)
