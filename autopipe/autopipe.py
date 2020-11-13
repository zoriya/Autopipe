import logging
import autopipe.coordinators as coordinators
from typing import Callable, List, Union

from autopipe import APData, Coordinator, ArgumentError


class Autopipe:
	def __init__(self, coordinator, coordinator_args, log_level=logging.WARNING):
		logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
		self.handlers = []

		coordinator_class = self.get_coordinator(coordinator, coordinator_args)
		if coordinator_class is None:
			raise ArgumentError(f"Invalid coordinator: {coordinator}", "coordinator")
		self.coordinator = coordinator_class(*coordinator_args)

		for data in self.coordinator.get_input():
			self._process_input(self.coordinator, data)

	@staticmethod
	def get_coordinator(coordinator: str, args: List[str]) -> Union[Callable, None]:
		if coordinator == "-":
			return None  # TODO support reading stdin as a coordinator file.
		try:
			return getattr(coordinators, coordinator)
		except AttributeError:
			try:
				module = __import__(coordinator)
				coordinator_class = getattr(module, args[0])
				del args[0]
				return coordinator_class
			except Exception:
				return None

	def _process_input(self, coordinator: Coordinator, data: APData) -> APData:
		logging.debug(data)
		handler = next((x for x in self.handlers if x[1](data)), None)
		if handler is None:
			return coordinator.default_handler(data)
		# TODO rename handler interceptors
		# TODO use a pipe array as the base pipe selector
		# TODO allow anonymous pipe (a function instead of a pipe in the array)
		# TODO use the Output() class to end the pipeline, without this the default_handler is used for next items
		# TODO change the default_handler error to ask if the Output() was forgotten
		return handler(data)

	def pipe_handler(self, f, selector: Callable[[APData], bool]):
		self.handlers.append((f, selector))
		return f
