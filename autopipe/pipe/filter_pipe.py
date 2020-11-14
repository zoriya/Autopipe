from typing import Callable
from autopipe.models import Pipe, APData


class FilterPipe(Pipe):
	def __init__(self, filter: Callable[[APData], bool]):
		self.filter = filter

	@property
	def name(self):
		return "Filter"

	def pipe(self, data: APData) -> APData:
		super().pipe(data)
		return data if self.filter(data) else None
