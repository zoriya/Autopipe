class ArgumentError(Exception):
	def __init__(self, msg, flag=None):
		self.msg = msg
		self.flag = flag

	def __str__(self):
		return self.msg
