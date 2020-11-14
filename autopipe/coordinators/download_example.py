from typing import List, Union, Callable
from autopipe import Coordinator, Pipe, APData, Output
from autopipe.input import RssInput
from autopipe.pipe import FileData, DownloaderPipe


class DownloadExample(Coordinator):
	def __init__(self, query: str = "raccoon"):
		super().__init__()
		self.query = query

	@classmethod
	def name(cls):
		return "NotifyExample"

	@property
	def pipeline(self) -> List[Union[Pipe, Callable[..., APData]]]:
		return [Output(DownloaderPipe())]

	def get_input(self):
		return RssInput(f"http://www.obsrv.com/General/ImageFeed.aspx?{self.query}",
		                lambda x: FileData(x.title, x["media:content"], True))
