from typing import Callable
from models import Pipe, APData


class FilterPipe(Pipe):
	def __init__(self, filter: Callable[[APData], bool]):
		super().__init__()
		self.filter = filter

	@property
	def name(self):
		return "Filter"

	def pipe(self, data: APData) -> APData:
		return data if self.filter(data) else None
