# encoding: utf-8
"""
Internal utility functions. They're intended to be used only by the methods within nodes,
so they might expect the input arguments to already be pre-validated.
"""

import typing as _t

from math import sqrt as _sqrt

from server import PromptServer as _PromptServer

from .enums import *


_t_number = _t.Union[int, float]


def aspect_ratios_sorted(aspect_a: float, aspect_b: float, min_clamp: float = 1.0):
	"""Return aspect ratio in a standard form: 2 floats, both 1+, in descending order (16:9, not 9:16)."""
	aspect_a = float(max(abs(aspect_a), min_clamp))
	aspect_b = float(max(abs(aspect_b), min_clamp))
	return (aspect_b, aspect_a) if aspect_b > aspect_a else (aspect_a, aspect_b)


def number_to_int(value: _t_number, min: int = 1) -> int:
	if not isinstance(value, int):
		if isinstance(value, float):
			sign = -1 if value < 0.0 else 1
			value = int(value * sign + 0.5) * sign
		else:
			value = int(value)
	return max(value, min)


def round_pos_int(value: float) -> int:
	"""Assuming a positive float is provided, rounds it to the nearest integer."""
	return int(value + 0.5)


def round_abs_to_step(abs_value: _t_number, step: int):
	"""
	Assuming both args are positive and ``step`` is already an int, detect the closest positive (non-zero) value
	which is also divisible by step.
	"""
	n_steps = round_pos_int(float(abs_value) / step)
	n_steps = max(n_steps, 1)
	return step * n_steps, n_steps


def round_width_and_height_closest_to_the_ratio(width_f: _t_number, height_f: _t_number, step: int):
	"""3-pass detection of the best rounded resolution. Best = closest to the desired ratio."""
	desired_width_to_height_ratio = float(width_f) / height_f

	# First pass: directly from width_f and height_f
	width, n_steps_x = round_abs_to_step(width_f, step)
	height, n_steps_y = round_abs_to_step(height_f, step)

	# Second pass: try calculating one side from already rounded another one:
	height_from_width, n_steps_y_from_x = round_abs_to_step(float(width) / desired_width_to_height_ratio, step)
	width_from_height, n_steps_x_from_y = round_abs_to_step(float(height) * desired_width_to_height_ratio, step)

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
		target_square_size_i = round_pos_int(target_square_size)
		if target_square_size_i * target_square_size_i == area_output:
			return f"=👑{target_square_size_i}🔳"
			# return f"=💯{target_square_size_i}🔳"
			# return f"=✨{target_square_size_i}🔳"
		if round_pos_int(target_square_size * target_square_size) == area_output:
			return f"=✨{target_square_size:.2f}🔳"
			# return f"=🌟{target_square_size:.2f}🔳"

	desired_square_area_f = float(width_f) * height_f
	desired_square_side_f = _sqrt(desired_square_area_f)
	desired_square_side_i = round_pos_int(desired_square_side_f)
	if desired_square_side_i * desired_square_side_i == area_output:
		return f"=✅{desired_square_side_i}🔳"

	actual_square_side_f = _sqrt(float(area_output))
	actual_square_side_i = round_pos_int(actual_square_side_f)
	if abs(actual_square_side_f - actual_square_side_i) < 0.005:
		return f"~={actual_square_side_i}🔳"
	return f"~={actual_square_side_f:.2f}🔳"


def format_report_simple(
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
	width_f: float, height_f: _t_number, step: int,
	show: bool = True,
	unique_id: str = None, target_square_size: _t_number = None
):
	"""Final part of the main func for simple (non-upscale) nodes - when desired width/height are already calculated."""
	step = number_to_int(step)
	width, n_steps_x, height, n_steps_y = round_width_and_height_closest_to_the_ratio(width_f, height_f, step)

	result = (width, height)

	if not unique_id:
		return result

	text = (
		format_report_simple(width_f, height_f, step, width, n_steps_x, height, n_steps_y, target_square_size)
		if show
		# TODO: Planned for the future - currently, there's no point removing the text since it's box is shown anyway
		else '<span></span>' # An odd workaround since `send_progress_text()` doesn't want to update text when '' passed
	)
	# print(f"{unique_id} text: {text!r}")
	# Snatched from: https://github.com/comfyanonymous/ComfyUI/blob/27870ec3c30e56be9707d89a120eb7f0e2836be1/comfy_extras/nodes_images.py#L581-L582
	_PromptServer.instance.send_progress_text(text, unique_id)

	return result


