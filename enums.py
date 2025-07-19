# encoding: utf-8
"""
Internal enums.
"""

import typing as _t

try:
	from enum import StrEnum as _StrEnum
except ImportError:
	from comfy.comfy_types.node_typing import StrEnum as _StrEnum


class __BaseEnum(_StrEnum):
	@classmethod
	def all_values(cls) -> _t.Tuple[str, ...]:
		return tuple(x.value for x in cls)


class RoundingPriority(__BaseEnum):
	"""
	Defines what resolution to prioritize, as well as which order to perform rounding in:


	• desired - first, approximate resolutions are calculated for both initial and upscaled size; then, both are rounded.
	In both cases, the rounded resolution is closest to the desired one,
	but aspect ratio might differ the most between sizes.
	• original - first, initial resolution is calculated and rounded; then, upscaled one is detected from it.
	Upscaled resolution might differ the most from the desired aspect ratio, but it follows the ratio from
	initial size as much as possible.
	• upscaled - vice versa: first, the rounded upscaled resolution is calculated;
	then, the initial one back-tracked from it.
	"""
	DESIRED = 'desired'
	ORIGINAL = 'original'
	UPSCALED = 'upscaled'


class UpscaledCropPadStrategy(__BaseEnum):
	"""
	If the upscaled resolution can't be achieved by uniform scaling of the initial-res,
	how to tweak the image to get there:


	• pad - upscale the image to fit it into the desired frame on one side,
	then add missing pixels on the other one for outpaint.
	• crop - upscale the image to fill the entire frame, then crop extra pixels on one side.
	• nearest - automatically choose one of the above, to crop/pad the least number of pixels.
	• exact-upscale - follow the provided upscale-value precisely. This is the only option
	that uses it. Also, it's the only one that might require both outpainting and crop.
	"""
	PAD = 'pad'
	CROP = 'crop'
	NEAREST = 'nearest'
	EXACT_UPSCALE = 'exact-upscale'
