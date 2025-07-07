# encoding: utf-8
"""
Internal utility functions. They're intended to be used only by the methods within nodes,
so they might expect the input arguments to already be pre-validated.
"""

import typing as _t

from math import sqrt as _sqrt

from server import PromptServer as _PromptServer


_t_number = _t.Union[int, float]


def aspect_ratios_sorted(aspect_a: float, aspect_b: float, min_clamp: float = 1.0):
	"""Return aspect ratio in a standard form: 2 floats, both 1+, in descending order (16:9, not 9:16)."""
	aspect_a = float(max(abs(aspect_a), min_clamp))
	aspect_b = float(max(abs(aspect_b), min_clamp))
	return (aspect_b, aspect_a) if aspect_b > aspect_a else (aspect_a, aspect_b)


def number_to_int(value: _t.Union[int, float], min: int = 1) -> int:
	if not isinstance(value, int):
		if isinstance(value, float):
			sign = -1 if value < 0.0 else 1
			value = int(value * sign + 0.5) * sign
		else:
			value = int(value)
	return max(value, min)


def round_abs(abs_value: _t_number, step: int):
	"""
	Assuming both args are positive and ``step`` is already an int, detect the closest positive (non-zero) value
	which is also divisible by step.
	"""
	n_steps = int(float(abs_value) / step + 0.5)
	n_steps = max(n_steps, 1)
	return step * n_steps, n_steps


def round_width_and_height_closest_to_the_ratio(width_f: _t_number, height_f: _t_number, step: int):
	"""3-pass detection of the best rounded resolution. Best = closest to the desired ratio."""
	desired_width_to_height_ratio = float(width_f) / height_f

	# First pass: directly from width_f and height_f
	width, n_steps_x = round_abs(width_f, step)
	height, n_steps_y = round_abs(height_f, step)

	# Second pass: try calculating one side from already rounded another one:
	height_from_width, n_steps_y_from_x = round_abs(float(width) / desired_width_to_height_ratio, step)
	width_from_height, n_steps_x_from_y = round_abs(float(height) * desired_width_to_height_ratio, step)

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


def float_width_height_from_area(square_size: _t_number, landscape: bool, aspect_a: float, aspect_b: float):
	"""The main function for the regular (non-upscale) ``area``-subtype node."""
	# square_size = 1024; step = 48; landscape = True; aspect_a = 9.0; aspect_b = 16.0
	aspect_big, aspect_small = aspect_ratios_sorted(aspect_a, aspect_b)
	aspect_x, aspect_y = (aspect_big, aspect_small) if landscape else (aspect_small, aspect_big)

	aspect_area = aspect_x * aspect_y
	aspect_norm_scale = 1.0 / _sqrt(aspect_area)
	aspect_x *= aspect_norm_scale
	aspect_y *= aspect_norm_scale
	# Now the two aspects produce a normalized rectangle - i.e., it's area is 1

	width_f: float = aspect_x * square_size
	height_f: float = aspect_y * square_size
	return width_f, height_f


def _format_report_square_part(
	width_f: float, height_f: _t_number,
	width: int, height: int,
	target_square_size: _t_number = None
) -> str:
	area_output = width * height
	if target_square_size is not None:
		target_square_size = max(abs(target_square_size), 1)
		target_square_size_i = int(target_square_size + 0.5)
		if target_square_size_i * target_square_size_i == area_output:
			return f"=👑{target_square_size_i}🔳"
			# return f"=💯{target_square_size_i}🔳"
			# return f"=✨{target_square_size_i}🔳"
		if int(target_square_size * target_square_size + 0.5) == area_output:
			return f"=✨{target_square_size:.2f}🔳"
			# return f"=🌟{target_square_size:.2f}🔳"

	desired_square_area_f = float(width_f) * height_f
	desired_square_side_f = _sqrt(desired_square_area_f)
	desired_square_side_i = int(desired_square_side_f + 0.5)
	if desired_square_side_i * desired_square_side_i == area_output:
		return f"=✅{desired_square_side_i}🔳"

	actual_square_side_f = _sqrt(float(area_output))
	actual_square_side_i = int(actual_square_side_f + 0.5)
	if abs(actual_square_side_f - actual_square_side_i) < 0.005:
		return f"~={actual_square_side_i}🔳"
	return f"~={actual_square_side_f:.2f}🔳"


def format_report(
	width_f: float, height_f: _t_number, step: int,
	width: int, n_steps_x: int, height: int, n_steps_y: int,
	target_square_size: _t_number = None
) -> str:
	square_side_text = _format_report_square_part(width_f, height_f, width, height, target_square_size)

	ar_desired = width_f / height_f
	ar_real = float(width) / height
	ar_text = (
		f"AR: ✅ {ar_real:.3f}"
		if abs(ar_desired - ar_real) < 0.0005
		else f"AR real/goal: {ar_real:.3f}/{ar_desired:.3f}"
	)

	return (
		f"{width}/{height}{square_side_text}\n"
		f"{n_steps_x} * {step} / {n_steps_y} * {step}\n"
		f"{ar_text}"
	)


def simple_result_from_approx_wh(
	width_f: float, height_f: _t_number, step: int, show: bool = True,
	unique_id: str = None, target_square_size: _t_number = None
):
	"""Final part of the main func for simple (non-upscale) nodes - when desired float/height are already calculated"""
	step = number_to_int(step)
	width, n_steps_x, height, n_steps_y = round_width_and_height_closest_to_the_ratio(width_f, height_f, step)

	if unique_id:
		text = (
			format_report(width_f, height_f, step, width, n_steps_x, height, n_steps_y, target_square_size)
			if show
			# TODO: Planned for the future - currently, there's no point removing the text since it's box is shown anyway
			else '<span></span>' # An odd workaround since `send_progress_text()` doesn't want to update text when '' passed
		)
		# print(f"{unique_id} text: {text!r}")
		# Snatched from: https://github.com/comfyanonymous/ComfyUI/blob/27870ec3c30e56be9707d89a120eb7f0e2836be1/comfy_extras/nodes_images.py#L581-L582
		_PromptServer.instance.send_progress_text(text, unique_id)

	return width, height
