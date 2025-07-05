# encoding: utf-8
"""
"""

import typing as _t

from inspect import cleandoc as _cleandoc
import sys as _sys

from frozendict import deepfreeze

from comfy.comfy_types.node_typing import IO as _IO

from .node_types import *


_t_number = _t.Union[int, float]


def _round_abs(abs_value: _t_number, step: int):
	"""
	Assuming both args are positive and ``step`` is already an int, detect the closest positive (non-zero) value
	which is also divisible by step.
	"""
	n_steps = int(float(abs_value) / step + 0.5)
	n_steps = max(n_steps, 1)
	return step * n_steps, n_steps


def _round_width_and_height_closest_to_the_ratio(width_f: _t_number, height_f: _t_number, step: int):
	"""3-pass detection of the best rounded resolution. Best = closest to the desired ratio."""
	desired_width_to_height_ratio = float(width_f) / height_f

	# First pass: directly from width_f and height_f
	width, n_steps_x = _round_abs(width_f, step)
	height, n_steps_y = _round_abs(height_f, step)

	# Second pass: try calculating one side from already rounded another one:
	height_from_width, n_steps_y_from_x = _round_abs(float(width) / desired_width_to_height_ratio, step)
	width_from_height, n_steps_x_from_y = _round_abs(float(height) * desired_width_to_height_ratio, step)

	# ... and select one of three options, closest to the perfect ratio:
	closest_delta = abs((float(width) / height) - desired_width_to_height_ratio)
	for w, n_x, h, n_y in [
		(width, n_steps_x, height_from_width, n_steps_y_from_x),
		(width_from_height, n_steps_x_from_y, height, n_steps_y),
	]:
		cur_delta = abs((float(w) / h) - desired_width_to_height_ratio)
		if cur_delta < closest_delta:
			closest_delta = cur_delta
			width, n_steps_x = w, n_x
			height, n_steps_y = h, n_y

	return width, n_steps_x, height, n_steps_y


_48_tooltip = (
	"The default 48 is (8 * 3 * 2), so it's a safe choice because:\n"
	"- it's compatible with SD1.5/XL step (divisible by 8),\n"
	"- it can be upscaled by x1.5 or x1.333 at the first iteration, which is optimal for latent-upscale,\n"
	"- after x1.5 upscale, if you only do x2 later (it's OK for already high resolutions) - it will be divisible "
	"by 3 AND 9, which might become handy at that point, where you'll probably use UltimateSDUpscale.\n\n"
	"Other values worth trying first: 64, 96, 128."
)

# Tiny optimization by reusing the same immutable dict:
_input_types_simple = deepfreeze({
	"required":  {
		"width": (_IO.INT, dict(type_dict_res, **{"tooltip": "Approximate width"})),
		"height": (_IO.INT, dict(type_dict_res, **{"tooltip": "Approximate height"})),
		"step": (_IO.INT, dict(type_dict_step_init, **{"tooltip": (
			f"Both width and height will be divisible by this value - by rounding them "
			f"to the closest appropriate resolution.\n\n{_48_tooltip}"
		)})),
	},
	# "hidden": {},
	# "optional": {},
})


class BestResolutionSimple:
	"""
	The simplest node for easier selection of an optimal resolution:
	only rounding performed, desired image size specified directly.
	"""
	NODE_NAME = "BestResolutionSimple"
	CATEGORY = "utils/resolution"
	DESCRIPTION = _cleandoc(__doc__)

	# OUTPUT_NODE = True  # TODO

	FUNCTION = "main"
	RETURN_TYPES = (_IO.INT, _IO.INT)
	# RETURN_TYPES_TOOLTIPS = {}
	RETURN_NAMES = ("width", "height")

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_simple

	def main(self, width: int, height: int, step: int):
		step = number_to_int(step)
		width, n_steps_x, height, n_steps_y = _round_width_and_height_closest_to_the_ratio(width, height, step)

		text = f"{width} x {height}\n{n_steps_x} * {step} x {n_steps_y} * {step}"
		# print(f"text: {text}")

		# The following return format is snatched from built-in PreviewAny
		# and easy_nodes.show_text from (https://github.com/andrewharp/ComfyUI-EasyNodes);
		# doesn't seem to be documented anywhere 🤷🏻‍♂️
		return {
			# "ui": {"text": [text]},  # TODO: for some reason, it isn't displayed
			"result": (width, height)
		}


