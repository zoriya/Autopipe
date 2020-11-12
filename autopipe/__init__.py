__all__ = ["Autopipe", "main",
           "Coordinator", "Pipe", "Input", "APData",
           "ArgumentError",
           "input", "output", "pipe", "coordinators"]

from .exceptions import ArgumentError
from .models import Coordinator, Pipe, Input, APData
from .autopipe import Autopipe

version = 1.0


def main(argv=None):
	import sys
	from autopipe import Autopipe, ArgumentError, coordinators
	import logging
	from argparse import ArgumentParser

	parser = ArgumentParser(description="Easily run advanced pipelines in a daemon or in one run sessions.")
	parser.add_argument("coordinator", help="The name of your pipeline coordinator.", nargs="+")
	parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {version}")
	parser.add_argument("-v", "--verbose", choices=["debug", "info", "warn", "error"], nargs="?", const="info",
	                    default="warn", dest="log_level", metavar="loglevel",
	                    help="Set the logging level.", type=str.lower)
	args = parser.parse_args(argv if argv is not None else sys.argv[1:])

	try:
		Autopipe(args.coordinator[0], args.coordinator[1:], log_level=getattr(logging, args.log_level.upper()))
		return 0
	except ArgumentError as e:
		logging.error(str(e))
		if e.flag == "coordinator":
			logging.error("Available coordinators:")
			for coordinator in coordinators.__all__:
				logging.error(f" - {coordinator.name()}")
		return 2
	except Exception as ex:
		logging.error(ex, exc_info=logging.getLogger().getEffectiveLevel() <= logging.INFO)
		return 1
