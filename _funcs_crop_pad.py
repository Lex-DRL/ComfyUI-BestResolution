# encoding: utf-8
"""
The actual behavior of "Upscaled Crop/Pad" node.
"""

import typing as _t

from ._dataclass import dataclass_with_slots_if_possible as _dataclass_with_slots_if_possible
from ._funcs import round_pos_int as _round_pos_int, _need_post_resize, _show_text_on_node
from .enums import *
from .return_tuples import *


@_dataclass_with_slots_if_possible
class _CropPadInput:
	"""
	For the ease of passing between the functions, the entire set of inputs for "Upscaled Crop/Pad" node
	is internally turned into a dataclass.
	"""
	upscale: float

	init_w: int
	init_h: int
	hd_w: int
	hd_h: int

	strategy: str
	align_x: float
	align_y: float


def _upscaled_crop_xy_offset(extra_w: int, extra_h: int, align_x: float, align_y: float):
	crop_x_origin = _round_pos_int(align_x * extra_w)
	crop_y_origin = _round_pos_int((1.0 - align_y) * extra_h)
	return crop_x_origin, crop_y_origin


def _upscaled_crop(_in: _CropPadInput, real_upscale: float) -> ResultUpscaledCropPad:
	raw_upscaled_w = _round_pos_int(real_upscale * _in.init_w)
	raw_upscaled_h = _round_pos_int(real_upscale * _in.init_h)
	extra_w = max(raw_upscaled_w - _in.hd_w, 0)
	extra_h = max(raw_upscaled_h - _in.hd_h, 0)
	crop_x_offset, crop_y_offset = _upscaled_crop_xy_offset(extra_w, extra_h, _in.align_x, _in.align_y)
	return ResultUpscaledCropPad(
		real_upscale,
		True, _in.hd_w, _in.hd_h, crop_x_offset, crop_y_offset,
		False, 0, 0, 0, 0,
	)


def _upscaled_pad_side_values(extra_w: int, extra_h: int, align_x: float, align_y: float):
	pad_left = _round_pos_int(align_x * extra_w)
	pad_right = extra_w - pad_left
	pad_bottom = _round_pos_int(align_y * extra_h)
	pad_top = extra_h - pad_bottom
	return pad_left, pad_top, pad_right, pad_bottom


def _upscaled_pad(_in: _CropPadInput, real_upscale: float) -> ResultUpscaledCropPad:
	raw_upscaled_w = _round_pos_int(real_upscale * _in.init_w)
	raw_upscaled_h = _round_pos_int(real_upscale * _in.init_h)
	pad_w = max(_in.hd_w - raw_upscaled_w, 0)
	pad_h = max(_in.hd_h - raw_upscaled_h, 0)
	return ResultUpscaledCropPad(
		real_upscale,
		False, raw_upscaled_w, raw_upscaled_h, 0, 0,
		True, *_upscaled_pad_side_values(pad_w, pad_h, _in.align_x, _in.align_y),
	)


def _upscaled_crop_delta_pixels(_in: _CropPadInput, result: ResultUpscaledCropPad) -> int:
	"""Calculate the area of total cropped patch for crop-only mode."""
	raw_upscaled_w = _round_pos_int(result.upscale * _in.init_w)
	raw_upscaled_h = _round_pos_int(result.upscale * _in.init_h)
	cropped_w = min(result.crop_width, raw_upscaled_w)
	cropped_h = min(result.crop_height, raw_upscaled_h)
	return abs(raw_upscaled_w * raw_upscaled_h - cropped_w * cropped_h)


def _upscaled_pad_delta_pixels(_in: _CropPadInput, result: ResultUpscaledCropPad) -> int:
	"""Calculate the area of total out-painted patch for pad-only mode."""
	raw_upscaled_w = _round_pos_int(result.upscale * _in.init_w)
	raw_upscaled_h = _round_pos_int(result.upscale * _in.init_h)
	padded_w = raw_upscaled_w + max(result.pad_left, 0) + max(result.pad_right, 0)
	padded_h = raw_upscaled_h + max(result.pad_top, 0) + max(result.pad_bottom, 0)
	return abs(padded_w * padded_h - raw_upscaled_w * raw_upscaled_h)


