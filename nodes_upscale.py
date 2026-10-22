# encoding: utf-8
"""
Advanced versions of nodes - with upscale.
"""

import typing as _t

from inspect import cleandoc as _cleandoc
from itertools import chain as _chain

from comfy_api.latest import io as _io

from . import _io_enum as _enums
from . import _io_simple as _i
from ._io_simple import _io_override
from . import _meta
from . import _tooltips as _tt
from .__docstring_formatter import format_docstring as _format_docstring
from .funcs import (
	number_to_int as _number_to_int,
	float_width_height_from_area as _float_width_height_from_area,
	upscale_result_from_approx_wh as _upscale_result_from_approx_wh
)
from .nodes_simple import BestResolutionFromArea as _BestResolutionFromArea

# ----------------------------------------------------------

class BestResolutionFromAreaUpscale(_io.ComfyNode):
	"""
	The most efficient way of selecting an optimal resolution:
	image size selected indirectly - by the total desired resolution (area) + aspect ratio...

	... PLUS, account for the immediate upscale right away.


	Desired resolution (aka image area/megapixels/pixel count) is specified with a side of a square image. This isn't
	accidental: most models disclose what image resolution they're trained on, and usually they're square:
	- SD 1.5 - 512x512 pixels
	- SDXL - 1024x1024 pixels


	By simply providing this single number and setting your aspect ratio/orientation, you get the width and height to
	produce the closest total resolution to the training set, while also respecting image proportions and step-rounding.
	"""
	_schema = _io.Schema(
		'BestResolutionFromAreaUpscale',
		display_name="Best-Res (area+scale)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),

		inputs=list(_chain(
			(
				x for x in _BestResolutionFromArea._schema.inputs
				if x.id != 'show'
			),
			[
				_enums.res_priority_in,
				_i.upscale,
				_io_override(_i.step_upscale1, 'HD_step')
			]
		)),

		hidden=[_io.Hidden.unique_id],

		outputs=[
			_io.Float.Output('UPSCALE', display_name='upscale', tooltip=_tt.upscale),
			_io.Int.Output('init_width', display_name='init_width', tooltip=_tt.init_width),
			_io.Int.Output('init_height', display_name='init_height', tooltip=_tt.init_height),
			_io.Int.Output('HD_width', display_name='HD_width', tooltip=_tt.HD_width),
			_io.Int.Output('HD_height', display_name='HD_height', tooltip=_tt.HD_height),
		],

		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		square_size: int, step: int, landscape: bool, aspect_a: float, aspect_b: float,
		priority: _t.Union[_enums.RoundingPriority, str], upscale: float, HD_step:int,
		# show: bool,
	) -> _io.NodeOutput:
		square_size: int = _number_to_int(square_size)
		width_f, height_f = _float_width_height_from_area(square_size, landscape, aspect_a, aspect_b)
		return _io.NodeOutput(*_upscale_result_from_approx_wh(
			width_f, height_f, step,
			_enums.RoundingPriority.validate(priority), upscale, HD_step,
			# show,
			unique_id=cls.hidden.unique_id, target_square_size=square_size
		))
