# encoding: utf-8
"""
"""

import typing as _t

from inspect import cleandoc as _cleandoc

from frozendict import deepfreeze as _deepfreeze

from comfy.comfy_types.node_typing import IO as _IO
# from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel as _ImageUpscaleWithModel
# from nodes import ImageScaleBy as _ImageScaleBy

from . import _meta
from .docstring_formatter import format_docstring as _format_docstring
from .node_scale import _scale_type_dict as __scale_type_dict_base
from .funcs import _show_text_on_node


# ==========================================================
# Copy of built-in ComfyUI nodes with v1 schema,
# as a temporary workaround


import torch

from comfy import model_management
import comfy.utils


class _ImageUpscaleWithModel:
	@classmethod
	def INPUT_TYPES(s):
		return {"required": {
			"upscale_model": ("UPSCALE_MODEL",), "image": ("IMAGE",),
		}}
	RETURN_TYPES = ("IMAGE",)
	FUNCTION = "upscale"

	CATEGORY = "image/upscaling"

	def upscale(self, upscale_model, image):
		device = model_management.get_torch_device()

		memory_required = model_management.module_size(upscale_model.model)
		memory_required += (512 * 512 * 3) * image.element_size() * max(upscale_model.scale, 1.0) * 384.0 #The 384.0 is an estimate of how much some of these models take, TODO: make it more accurate
		memory_required += image.nelement() * image.element_size()
		model_management.free_memory(memory_required, device)

		upscale_model.to(device)
		in_img = image.movedim(-1,-3).to(device)

		tile = 512
		overlap = 32

		oom = True
		while oom:
			try:
				steps = in_img.shape[0] * comfy.utils.get_tiled_scale_steps(in_img.shape[3], in_img.shape[2], tile_x=tile, tile_y=tile, overlap=overlap)
				pbar = comfy.utils.ProgressBar(steps)
				s = comfy.utils.tiled_scale(in_img, lambda a: upscale_model(a), tile_x=tile, tile_y=tile, overlap=overlap, upscale_amount=upscale_model.scale, pbar=pbar)
				oom = False
			except model_management.OOM_EXCEPTION as e:
				tile //= 2
				if tile < 128:
					raise e

		upscale_model.to("cpu")
		s = torch.clamp(s.movedim(-3,-1), min=0, max=1.0)
		return (s,)


class _ImageScaleBy:
	upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

	@classmethod
	def INPUT_TYPES(s):
		return {"required": {
			"image": ("IMAGE",), "upscale_method": (s.upscale_methods,),
			"scale_by": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 8.0, "step": 0.01}),
		}}
	RETURN_TYPES = ("IMAGE",)
	FUNCTION = "upscale"

	CATEGORY = "image/upscaling"

	def upscale(self, image, upscale_method, scale_by):
		samples = image.movedim(-1,1)
		width = round(samples.shape[3] * scale_by)
		height = round(samples.shape[2] * scale_by)
		s = comfy.utils.common_upscale(samples, width, height, upscale_method, "disabled")
		s = s.movedim(1,-1)
		return (s,)


# ==========================================================


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