def upscale_result_from_approx_wh(
	width_f: float, height_f: _t_number, step: int,
	priority: _t.Union[RoundingPriority, str], upscale: float, up_step:int,
	show: bool = True,
	unique_id: str = None, target_square_size: _t_number = None
):
	"""Primary part of the main func for nodes with upscaling - when desired initial-width/height are already calculated."""
	upscale = max(float(upscale), 1.0)
	up_width_f: float = upscale * width_f
	up_height_f: float = upscale * height_f
	width_f = float(width_f)

	step = number_to_int(step)
	up_step = number_to_int(up_step)

	if priority == RoundingPriority.DESIRED:
		width, n_steps_x, height, n_steps_y = round_width_and_height_closest_to_the_ratio(width_f, height_f, step)
		up_width, up_steps_x, up_height, up_steps_y = round_width_and_height_closest_to_the_ratio(
			up_width_f, up_height_f, up_step
		)
	elif priority == RoundingPriority.ORIGINAL:
		width, n_steps_x, height, n_steps_y = round_width_and_height_closest_to_the_ratio(width_f, height_f, step)
		up_width, up_steps_x, up_height, up_steps_y = round_width_and_height_closest_to_the_ratio(
			upscale * width, upscale * height, up_step
		)
	else:
		up_width, up_steps_x, up_height, up_steps_y = round_width_and_height_closest_to_the_ratio(
			up_width_f, up_height_f, up_step
		)
		width, n_steps_x, height, n_steps_y = round_width_and_height_closest_to_the_ratio(
			float(up_width) / upscale, float(up_height) / upscale, step
		)

	result = (width, height, up_width, up_height)

	if not unique_id:
		return result

	# TODO: Planned for the future - currently, there's no point removing the text since it's box is shown anyway
	text = '<span></span>'  # An odd workaround since `send_progress_text()` doesn't want to update text when '' passed
	if show:
		reports: _t.List[str] = list()
		for prefix, w_f, h_f, s, w, n_x, h, n_y, trg_sq in [
			('◻️ ', width_f, height_f, step, width, n_steps_x, height, n_steps_y, target_square_size),
			('🔲 ', up_width_f, up_height_f, up_step, up_width, up_steps_x, up_height, up_steps_y, _sqrt(up_width_f * up_height_f))
		]:
			cur_report = format_report_simple(w_f, h_f, s, w, n_x, h, n_y, trg_sq)
			reports.append('\n'.join(
				f"{prefix}{x}" for x in cur_report.split('\n')
			))
		real_upscale_x = float(up_width) / width
		real_upscale_y = float(up_height) / height

		# Pixel size relative to the upscaled image:
		up_half_pixel_x = 0.5 / up_width
		up_half_pixel_y = 0.5 / up_height
		# Threshold for upscale-multiplier to be considered the same res:
		almost_equal_rel_delta_x = real_upscale_x * up_half_pixel_x
		almost_equal_rel_delta_y = real_upscale_y * up_half_pixel_y
		almost_equal_rel_delta = max(almost_equal_rel_delta_x, almost_equal_rel_delta_y)
		if abs(real_upscale_x - real_upscale_y) < almost_equal_rel_delta:
			# The x/y delta between upscale multipliers is below a threshold to contribute even 1 pixel.
			# So, basically, the upscale is uniform:
			divider_line = f"\n--- x{real_upscale_x:.3f} ---\n"
		else:
			divider_line = f"\n--- ⚠️ x{real_upscale_x:.3f} / x{real_upscale_y:.3f} ---\n"
		text = divider_line.join(reports)
	# Snatched from: https://github.com/comfyanonymous/ComfyUI/blob/27870ec3c30e56be9707d89a120eb7f0e2836be1/comfy_extras/nodes_images.py#L581-L582
	_PromptServer.instance.send_progress_text(text, unique_id)

	return result
