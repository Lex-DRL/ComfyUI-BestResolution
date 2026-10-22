# encoding: utf-8
"""
"""

try:
	# To let the internal non-comfy functions be used without comfy itself
	from comfy_api.latest import ComfyExtension as _ComfyExtension, io as _io
	from typing_extensions import override as _override

	class BestResolutionExtension(_ComfyExtension):
		@_override
		async def get_node_list(self) -> list[type[_io.ComfyNode]]:
			from .node_crop_pad import BestResolutionUpscaledCropPad
			from .node_scale import BestResolutionScale
			from .node_upscale_by import ImageUpscaleByWithModel
			from .nodes_prims import BestResolutionPrimResPriority, BestResolutionPrimCropPadStrategy
			from .nodes_simple import BestResolutionSimple, BestResolutionFromAspectRatio, BestResolutionFromArea
			from .nodes_upscale import BestResolutionFromAreaUpscale

			return [
				BestResolutionFromArea,
				BestResolutionFromAreaUpscale,
				BestResolutionFromAspectRatio,
				BestResolutionSimple,

				BestResolutionScale,

				BestResolutionPrimCropPadStrategy,
				BestResolutionPrimResPriority,

				BestResolutionUpscaledCropPad,

				ImageUpscaleByWithModel,
			]
except ImportError:
	class BestResolutionExtension:
		pass

async def comfy_entrypoint() -> BestResolutionExtension:
	return BestResolutionExtension()

__all__ = ("BestResolutionExtension", "comfy_entrypoint")
