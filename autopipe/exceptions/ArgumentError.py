from sys import stderr


class ArgumentError(Exception):
	def __init__(self, msg, flag=None):
		self.msg = msg
		self.flag = flag

	def __str__(self):
		return self.msg

	def print_more(self, args):
		if self.flag == "coordinator":
			import autopipe.coordinators as coordinators
			print("Available coordinators:", file=stderr)
			for coordinator in coordinators.__all__:
				print(f"\t{coordinator.name()}", file=stderr)
			if ':' in args.coordinator[0]:
				try:
					file, cls = args.coordinator[0].split(':')
				except ValueError:
					print(f"{args.coordinator[0]} is not a valid syntax. Did you meant to use file:class?", file=stderr)
					return 2
				print(f"Coordinators of ${file}:")
				module = __import__(file)
				for coordinator in module.__all__:
					print(f"\t{coordinator.name()}", file=stderr)
			else:
				print("Or you can input a file anywhere on the system with the syntax: path/to/file.py:coordinator",
				      file=stderr)
