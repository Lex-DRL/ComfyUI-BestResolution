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

size_one_side = "Approximate size of one of the image sides.\nWhich one - see the 'size_is_big' and 'landscape' toggles."
size_square = (
	"The total resolution of the image would be the same as of a square with this side.\n"
	"The width and height would be such to respect aspect ratio, but also be as close as possible to the "
	"total number of pixels as in this square image.\n\n"
	"- 512x512 square (SD 1.5): ~0.25 megapixels\n"
	"- 1024x1024 square (SDXL): ~1 megapixel"
)

step_init = (
	"Both width and height will be divisible by this value - by rounding them "
	"to the closest appropriate resolution.\n\n"
	"The default 48 is (8 * 3 * 2), so it's a safe choice because:\n"
	"- it's compatible with SD1.5/XL downsampling factor (divisible by 8),\n"
	"- it can be upscaled by x1.5 or x1.333 at the first iteration, which is optimal for latent-upscale,\n"
	"- after x1.5 upscale, if you only do x2 later (it's OK for already high resolutions) - it will be divisible "
	"by 3 AND 9, which might become handy at that point, where you'll probably use UltimateSDUpscale.\n\n"
	"Other values worth trying first: 64, 96, 128."
)
step_upscale1 = "Same as the main `step`, but for the upscaled resolution.\n144 = 8 * 2 * 3 * 3",

aspect = (
	"Two aspects together define an aspect ratio (16:9, 4:3, etc).\n"
	"Order doesn't matter: image orientation is defined by the 'landscape' toggle.\n\n"
	"The specified aspect ratio is APPROXIMATE: step parameter has priority over the exact image proportions."
)
toggle_size_is_big = "When ON, size parameter represents the bigger image side.\nWhen OFF, it specifies the smaller one."
toggle_landscape = (
	"Specifies image orientation:\n\n"
	"When ON, width is bigger (image is horizontal).\n"
	"When OFF, height is bigger (image is vertical)."
)
