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
		return "DownloadExample"

	@property
	def input(self):
		return RssInput(f"http://www.obsrv.com/General/ImageFeed.aspx?{self.query}",
		                lambda x: FileData(None, x["media_content"][0]["url"], False))

	@property
	def pipeline(self) -> List[Union[Pipe, Callable[[APData], Union[APData, Pipe]]]]:
		return [Output(DownloaderPipe())]
