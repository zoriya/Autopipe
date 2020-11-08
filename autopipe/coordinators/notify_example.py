from autopipe import Coordinator


class NotifyExample(Coordinator):
	@classmethod
	def name(cls):
		return "NotifyExample"
