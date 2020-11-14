import logging

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
	@property
	def name(self):
		return "Downloader"

	def pipe(self, data: FileData) -> FileData:
		super().pipe(data)
		if data.is_local:
			return data
		# if not force_refresh and os.path.isfile(path):
		# 	if not read:
		# 		return
		# 	with open(path, "r") as f:
		# 		return StringIO(f.read())
		#
		# if message:
		# 	print(message)
		# r = requests.get(url, stream=progress)
		# try:
		# 	Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
		# 	with open(path, "wb") as f:
		# 		length = r.headers.get("content-length")
		# 		if progress and length:
		# 			local = 0
		# 			length = int(length)
		# 			for chunk in r.iter_content(chunk_size=4096):
		# 				f.write(chunk)
		# 				local += len(chunk)
		# 				per = 50 * local // length
		# 				print(f"\r [{'#' * per}{'-' * (50 - per)}] ({sizeof_fmt(local)}/{sizeof_fmt(length)})       \r",
		# 				      end='', flush=True)
		# 		else:
		# 			f.write(r.content)
		# 		if read:
		# 			return StringIO(r.content.decode(encoding))
		# except KeyboardInterrupt:
		# 	os.remove(path)
		# 	if progress:
		# 		print()
		# 	print("Download cancelled")
		# 	raise
		data.is_local = True
		return data
