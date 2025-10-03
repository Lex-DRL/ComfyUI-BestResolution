# encoding: utf-8
"""
"""

from inspect import cleandoc as _cleandoc
from math import sqrt as _sqrt

from comfy_api.latest import io as _io

from . import _io_simple as _i
from ._io_simple import _io_override
from . import _meta
from .docstring_formatter import format_docstring as _format_docstring
from .funcs import simple_result_from_approx_wh as _simple_result_from_approx_wh


class BestResolutionScale(_io.ComfyNode):
	"""
	Scale width and height by the same value + round them.
	"""
	_schema = _io.Schema(
		'BestResolutionScale',
		display_name="Scale (Best-Res)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io_override(_i.res, 'width'),
			_io_override(_i.res, 'height'),
			_io_override(_i.step_default, 'step'),
			_i.scale,
			_io.Boolean.Input('direction', default=True, label_on='res * scale', label_off='res / scale', tooltip=(
				"Sometimes it's easier to specify scale by it's inverse: how much to scale DOWN by. This toggle controls that."
			)),
		],

		hidden=[_io.Hidden.unique_id],

		outputs=[
			_io.Int.Output('WIDTH', display_name='width'),
			_io.Int.Output('HEIGHT', display_name='height'),
			_io.Float.Output('SCALE', display_name='scale'),
		],

		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		width: int, height: int, step: int, scale: float, direction: bool,
		# show: bool,
	) -> _io.NodeOutput:
		scale = float(scale)
		if not direction:
			scale = 1.0 / scale
		width_f = scale * width
		height_f = scale * height
		out_width, out_height = _simple_result_from_approx_wh(
			width_f, height_f, step,
			# show,
			unique_id=cls.hidden.unique_id,
			target_square_size=_sqrt(width_f * height_f),
			status_suffix=f"\n({width}/{height}) * {scale:.3f} scale"
		)
		return _io.NodeOutput(out_width, out_height, scale)
