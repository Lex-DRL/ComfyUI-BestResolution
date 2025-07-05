# encoding: utf-8
"""
"""

import typing as _t

import sys as _sys


def number_type_dict(default: int = 512, min: int = 1, max: int = _sys.maxsize, step: int = 1) -> _t.Dict[str, int]:
	"""Prepare type-dict for an input int/float parameter."""

	# sys.maxsize is Py3's closest equivalent to 'sys.maxint' from Py2
	return {
		"default": default,
		"min": min,
		"max": max,
		"step": step
	}


type_dict_step_init = number_type_dict(48)
type_dict_step_upscale1 = number_type_dict(128)
type_dict_res = number_type_dict(1024)
