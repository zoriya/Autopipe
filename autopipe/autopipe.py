import logging
from autopipe import available_coordinators, ArgumentError


class Autopipe:
	def __init__(self, coordinator, coordinator_args, log_level=logging.WARNING):
		logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
		if coordinator not in available_coordinators:
			raise ArgumentError(f"Invalid coordinator: {coordinator}", "coordinator")
		self.coordinator = available_coordinators[coordinator](*coordinator_args)
