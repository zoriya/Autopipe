from autopipe import Coordinator
from autopipe.input import RssInput


class NotifyExample(Coordinator):
	def __init__(self, url, mapper):
		super().__init__()
		self.url = url
		self.mapper = mapper

	@classmethod
	def name(cls):
		return "NotifyExample"

	def get_input(self):
		return RssInput(self.url, self.mapper)
