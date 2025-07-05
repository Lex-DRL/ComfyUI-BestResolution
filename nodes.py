# encoding: utf-8
"""
"""

import typing as _t

from frozendict import deepfreeze

from comfy.comfy_types.node_typing import IO as _IO

from .node_types import *


def _round_abs(abs_value: _t.Union[int, float], step: int):
	"""
	Assuming both args are positive and ``step`` is already an int, detect the closest positive (non-zero) value
	which is also divisible by step.
	"""
	n_steps = int(float(number_to_int(abs_value)) / step + 0.5)
	n_steps = max(n_steps, 1)
	return step * n_steps, n_steps


# Tiny optimization by reusing the same immutable dict:
_input_types_simple = deepfreeze({
	"required":  {
		"width": (_IO.INT, dict(type_dict_res, **{'tooltip': "Approximate width"})),
		"height": (_IO.INT, dict(type_dict_res, **{'tooltip': "Approximate height"})),
		"step": (_IO.INT, dict(type_dict_step_init, **{'tooltip': "Resolution must be divisible by this value"})),
	},
	# "hidden": {},
	# "optional": {},
})


class BestResolutionSimple:
	NODE_NAME = "BestResolutionSimple"
	CATEGORY = "utils/resolution"

	# OUTPUT_NODE = True  # TODO

	FUNCTION = "main"
	RETURN_TYPES = (_IO.INT, _IO.INT)
	RETURN_NAMES = ("width", "height")

	@classmethod
	def INPUT_TYPES(cls):
		return _input_types_simple

	def main(self, width: int, height: int, step: int):
		step = number_to_int(step)

		width, n_steps_x = _round_abs(width, step)
		height, n_steps_y = _round_abs(height, step)

		width = n_steps_x * step
		height = n_steps_y * step

		text = f"{width} x {height}\n{n_steps_x} * {step} x {n_steps_y} * {step}"
		print(f"text: {text}")

		# The following return format is snatched from built-in PreviewAny
		# and easy_nodes.show_text from (https://github.com/andrewharp/ComfyUI-EasyNodes);
		# doesn't seem to be documented anywhere 🤷🏻‍♂️
		return {
			# "ui": {"text": [text]},  # TODO: for some reason, it isn't displayed
			"result": (width, height)
		}
