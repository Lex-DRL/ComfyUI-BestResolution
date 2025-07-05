# encoding: utf-8
"""
"""

from .nodes import *

NODE_CLASS_MAPPINGS = {
	"BestResolutionSimple": BestResolutionSimple,
}
NODE_DISPLAY_NAME_MAPPINGS = {
	"BestResolutionSimple": "Best-Res (simple)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
