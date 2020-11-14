__all__ = ["Autopipe", "main",
           "Coordinator", "Pipe", "Input", "APData", "Output",
           "ArgumentError",
           "input", "output", "pipe", "coordinators"]

from sys import stderr

from .exceptions import ArgumentError
from .models import Coordinator, Pipe, Input, APData, Output
from .autopipe import Autopipe

version = 1.0
autopipe: Autopipe


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
	parser.add_argument("-d", "--daemon", help="Enable the daemon mode (rerun input generators after a sleep cooldown",
	                    action="store_true")
	args = parser.parse_args(argv if argv is not None else sys.argv[1:])

	try:
		global autopipe
		autopipe = Autopipe(args.coordinator[0], args.coordinator[1:],
		                    log_level=getattr(logging, args.log_level.upper()),
		                    daemon=args.daemon)
		return 0
	except ArgumentError as e:
		print(str(e), file=stderr)
		if e.flag == "coordinator":
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
		return 2
	except KeyboardInterrupt:
		print("Interrupted by user", file=stderr)
		return 2
	except Exception as ex:
		logging.error(ex, exc_info=logging.getLogger().getEffectiveLevel() <= logging.INFO)
		return 1
