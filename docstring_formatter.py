# encoding: utf-8
"""
"""

import typing as _t

from inspect import getdoc as _getdoc
import re as _re

from ._dataclass import dataclass_with_slots_if_possible as _dataclass_with_slots_if_possible


_re_indent_match = _re.compile("(\t*)( +)(\t*)(.*?)$").match
_re_tab_indent_match = _re.compile("(\t+)(.*?)$").match


@_dataclass_with_slots_if_possible
class DocStringFormatter:
	"""
	Function-like (callable) class. Turn a pre-cleaned-up docstring (with tabs as spaces and newlines mid-sentence)
	into an actually printable output.

	Remember to call the class instance - i.e., ``DocStringFormatter(inspect.cleandoc(__doc__))()``
	"""
	doc: str
	tab_size: int = 8

	def __recover_tab_indents(self, line: str):
		"""Turn indenting spaces back to tabs using regexp. Half-tab indents are rounded."""
		assert bool(line) and isinstance(line, str)

		tab_size = self.tab_size
		n_tabs = 0.0

		match = _re_indent_match(line)
		while match:
			pre_tabs, spaces, post_tabs, line = match.groups()
			n_tabs_from_spaces = float(len(spaces)) / tab_size + 0.00001
			n_post_tabs = len(post_tabs)
			if n_post_tabs > 0:
				# There are tabs after spaces. Don't preserve the fractional spaces-indent, truncate it:
				n_tabs_from_spaces = int(n_tabs_from_spaces)
			n_tabs += len(pre_tabs) + n_tabs_from_spaces + n_post_tabs
			match = _re_indent_match(line)

		if n_tabs < 0.5:
			return line

		tabs_prefix = '\t' * int(n_tabs + 0.50001)
		return f"{tabs_prefix}{line}"

	def __join_paragraph_and_format_tabs(self, paragraph: _t.List[str]):
		"""
		Given "continuous" paragraph (i.e., with no empty newlines between chunks), recover tabs for each chunk
		and join them together into a single actual line.
		Works as a generator to account for blocks with different indents - to make each its own line.
		"""
		_recover_tab_indents = self.__recover_tab_indents

		pending_indent = 0
		pending_chunks: _t.List[str] = list()

		def join_pending_chunks() -> str:
			return "{}{}".format('\t' * pending_indent, ' '.join(pending_chunks))

		for chunk in paragraph:
			chunk = _recover_tab_indents(chunk)

			cur_indent = 0
			match = _re_tab_indent_match(chunk)
			if match:
				tab_indent, chunk = match.groups()  # We've detected indent. Now, get rid of it.
				cur_indent = len(tab_indent)

			if cur_indent == pending_indent:
				pending_chunks.append(chunk)
				continue

			# Indent mismatch - we're either ended one block or entered another. Either way, the previous block ends.
			if pending_chunks:
				yield join_pending_chunks()
				pending_chunks = list()

			assert not pending_chunks
			pending_chunks.append(chunk)
			pending_indent = cur_indent

		if pending_chunks:
			yield join_pending_chunks()

	def __formatted_paragraphs_gen(self):
		"""
		Generator, which splits docstring into lines and transforms them into an actual printable output:
		- From each bulk of empty lines, the first one is skipped...
		- ... thus, non-empty lines are joined into continuous paragraphs.
		- Recover tabs in the beginning oh lines (``inspect.cleandoc()`` converts them into spaces).
		"""
		doc = self.doc
		if not doc:
			return
		doc = str(doc)
		if not doc.strip():
			return

		self.tab_size = max(int(self.tab_size), 1)

		_join_paragraph_and_format_tabs = self.__join_paragraph_and_format_tabs
		cur_paragraph: _t.List[str] = list()

		for line in doc.splitlines():
			line: str = line.rstrip()
			if line:
				cur_paragraph.append(line)
				continue

			assert not line
			if cur_paragraph:
				for block in _join_paragraph_and_format_tabs(cur_paragraph):
					yield block
				cur_paragraph = list()
				# Just skip the current empty line entirely - do nothing with it.
				continue

			# We're in a chain of empty lines, and we've already skipped the first one. Preserve the remaining ones:
			yield ''

		# Return the last paragraph post-loop:
		if cur_paragraph:
			for block in _join_paragraph_and_format_tabs(cur_paragraph):
				yield block

	def __call__(self):
		return '\n'.join(self.__formatted_paragraphs_gen())

	@classmethod
	def from_object(cls, _obj, tab_size: int = 8):
		doc = _getdoc(_obj)
		if not doc:
			return ''
		# noinspection PyArgumentList
		return cls(doc, tab_size=tab_size)()
