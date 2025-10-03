# encoding: utf-8
"""
Nodes to calculate crop / padding values (for out-paint).
"""

from inspect import cleandoc as _cleandoc

from comfy_api.latest import io as _io

from . import _io_enum as _enums
from . import _io_simple as _i
from ._io_simple import _io_override
from . import _meta
from . import _tooltips as _tt
from .docstring_formatter import format_docstring as _format_docstring
from .funcs_crop_pad import upscaled_crop_pad as _upscaled_crop_pad

# ----------------------------------------------------------

class BestResolutionUpscaledCropPad(_io.ComfyNode):
	"""
	If the original resolution can't be scaled to the higher one uniformly (i.e., without stretching),
	this node detects the appropriate values for cropping/out-painting.
	"""
	_schema = _io.Schema(
		'BestResolutionUpscaledCropPad',
		display_name="Upscaled Crop/Pad (Best-Res)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),
		inputs=[
			_io_override(_i.upscale, tooltip=f"Only used when {_enums.UpscaledCropPadStrategy.EXACT_UPSCALE!r} strategy selected."),
			_io_override(_i.res, 'init_width', tooltip=_tt.init_width),
			_io_override(_i.res, 'init_height', tooltip=_tt.init_height),

			_io_override(_i.res, 'HD_width', default=1536, tooltip=_tt.HD_width),
			_io_override(_i.res, 'HD_height', default=1536, tooltip=_tt.HD_height),

			_enums.crop_pad_strategy_in,

			_io_override(_i.rel_pos, 'align_x', tooltip=(
				"Where's the image pivot for horizontal alignment (which side stays in place during crop/out-paint):\n"
				"0 - Left\n"
				"0.5 - Center\n"
				"1 - Right"
			)),
			_io_override(_i.rel_pos, 'align_y', default=0.0, tooltip=(
				"Where's the image pivot for vertical alignment (which side stays in place during crop/out-paint):\n"
				"0 - Bottom\n"
				"0.5 - Center\n"
				"1 - Top"
			)),
		],
		hidden=[_io.Hidden.unique_id],
		outputs=[
			# In v3 schema, IDs must be unique between BOTH lists: inputs and outputs, so uppercase ID + `display_name`:
			_io.Float.Output('UPSCALE', display_name='upscale', tooltip="The actual uniform upscale value to do."),

			# Once we have a single ID in the list, we need to specify all the display names.
			# Without it, outputs will be drawn with their types.
			_io.Boolean.Output('do_crop', display_name='do_crop', tooltip="Whether post-upscale crop needs to be done to get the specified resolution."),
			_io.Int.Output('crop_width', display_name='crop_width', tooltip="Width for the post-upscale crop."),
			_io.Int.Output('crop_height', display_name='crop_height', tooltip="Height for the post-upscale crop."),
			_io.Int.Output('crop_x', display_name='crop_x', tooltip="X-offset for the post-upscale crop."),
			_io.Int.Output('crop_y', display_name='crop_y', tooltip="Y-offset for the post-upscale crop."),

			_io.Boolean.Output('do_padding', display_name='do_padding', tooltip="Whether post-upscale padding and out-paint need to be done to get the specified resolution."),
			_io.Int.Output('pad_left', display_name='pad_left', tooltip="Left padding for the post-upscale out-paint."),
			_io.Int.Output('pad_top', display_name='pad_top', tooltip="Top padding for the post-upscale out-paint."),
			_io.Int.Output('pad_right', display_name='pad_right', tooltip="Right padding for the post-upscale out-paint."),
			_io.Int.Output('pad_bottom', display_name='pad_bottom', tooltip="Bottom padding for the post-upscale out-paint."),
		],
		is_output_node=True,
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	@classmethod
	def execute(
		cls,
		upscale: float,
		init_width: int, init_height: int, HD_width: int, HD_height: int,
		strategy: _enums.UpscaledCropPadStrategy | str,
		align_x: float, align_y: float,
		# show: bool,
	) -> _io.NodeOutput:
		return _io.NodeOutput(
			*_upscaled_crop_pad(
				upscale,
				init_width, init_height, HD_width, HD_height,
				_enums.UpscaledCropPadStrategy.validate(strategy),
				align_x, align_y,
				# show,
				unique_id=cls.hidden.unique_id
			)
		)
