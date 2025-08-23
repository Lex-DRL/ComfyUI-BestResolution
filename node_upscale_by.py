# encoding: utf-8
"""
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from comfy.comfy_types.node_typing import IO as _IO
from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel as _ImageUpscaleWithModel
from nodes import ImageScaleBy as _ImageScaleBy

from . import _meta
from .docstring_formatter import format_docstring as _format_docstring
from .node_scale import _scale_type_dict as __scale_type_dict_base
from .funcs import _show_text_on_node


_ImageUpscaleWithModel_instance = _ImageUpscaleWithModel()
__ImageUpscaleWithModel_input_types: _t.Dict[str, dict] = _ImageUpscaleWithModel_instance.INPUT_TYPES()
__ImageUpscaleWithModel_input_types_required = __ImageUpscaleWithModel_input_types.get('required', dict())

_ImageScaleBy_instance = _ImageScaleBy()

__scale_type_dict: _t.Dict[str, _t.Any] = dict(__scale_type_dict_base, round=0.00001)

_input_types = _deepfreeze({
	'required': {
		'upscale_model': __ImageUpscaleWithModel_input_types_required.get('upscale_model', (_IO.UPSCALE_MODEL, )),
		'image': __ImageUpscaleWithModel_input_types_required.get('image', (_IO.IMAGE, )),
		'model_scale': (
			_IO.FLOAT,
			dict(__scale_type_dict, default=2.0, tooltip='The upscale factor a model natively increases image by'),
		),
		'scale_method': (_ImageScaleBy.upscale_methods, {'default': 'bicubic'}),
		'scale': (
			_IO.FLOAT,
			dict(__scale_type_dict, default=1.5, tooltip='The actual factor you want to upscale by'),
		),
		'show_status': (
			_IO.BOOLEAN,
			{
				'default': False, 'label_on': 'scales performed', 'label_off': 'no',
				'tooltip': "Show the extracted string on the node itself?"
			},
		),
	},
	# 'optional': {},
	'hidden': {
		'unique_id': 'UNIQUE_ID',  # used for text display at the bottom of the node
	},
})

# Threshold for "almost equal to 1.0".
# Supposedly, no image would go beyond 250k pixels in either side (even polygraphy),
# and the double of that equals change of less than a half-pixel.
_epsilon = 1.0 / 500_000
_half_upper_threshold = 0.5 + _epsilon * 0.5


def _status_message(no_model_scale: bool, do_downscale: bool, model_scale: float, scale: float, second_downscale: float):
	if no_model_scale:
		return f"🤔❔ x{scale:.3f} (no model)"
	if not do_downscale:
		return f"x{scale:.3f} (no second scale)"

	base_msg = f"x{scale:.3f} = x{model_scale:.3f} → <strong>x{second_downscale:.3f}</strong>"
	if scale > model_scale:
		return f"‼️ <strong>VERY</strong> blurry output\n{base_msg}"
	if scale > (model_scale - 0.5 + _epsilon):
		return f"⚠️ Blurry output\n{base_msg}"
	return base_msg


class ImageUpscaleByWithModel:
	"""
	A simple wrapper over "Upscale Image (using Model)" and "Upscale Image By".

	First, up-scales with model. Then, (down)scales to get to the desired scale factor.
	"""
	NODE_NAME = 'ImageUpscaleByWithModel'
	CATEGORY = _meta.category
	DESCRIPTION = _format_docstring(_cleandoc(__doc__))

	FUNCTION = 'main'
	RETURN_TYPES = (_IO.IMAGE, )
	RETURN_NAMES = ('image', )
	# OUTPUT_TOOLTIPS = tuple()

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types

	@staticmethod
	def main(
		upscale_model, image, model_scale: float, scale_method, scale: float,
		show_status: bool = False,
		unique_id: str = None,
	) -> _t.Tuple[str]:
		"""
		A simple wrapper over ``ImageUpscaleWithModel`` and ``ImageScaleBy``.

		First, up-scales with model. Then, (down)scales to get to the desired scale factor.
		"""
		second_downscale = scale / model_scale
		do_downscale = abs(second_downscale - 1.0) > _epsilon
		no_model_scale = (
			scale <= _half_upper_threshold
			or abs(model_scale - 1.0) <= _epsilon
		)
		if no_model_scale:
			out_image = _ImageScaleBy_instance.upscale(image, scale_method, scale)[0]
		else:
			out_image = _ImageUpscaleWithModel_instance.upscale(upscale_model, image)[0]
			if do_downscale:
				out_image = _ImageScaleBy_instance.upscale(out_image, scale_method, second_downscale)[0]

		if show_status and unique_id:
			msg = _status_message(no_model_scale, do_downscale, model_scale, scale, second_downscale)
			_show_text_on_node(msg, unique_id)

		return (out_image, )
