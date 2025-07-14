# encoding: utf-8
"""
"""

import typing as _t

from .nodes_simple import *
from .nodes_upscale import *
from .nodes_prims import *

NODE_CLASS_MAPPINGS: _t.Dict[str, type] = {
	"BestResolutionFromArea": BestResolutionFromArea,
	"BestResolutionFromAreaUpscale": BestResolutionFromAreaUpscale,
	"BestResolutionFromAspectRatio": BestResolutionFromAspectRatio,
	"BestResolutionSimple": BestResolutionSimple,

	"BestResolutionPrimResPriority": BestResolutionPrimResPriority,
	"BestResolutionPrimUpStrategy": BestResolutionPrimUpStrategy,
}
NODE_DISPLAY_NAME_MAPPINGS: _t.Dict[str, str] = {
	"BestResolutionFromArea": "Best-Res (area)",
	"BestResolutionFromAreaUpscale": "Best-Res (area+scale)",
	"BestResolutionFromAspectRatio": "Best-Res (ratio)",
	"BestResolutionSimple": "Best-Res (simple)",

	"BestResolutionPrimResPriority": "Priority (Best-Res)",
	"BestResolutionPrimUpStrategy": "Upscale Strategy (Best-Res)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
