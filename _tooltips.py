# encoding: utf-8
"""
Pre-defined tooltips, shared between node inputs.
"""

upscale = (
	"If the HD resolution can be achieved by uniformly scaling the initial one "
	"(there is \"✅\" and not \"⚠️\" in the upscale-line of the status message), "
	"outputs this precise upscale-value (might be different from the one originally set on the node itself).\n\n"
	"Otherwise, outputs the original upscale-value intact.\n"
	"In this case, you shouldn't use it directly and instead should pass it "
	"to the \"Upscaled Crop/Pad (Best-Res)\" node and use the upscale-output from it.\n\n"
	"In both cases, it won't hurt to use the \"Upscaled Crop/Pad (Best-Res)\" node and just rely "
	"on it's `do_crop` and `do_padding` toggle-outputs."
)
init_width = "Width for original/initial image"
init_height = "Height for original/initial image"
HD_width = "Width for the (main/upscaled) HD-image"
HD_height = "Height for the (main/upscaled) HD-image"
