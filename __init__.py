# encoding: utf-8
"""
"""

import typing as _t

from .node_crop_pad import BestResolutionUpscaledCropPad
from .node_scale import BestResolutionScale
from .node_upscale_by import ImageUpscaleByWithModel
from .nodes_prims import *
from .nodes_simple import *
from .nodes_upscale import *

NODE_CLASS_MAPPINGS: _t.Dict[str, type] = {
	"BestResolutionFromArea": BestResolutionFromArea,
	"BestResolutionFromAreaUpscale": BestResolutionFromAreaUpscale,
	"BestResolutionFromAspectRatio": BestResolutionFromAspectRatio,
	"BestResolutionSimple": BestResolutionSimple,

	"BestResolutionScale": BestResolutionScale,

	"BestResolutionPrimCropPadStrategy": BestResolutionPrimCropPadStrategy,
	"BestResolutionPrimResPriority": BestResolutionPrimResPriority,

	"BestResolutionUpscaledCropPad": BestResolutionUpscaledCropPad,

	"ImageUpscaleByWithModel": ImageUpscaleByWithModel,
}
NODE_DISPLAY_NAME_MAPPINGS: _t.Dict[str, str] = {
	"BestResolutionFromArea": "Best-Res (area)",
	"BestResolutionFromAreaUpscale": "Best-Res (area+scale)",
	"BestResolutionFromAspectRatio": "Best-Res (ratio)",
	"BestResolutionSimple": "Best-Res (simple)",

	"BestResolutionScale": "Scale (Best-Res)",

	"BestResolutionPrimCropPadStrategy": "Crop-Pad Strategy (Best-Res)",
	"BestResolutionPrimResPriority": "Priority (Best-Res)",

	"BestResolutionUpscaledCropPad": "Upscaled Crop/Pad (Best-Res)",

	"ImageUpscaleByWithModel": "Upscale Image By (with Model)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
