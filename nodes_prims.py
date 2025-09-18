# encoding: utf-8
"""
Supporting primitive nodes for the pack.
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from comfy_api.latest import io as _io

from . import _io_enum as _enums
from . import _meta
from .docstring_formatter import format_docstring as _format_docstring

# ----------------------------------------------------------

class BestResolutionPrimResPriority(_io.ComfyNode):
	"""
	'priority' selector for "Best Resolution" upscale-nodes.
	"""
	_schema = _io.Schema(
		'BestResolutionPrimResPriority',
		display_name="Priority (Best-Res)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[_enums.res_priority_in],

		outputs=[_enums.res_priority_out],

		is_output_node=False,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls, priority: _t.Union[_enums.RoundingPriority, str],
		# show: bool,
		# unique_id: str = None
	) -> _io.NodeOutput:
		return _io.NodeOutput(_enums.RoundingPriority.validate(priority), )

# ----------------------------------------------------------

class BestResolutionPrimCropPadStrategy(_io.ComfyNode):
	"""
	'strategy' selector for "Upscaled Crop/Pad" node in "Best Resolution" pack.
	"""
	_schema = _io.Schema(
		'BestResolutionPrimCropPadStrategy',
		display_name="Crop-Pad Strategy (Best-Res)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[_enums.crop_pad_strategy_in],

		outputs=[_enums.crop_pad_strategy_out],

		is_output_node=False,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls, strategy: _t.Union[_enums.UpscaledCropPadStrategy, str],
		# show: bool,
		# unique_id: str = None
	) -> _io.NodeOutput:
		return _io.NodeOutput(_enums.UpscaledCropPadStrategy.validate(strategy), )
