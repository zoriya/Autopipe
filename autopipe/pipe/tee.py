from autopipe.models import Pipe, APData


class TeePipe(Pipe):
	def __init__(self, *outputs):
		self.outputs = outputs

	@property
	def name(self):
		return "Tee"

	def pipe(self, data: APData) -> APData:
		super().pipe(data)
		for output in self.outputs:
			output.pipe(data)
		return data
