# encoding: utf-8
"""
"""

import typing as _t

from dataclasses import dataclass as dataclass_with_slots_if_possible
from sys import version_info as _version_info

if _version_info > (3, 10):
	_dataclass_raw = dataclass_with_slots_if_possible

	def dataclass_with_slots_if_possible(*args, **kwargs):
		kwargs['slots'] = True
		return _dataclass_raw(*args, **kwargs)
