import json
import logging
import shutil
import time

from typing import Callable, Union, List
from autopipe import APData, Coordinator, ArgumentError, Output, Pipe, LogLevel
from .utils import to_dict


class Autopipe:
	def __init__(self, coordinator: str, coordinator_args: List[str],
	             log_level: LogLevel = LogLevel.WARN,
	             daemon: bool = False):
		logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level.value)
		self.interceptors = []

		coordinator_class = self.get_coordinator(coordinator)
		if coordinator_class is None:
			raise ArgumentError(f"Invalid coordinator: {coordinator}", "coordinator")
		self.coordinator = coordinator_class(*coordinator_args)
		self.pipeline = self.coordinator.pipeline

		self.step = 0
		while True:
			self.process_coordinator()
			sleep_time = self.coordinator.input.loop_cooldown
			if sleep_time <= 0 or not daemon:
				logging.info("Input generator finished. Closing now.")
				break
			logging.info(f"Input generator finished. Starting again in {sleep_time} seconds.")
			time.sleep(sleep_time)

	@staticmethod
	def get_coordinator(coordinator: str) -> Union[Callable, None]:
		if coordinator == "-":
			return None  # TODO support reading stdin as a coordinator file.
		try:
			import autopipe.coordinators as coordinators
			return getattr(coordinators, coordinator)
		except AttributeError:
			try:
				mod, cls = coordinator.split(':')
				module = __import__(mod)
				return getattr(module, cls)
			except Exception:
				return None

	def process_coordinator(self):
		logging.info(f"Starting input manager: {self.coordinator.input.name}")
		for data in self.coordinator.input:
			self.step = 0
			pipe = None
			while pipe is None or not isinstance(pipe, Output):
				pipe = self._process_input(self.coordinator, data)
				data = pipe if isinstance(pipe, APData) else pipe.pipe(data)
			logging.info("Pipeline finished")
			if data is not None:
				logging.debug(f"Output data (discarded): {json.dumps(to_dict(data), indent=4)}")
			logging.separator()

	def _process_input(self, coordinator: Coordinator, data: APData) -> Union[APData, Pipe]:
		logging.debug(f"Data: {json.dumps(to_dict(data), indent=4)}")

		interceptor = next((x for x in self.interceptors if x[1](data)), None)
		if interceptor:
			logging.info(f"Using interceptor: {interceptor.__name__}")
			return interceptor(data)

		if len(self.pipeline) > self.step:
			pipe = self.pipeline[self.step]
			self.step += 1
			if isinstance(pipe, Pipe):
				return pipe
			return pipe(data)

		logging.info(f"Using default handler.")
		return coordinator.default_handler(data)

	def interceptor(self, f, selector: Callable[[APData], bool]):
		self.interceptors.append((f, selector))
		return f
