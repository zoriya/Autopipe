from autopipe import Coordinator
from autopipe.input import RssInput
from autopipe.pipe import FileData


class NotifyExample(Coordinator):
	def __init__(self, query):
		super().__init__()
		self.query = query

	@classmethod
	def name(cls):
		return "NotifyExample"

	def get_input(self):
		return RssInput(f"http://www.obsrv.com/General/ImageFeed.aspx?{self.query if self.query else 'raccoon'}",
		                lambda x: FileData(x.title, x["media:content"], True))
