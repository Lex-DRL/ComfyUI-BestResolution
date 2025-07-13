# encoding: utf-8
"""
Internal enums.
"""

import typing as _t

try:
	from enum import StrEnum as _StrEnum
except ImportError:
	from comfy.comfy_types.node_typing import StrEnum as _StrEnum


class RoundingPriority(_StrEnum):
	DESIRED = 'desired'
	ORIGINAL = 'original'
	UPSCALED = 'upscaled'

	@classmethod
	def all_values(cls) -> _t.Tuple[str, ...]:
		return tuple(x.value for x in cls)
