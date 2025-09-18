# encoding: utf-8
"""
Pre-defined simple (non-combo) inputs for Node-v3, shared between nodes.
"""

import typing as _t

import sys as _sys

from comfy_api.latest import io as _io

from . import _tooltips as _tt

T_Widget = _t.TypeVar('T_Widget', bound=_io.WidgetInput)


def _int(id: str, default: int = 512, min: int = 1, max: int = _sys.maxsize, step: int = 1, **kwargs) -> _io.Int.Input:
	return _io.Int.Input(id, default=default, min=min, max=max, step=step, **kwargs)


def _io_override(input: T_Widget, id: str = None, **overrides) -> T_Widget:
	assert isinstance(input, _io.WidgetInput)
	tp = type(input)
	if not (isinstance(id, str) and id):
		id = input.id
	assert isinstance(id, str) and id

	kwargs = {k: v for k, v in input.as_dict().items() if k != 'id'}
	kwargs.update(overrides)
	return tp(id, **kwargs)


res = _int('res', default=1024)
step_default = _int('step_default', default=8)
step_init = _int('step_init', default=8*2*3, tooltip=_tt.step_init)
step_upscale1 = _int('step_upscale1', default=8*2*3*3, tooltip=_tt.step_upscale1)

rel_pos = _io.Float.Input('rel_pos', default=0.5, min=0.0, max=1.0, step=0.125, round=0.0001)
upscale = _io.Float.Input('upscale', default=1.5, min=1.0, max=_sys.float_info.max, step=0.25, round=0.0001)
scale = _io_override(upscale, 'scale', min=upscale.round)
aspect_a = _io.Float.Input('aspect_a', default=16.0, min=1.0, max=_sys.float_info.max, step=1.0, round=0.0001, tooltip=_tt.aspect)
aspect_b = _io_override(aspect_a, 'aspect_b', default=9.0)
toggle_size_is_big = _io.Boolean.Input('size_is_big', default=True, label_on='bigger', label_off='smaller', tooltip=_tt.toggle_size_is_big)
toggle_landscape = _io.Boolean.Input('landscape', default=True, label_on='landscape', label_off='portrait', tooltip=_tt.toggle_landscape)
