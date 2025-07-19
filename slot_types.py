# encoding: utf-8
"""
Pre-defined dictionaries for nice input types.
"""

import typing as _t

import sys as _sys

from comfy.comfy_types.node_typing import IO as _IO


def number_type_dict(default: int = 512, min: int = 1, max: int = _sys.maxsize, step: int = 1) -> _t.Dict[str, int]:
	"""Prepare type-dict for an input int/float parameter."""

	# sys.maxsize is Py3's closest equivalent to 'sys.maxint' from Py2
	return {
		"default": default,
		"min": min,
		"max": max,
		"step": step
	}


type_dict_res = number_type_dict(1024)
type_dict_step_init = number_type_dict(48)
type_dict_step_upscale1 = number_type_dict(128)

upscale_in_type = (_IO.FLOAT, {
	'default': 1.5, 'min': 1.0, 'max': _sys.float_info.max, 'step': 0.25, 'round': 0.001,
	# 'tooltip': "",  # TODO
})
rel_pos_in_type = (_IO.FLOAT, {
	'default': 0.5, 'min': 0.0, 'max': 1.0, 'step': 0.125, 'round': 0.0001,
	# 'display': 'slider', # Cosmetic only: display as 'number' or 'slider'
})
