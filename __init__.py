# encoding: utf-8
"""
"""

import typing as _t

from .node_crop_pad import BestResolutionUpscaledCropPad
from .nodes_prims import *
from .nodes_simple import *
from .nodes_upscale import *

NODE_CLASS_MAPPINGS: _t.Dict[str, type] = {
	"BestResolutionFromArea": BestResolutionFromArea,
	"BestResolutionFromAreaUpscale": BestResolutionFromAreaUpscale,
	"BestResolutionFromAspectRatio": BestResolutionFromAspectRatio,
	"BestResolutionSimple": BestResolutionSimple,

	"BestResolutionPrimResPriority": BestResolutionPrimResPriority,
	"BestResolutionPrimUpStrategy": BestResolutionPrimUpStrategy,

	"BestResolutionUpscaledCropPad": BestResolutionUpscaledCropPad,
}
NODE_DISPLAY_NAME_MAPPINGS: _t.Dict[str, str] = {
	"BestResolutionFromArea": "Best-Res (area)",
	"BestResolutionFromAreaUpscale": "Best-Res (area+scale)",
	"BestResolutionFromAspectRatio": "Best-Res (ratio)",
	"BestResolutionSimple": "Best-Res (simple)",

	"BestResolutionPrimResPriority": "Priority (Best-Res)",
	"BestResolutionPrimUpStrategy": "Upscale Strategy (Best-Res)",

	"BestResolutionUpscaledCropPad": "Upscaled Crop/Pad (Best-Res)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
