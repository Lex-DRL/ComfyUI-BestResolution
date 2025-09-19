# encoding: utf-8
"""
"""

from inspect import cleandoc as _cleandoc

from comfy_api.latest import io as _io
from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel as _ImageUpscaleWithModel
from nodes import ImageScaleBy as _ImageScaleBy

from . import _io_simple as _i
from ._io_simple import _io_override
from . import _meta
from .__docstring_formatter import format_docstring as _format_docstring
from .funcs import _show_text_on_node


_ImageUpscaleWithModel_instance = _ImageUpscaleWithModel()
_ImageScaleBy_instance = _ImageScaleBy()


class ImageUpscaleByWithModel(_io.ComfyNode):
	"""
	A simple wrapper over "Upscale Image (using Model)" and "Upscale Image By".

	First, up-scales with model. Then, (down)scales to get to the desired scale factor.
	"""
	_schema = _io.Schema(
		'ImageUpscaleByWithModel',
		display_name="Upscale Image By (with Model)",
		category=_meta.category,
		description=_format_docstring(_cleandoc(__doc__)),

		inputs=[
			_io.UpscaleModel.Input('upscale_model'),
			_io.Image.Input('image'),
			_io_override(_i.scale, 'model_scale', default=2.0, round=0.00001, tooltip=(
				"The upscale factor a model natively increases image by"
			)),
			_io.Combo.Input('scale_method', options=_ImageScaleBy.upscale_methods, default='bicubic'),
			_io_override(_i.scale, 'scale', default=1.5, round=0.00001, tooltip=(
				"The actual factor you want to upscale by"
			)),
			_io.Boolean.Input('show_status', default=False, label_on='scales performed', label_off='no', tooltip=(
				"Show the extracted string on the node itself?"
			)),
		],

		hidden=[_io.Hidden.unique_id],

		outputs=[_io.Image.Output('IMAGE', display_name='image')],
	)

	@classmethod
	def define_schema(cls) -> _io.Schema:
		return cls._schema

	# Threshold for "almost equal to 1.0".
	# Supposedly, no image would go beyond 250k pixels in either side (even polygraphy),
	# and the double of that equals change of less than a half-pixel.
	_epsilon = 1.0 / 500_000
	_half_upper_threshold = 0.5 + _epsilon * 0.5

	@classmethod
	def _status_message(
		cls,
		no_model_scale: bool, do_downscale: bool, model_scale: float, scale: float, second_downscale: float
	):
		if no_model_scale:
			return f"🤔❔ x{scale:.3f} (no model)"
		if not do_downscale:
			return f"x{scale:.3f} (no second scale)"

		base_msg = f"x{scale:.3f} = x{model_scale:.3f} → <strong>x{second_downscale:.3f}</strong>"
		if scale > model_scale:
			return f"‼️ <strong>VERY</strong> blurry output\n{base_msg}"
		if scale > (model_scale - 0.5 + cls._epsilon):
			return f"⚠️ Blurry output\n{base_msg}"
		return base_msg

	@classmethod
	def execute(
		cls,
		upscale_model, image, model_scale: float, scale_method, scale: float,
		show_status: bool = False,
	) -> _io.NodeOutput:
		second_downscale = scale / model_scale
		do_downscale = abs(second_downscale - 1.0) > cls._epsilon
		no_model_scale = (
			scale <= cls._half_upper_threshold
			or abs(model_scale - 1.0) <= cls._epsilon
		)
		if no_model_scale:
			out_image = _ImageScaleBy_instance.upscale(image, scale_method, scale)[0]
		else:
			out_image = _ImageUpscaleWithModel_instance.upscale(upscale_model, image)[0]
			if do_downscale:
				out_image = _ImageScaleBy_instance.upscale(out_image, scale_method, second_downscale)[0]

		unique_id = cls.hidden.unique_id
		if show_status and unique_id:
			msg = cls._status_message(no_model_scale, do_downscale, model_scale, scale, second_downscale)
			_show_text_on_node(msg, unique_id)

		return _io.NodeOutput(out_image, )
