# encoding: utf-8
"""
"""

from .nodes import *

NODE_CLASS_MAPPINGS = {
	"BestResolutionFromArea": BestResolutionFromArea,
	"BestResolutionFromAreaUpscale": BestResolutionFromAreaUpscale,
	"BestResolutionFromAspectRatio": BestResolutionFromAspectRatio,
	"BestResolutionSimple": BestResolutionSimple,
}
NODE_DISPLAY_NAME_MAPPINGS = {
	"BestResolutionFromArea": "Best-Res (area)",
	"BestResolutionFromAreaUpscale": "Best-Res (area+scale)",
	"BestResolutionFromAspectRatio": "Best-Res (ratio)",
	"BestResolutionSimple": "Best-Res (simple)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
