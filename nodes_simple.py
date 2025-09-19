# encoding: utf-8
"""
Simple (aka no-upscale) versions of nodes.
"""

from inspect import cleandoc as _cleandoc
from math import sqrt as _sqrt

from comfy_api.latest import io as _io

from . import _io_simple as _i
from ._io_simple import _io_override
from . import _meta
from . import _tooltips as _tt
from .__docstring_formatter import format_docstring as _format_docstring
from .funcs import (
	aspect_ratios_sorted as _aspect_ratios_sorted,
	number_to_int as _number_to_int,
	float_width_height_from_area as _float_width_height_from_area,
	simple_result_from_approx_wh as _simple_result_from_approx_wh
)

# ----------------------------------------------------------

class BestResolutionSimple(_io.ComfyNode):
	"""
	The simplest node for easier selection of an optimal resolution:
	only rounding performed, desired image size specified directly.
	"""
	_schema = _io.Schema(
		'BestResolutionSimple',
		display_name="Best-Res (simple)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),

		inputs=[
			_io_override(_i.res, 'width', tooltip="Approximate width"),
			_io_override(_i.res, 'height', tooltip="Approximate height"),
			_io_override(_i.step_init, 'step'),
		],

		hidden=[_io.Hidden.unique_id],

		outputs=[
			_io.Int.Output('WIDTH', display_name='width'),
			_io.Int.Output('HEIGHT', display_name='height'),
		],

		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		width: int, height: int, step: int,
		# show: bool,
	) -> _io.NodeOutput:
		return _io.NodeOutput(*_simple_result_from_approx_wh(
			float(width), height, step,
			# show,
			unique_id=cls.hidden.unique_id, target_square_size=_sqrt(width * height)
		))

# ----------------------------------------------------------

class BestResolutionFromAspectRatio(_io.ComfyNode):
	"""
	A more advanced node for easier selection of an optimal resolution:
	image size selected indirectly - by one of the sides + aspect ratio.
	"""
	_schema = _io.Schema(
		'BestResolutionFromAspectRatio',
		display_name="Best-Res (ratio)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),

		inputs=[
			_io_override(_i.res, 'size', tooltip=_tt.size_one_side),
			_io_override(_i.step_init, 'step'),
			_i.toggle_size_is_big,
			_i.toggle_landscape,
			_i.aspect_a,
			_i.aspect_b,
		],

		hidden=[_io.Hidden.unique_id],

		outputs=list(BestResolutionSimple._schema.outputs),

		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		size: int, step: int, size_is_big: bool, landscape: bool, aspect_a: float, aspect_b: float,
		# show: bool,
	) -> _io.NodeOutput:
		aspect_big, aspect_small = _aspect_ratios_sorted(aspect_a, aspect_b)

		side_main_f = float(size)
		side_other_f = side_main_f * (
			(aspect_small / aspect_big) if size_is_big else (aspect_big / aspect_small)
		)

		width_f, height_f = (side_other_f, side_main_f) if side_other_f > side_main_f else (side_main_f, side_other_f)
		if not landscape:
			# The opposite: height is bigger
			width_f, height_f = height_f, width_f

		return _io.NodeOutput(*_simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=cls.hidden.unique_id, target_square_size=_sqrt(width_f * height_f)
		))

# ----------------------------------------------------------

class BestResolutionFromArea(_io.ComfyNode):
	"""
	The most efficient way of selecting an optimal resolution:
	image size selected indirectly - by the total desired resolution (area) + aspect ratio.


	Desired resolution (aka image area/megapixels/pixel count) is specified with a side of a square image. This isn't
	accidental: most models disclose what image resolution they're trained on, and usually they're square:
	- SD 1.5 - 512x512 pixels
	- SDXL - 1024x1024 pixels


	By simply providing this single number and setting your aspect ratio/orientation, you get the width and height to
	produce the closest total resolution to the training set, while also respecting image proportions and step-rounding.
	"""
	_schema = _io.Schema(
		'BestResolutionFromArea',
		display_name="Best-Res (area)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),

		inputs=[
			_io_override(_i.res, 'square_size', tooltip=_tt.size_square),
			_io_override(_i.step_init, 'step'),
			_i.toggle_landscape,
			_i.aspect_a,
			_i.aspect_b,
		],

		hidden=[_io.Hidden.unique_id],

		outputs=list(BestResolutionSimple._schema.outputs),

		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		square_size: int, step: int, landscape: bool, aspect_a: float, aspect_b: float,
		# show: bool,
	) -> _io.NodeOutput:
		square_size: int = _number_to_int(square_size)
		width_f, height_f = _float_width_height_from_area(square_size, landscape, aspect_a, aspect_b)
		return _io.NodeOutput(*_simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=cls.hidden.unique_id, target_square_size=square_size
		))