def _upscaled_crop_pad(_in: _CropPadInput) -> ResultUpscaledCropPad:
	"""The actual function for "Upscaled Crop/Pad" node - extracted to wrap it with displaying the message."""
	needs_resize, real_upscale_avg, real_upscale_x, real_upscale_y = _need_post_resize(_in.init_w, _in.init_h, _in.hd_w, _in.hd_h)
	if not needs_resize:
		return ResultUpscaledCropPad(
			real_upscale_avg,
			False, _in.hd_w, _in.hd_h, 0, 0,
			False, 0, 0, 0, 0,
		)

	_in.align_x = min(max(_in.align_x, 0.0), 1.0)
	_in.align_y = min(max(_in.align_y, 0.0), 1.0)

	if _in.strategy == UpscaledCropPadStrategy.CROP:
		return _upscaled_crop(_in, max(real_upscale_x, real_upscale_y))

	if _in.strategy == UpscaledCropPadStrategy.PAD:
		return _upscaled_pad(_in, min(real_upscale_x, real_upscale_y))

	if _in.strategy == UpscaledCropPadStrategy.NEAREST:
		crop_result = _upscaled_crop(_in, max(real_upscale_x, real_upscale_y))
		pad_result = _upscaled_pad(_in, min(real_upscale_x, real_upscale_y))
		return (
			pad_result
			if _upscaled_pad_delta_pixels(_in, pad_result) < _upscaled_crop_delta_pixels(_in, crop_result)
			else crop_result
		)

	assert _in.strategy == UpscaledCropPadStrategy.EXACT_UPSCALE

	upscale = _in.upscale
	raw_upscaled_w = _round_pos_int(upscale * _in.init_w)
	raw_upscaled_h = _round_pos_int(upscale * _in.init_h)
	# We're in the most complex case. These ^ can be both below and above the target up-res.
	# So, we need to follow the whole upscale->crop->pad chain: we'll just get zeroes where there will be nothing to do.

	cropped_w = min(_in.hd_w, raw_upscaled_w)
	cropped_h = min(_in.hd_h, raw_upscaled_h)
	crop_extra_w = raw_upscaled_w - cropped_w
	crop_extra_h = raw_upscaled_h - cropped_h
	crop_x_offset, crop_y_offset = _upscaled_crop_xy_offset(crop_extra_w, crop_extra_h, _in.align_x, _in.align_y)

	pad_extra_w = _in.hd_w - cropped_w
	pad_extra_h = _in.hd_h - cropped_h
	pad_side_values = _upscaled_pad_side_values(pad_extra_w, pad_extra_h, _in.align_x, _in.align_y)
	return ResultUpscaledCropPad(
		upscale,
		crop_extra_w > 0 or crop_extra_h > 0, cropped_w, cropped_h, crop_x_offset, crop_y_offset,
		pad_extra_w > 0 or pad_extra_h > 0, *pad_side_values,
	)


def upscaled_crop_pad(
	upscale: float,
	init_w: int, init_h: int, hd_w: int, hd_h: int,
	strategy: str,
	align_x: float, align_y: float,
	show: bool = True,
	unique_id: str = None
) -> ResultUpscaledCropPad:
	"""
	Detect, whether some cropping/out-painting needs to be done after upscaling the original image.
	And if so - what are the values for them.
	"""
	# noinspection PyArgumentList
	result = _upscaled_crop_pad(_CropPadInput(
		upscale,
		init_w, init_h, hd_w, hd_h,
		strategy,
		align_x, align_y,
	))

	if not unique_id:
		return result

	if not show:
		_show_text_on_node(None, unique_id)
		return result

	if not(result.do_crop or result.do_padding):
		_show_text_on_node(f"x{result.upscale:.3f}✅", unique_id)
		return result

	# Either crop, or pad, or both
	text_parts: _t.List[str] = [f"x{result.upscale:.3f}", ]

	if result.do_crop:
		crop_r = hd_w - (result.crop_x_origin + result.crop_width)
		crop_b = hd_h - (result.crop_y_origin + result.crop_height)
		text_parts.append(f"Crop:\nL {result.crop_x_origin}, R {crop_r}, B {crop_b}, T {result.crop_y_origin}")

	if result.do_padding:
		text_parts.append(f"Padding:\nL {result.pad_left}, R {result.pad_right}, B {result.pad_bottom}, T {result.pad_top}")

	_show_text_on_node('\n\n'.join(text_parts), unique_id)
	return result
