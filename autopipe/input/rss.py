import logging
from datetime import datetime
from typing import Generator, Callable
from models import Input, APData
import feedparser


class RssInput(Input):
	def __init__(self, url: str, mapper: Callable[[[]], APData], start_from_now: bool = True):
		super().__init__()
		self.url = url
		self.mapper = mapper
		self.last_etag = None
		self.last_modified = datetime.now() if start_from_now else None

	@property
	def name(self):
		return "Rss"

	def generate(self) -> Generator[APData]:
		logging.debug(f"Pulling the rss feed at {self.url}, last etag: {self.last_etag}, modif: {self.last_modified}")
		feed = feedparser.parse(self.url, etag=self.last_etag, modified=self.last_modified)
		if feed.status != 304:
			for entry in feed.entries:
				yield self.mapper(entry)

	@property
	def loop_cooldown(self) -> int:
		return 300