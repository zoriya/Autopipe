import logging
from autopipe import available_coordinators, ArgumentError


class Autopipe:
	def __init__(self, coordinator, coordinator_args, log_level=logging.WARNING):
		logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
		coordinator_class = next((i for i in available_coordinators if i.name() == coordinator), None)
		if coordinator_class is None:
			raise ArgumentError(f"Invalid coordinator: {coordinator}", "coordinator")
		self.coordinator = coordinator_class(*coordinator_args)