_tooltip_aspect = (
	"Two aspects together define an aspect ratio (16:9, 4:3, etc).\n"
	"Order doesn't matter: image orientation is defined by the 'landscape' toggle.\n\n"
	"The specified aspect ratio is APPROXIMATE: step parameter has priority over the exact image proportions."
)

_input_types_orient = deepfreeze({
	"required":  {
		"size": (_IO.INT, dict(type_dict_res, **{"tooltip": (
			"Approximate size of one of the image sides.\nWhich one - see the 'size_is_big' and 'landscape' toggles."
		)})),
		"step": _input_types_simple["required"]["step"],
		"size_is_big": (_IO.BOOLEAN, {
			"default": True, "label_on": "bigger", "label_off": "smaller",
			"tooltip": "When ON, size parameter represents the bigger image side.\nWhen OFF, it specifies the smaller one."
		}),
		"landscape": (_IO.BOOLEAN, {
			"default": True, "label_on": "landscape", "label_off": "portrait",
			"tooltip": (
				"Specifies image orientation:\n\n"
				"When ON, width is bigger (image is horizontal).\n"
				"When OFF, height is bigger (image is vertical)."
			)
		}),
		"aspect_a": (_IO.FLOAT, {
			"default": 16.0, "min": 1.0, "max": _sys.float_info.max, "step": 1.0, "round": 0.001,
			"tooltip": _tooltip_aspect
		}),
		"aspect_b": (_IO.FLOAT, {
			"default": 9.0, "min": 1.0, "max": _sys.float_info.max, "step": 1.0, "round": 0.001,
			"tooltip": _tooltip_aspect
		}),
	},
	# "hidden": {},
	# "optional": {},
})


class BestResolutionFromAspectRatio:
	"""
	A more advanced node for easier selection of an optimal resolution:
	image size specified indirectly - by one of the sides + aspect ratio.
	"""
	NODE_NAME = "BestResolutionFromAspectRatio"
	CATEGORY = "utils/resolution"
	DESCRIPTION = _cleandoc(__doc__)

	# OUTPUT_NODE = True  # TODO

	FUNCTION = "main"
	RETURN_TYPES = (_IO.INT, _IO.INT)
	RETURN_NAMES = ("width", "height")

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_orient

	def main(self, size: int, step: int, size_is_big: bool, landscape: bool, aspect_a: float, aspect_b: float):
		aspect_a = max(float(aspect_a), 1.0)
		aspect_b = max(float(aspect_b), 1.0)
		aspect_big = max(aspect_a, aspect_b)
		aspect_small = min(aspect_a, aspect_b)

		side_main_f = float(size)
		side_secondary_f = side_main_f * (
			(aspect_small / aspect_big) if size_is_big else (aspect_big / aspect_small)
		)

		width_f = max(side_main_f, side_secondary_f)
		height_f = min(side_main_f, side_secondary_f)
		if not landscape:
			# The opposite: height is bigger
			width_f, height_f = height_f, width_f

		step = number_to_int(step)
		width, n_steps_x, height, n_steps_y = _round_width_and_height_closest_to_the_ratio(width_f, height_f, step)

		text = f"{width} x {height}\n{n_steps_x} * {step} x {n_steps_y} * {step}"
		return {
			# "ui": {"text": [text]},  # TODO: for some reason, it isn't displayed
			"result": (width, height)
		}
