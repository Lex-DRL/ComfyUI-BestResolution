# encoding: utf-8
"""
Compatibility layer for dataclasses in different py3 versions.
"""

from sys import version_info as __version_info

slots_args = dict() if __version_info < (3, 10) else dict(slots=True)
