# encoding: utf-8
"""
"""

from .nodes import *

NODE_CLASS_MAPPINGS = {
	"BestResolutionSimple": BestResolutionSimple,
	"BestResolutionFromAspectRatio": BestResolutionFromAspectRatio,
}
NODE_DISPLAY_NAME_MAPPINGS = {
	"BestResolutionSimple": "Best-Res (simple)",
	"BestResolutionFromAspectRatio": "Best-Res (ratio)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
