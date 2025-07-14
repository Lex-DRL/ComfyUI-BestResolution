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
	DESIRED = 'desired'
	ORIGINAL = 'original'
	UPSCALED = 'upscaled'


class UpscaleTweakStrategy(__BaseEnum):
	PAD = 'pad'
	CROP = 'crop'
	NEAREST = 'nearest'
	EXACT_UPSCALE = 'exact-upscale'
