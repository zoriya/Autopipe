import logging


class Autopipe:
	def __init__(self, coordinator, log_level=logging.WARNING):
		logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
		print("Hello from autopipe")
		logging.info(f"Using coordinator: {coordinator}")
