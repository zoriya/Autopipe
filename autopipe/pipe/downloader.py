import os
from pathlib import Path

import requests

from autopipe import Pipe, APData


class FileData(APData):
	def __init__(self, name, link, is_locale=True):
		self.name = name
		self.link = link
		self.is_local = is_locale

	@property
	def type(self):
		return "File"


class DownloaderPipe(Pipe):
	def __init__(self, cwd=None):
		self.cwd = cwd if cwd is not None else os.getcwd()
		Path(self.cwd).mkdir(parents=True, exist_ok=True)

	@property
	def name(self):
		return "Downloader"

	def pipe(self, data: FileData) -> FileData:
		super().pipe(data)
		if data.is_local:
			return data
		path = os.path.join(self.cwd, data.name if data.name is not None else data.link.split('/')[-1])
		try:
			r = requests.get(data.link)
			with open(path, "wb") as f:
				f.write(r.content)
		except KeyboardInterrupt:
			os.remove(path)
			raise
		data.is_local = True
		return data
