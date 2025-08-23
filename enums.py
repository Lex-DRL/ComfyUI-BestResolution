# encoding: utf-8
"""
Internal enums: option choices, shared between nodes.
"""

try:
	from enum import StrEnum as _StrEnum
except ImportError:
	from comfy.comfy_types.node_typing import StrEnum as _StrEnum

from abc import ABCMeta as _ABCMeta, abstractmethod as _abstractmethod


class __BaseEnum(_StrEnum, metaclass=_ABCMeta):
	@classmethod
	def all_values(cls) -> tuple[str, ...]:
		return tuple(x.value for x in cls)

	@classmethod
	@_abstractmethod
	def validate(cls, value) -> str:
		raise NotImplementedError


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

	@classmethod
	def validate(cls, value) -> str:
		if value not in _res_priority_values_set:
			raise ValueError(f"Invalid value for resolution priority: {value!r}\nExpected one of: {_res_priority_values!r}")
		return str(value)


_res_priority_values = RoundingPriority.all_values()
_res_priority_values_set = set(_res_priority_values)
_res_priority_validate = RoundingPriority.validate


class UpscaledCropPadStrategy(__BaseEnum):
	"""
	If the upscaled resolution can't be achieved by uniform scaling of the initial-res,
	how to tweak the image to get there:


	• pad only - upscale the image to fit it into the desired frame on one side,
	then add missing pixels on the other one for outpaint.
	• crop only - upscale the image to fill the entire frame, then crop extra pixels on one side.
	• nearest - automatically choose one of the above, to crop/pad the least number of pixels (by area).
	• exact-upscale - follow the provided upscale-value precisely. This is the only option
	that uses it. Also, it's the only one that might require both outpainting and crop.

	In case when both are required, the output values assume this order: upscale -> crop -> pad.
	"""
	PAD = 'pad only'
	CROP = 'crop only'
	NEAREST = 'nearest'
	EXACT_UPSCALE = 'exact-upscale'

	@classmethod
	def validate(cls, value) -> str:
		if value not in _up_strategy_values_set:
			raise ValueError(f"Invalid value for upscale strategy: {value!r}\nExpected one of: {_up_strategy_values!r}")
		return str(value)


_up_strategy_values = UpscaledCropPadStrategy.all_values()
_up_strategy_values_set = set(_up_strategy_values)
_up_strategy_validate = UpscaledCropPadStrategy.validate
