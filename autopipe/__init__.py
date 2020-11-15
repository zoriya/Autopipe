__all__ = ["Autopipe", "main",
           "LogLevel", "Coordinator", "Pipe", "Input", "APData", "Output",
           "ArgumentError",
           "input", "output", "pipe", "coordinators"]

from .logging import LogLevel
from .exceptions import ArgumentError
from .models import Coordinator, Pipe, Input, APData, Output
from .autopipe import Autopipe

version = 1.0
autopipe: Autopipe


def _parse_args(argv=None):
	from sys import argv as sysargv
	from argparse import ArgumentParser, HelpFormatter
	import os

	class CustomHelpFormatter(HelpFormatter):
		# noinspection PyProtectedMember
		def _format_action_invocation(self, action):
			if not action.option_strings or action.nargs == 0:
				return super()._format_action_invocation(action)
			default = self._get_default_metavar_for_optional(action)
			args_string = self._format_args(action, default)
			return ', '.join(action.option_strings) + ' ' + args_string

	def dir_path(path):
		if os.path.isdir(path):
			return path
		raise NotADirectoryError

	# noinspection PyTypeChecker
	parser = ArgumentParser(description="Easily run advanced pipelines in a daemon or in one run sessions.",
	                        formatter_class=CustomHelpFormatter)
	parser.add_argument("coordinator", help="The name of your pipeline coordinator.", nargs="+")
	parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {version}")
	parser.add_argument("-v", "--verbose", choices=list(LogLevel), nargs="?",
	                    const="info", default="warn", dest="level", metavar="lvl",
	                    help="Set the logging level. (default: warn ; available: %(choices)s)", type=LogLevel.parse)
	parser.add_argument("-d", "--daemon", help="Enable the daemon mode (rerun input generators after a sleep cooldown)",
	                    action="store_true")
	parser.add_argument("-w", "--workdir", help="Change the workdir, default is the pwd.", type=dir_path, metavar="dir")

	args = parser.parse_args(argv if argv is not None else sysargv[1:])
	if args.workdir is not None:
		os.chdir(args.workdir)
	return args


def main(argv=None):
	from sys import stderr
	from autopipe import Autopipe, ArgumentError, coordinators
	import logging

	args = _parse_args(argv)
	try:
		global autopipe
		autopipe = Autopipe(args.coordinator[0], args.coordinator[1:], log_level=args.level, daemon=args.daemon)
		return 0
	except ArgumentError as e:
		print(str(e), file=stderr)
		if e.flag is not None:
			e.print_more(args)
		return 2
	except KeyboardInterrupt:
		print("Interrupted by user", file=stderr)
		return 2
	except Exception as ex:
		logging.error(ex, exc_info=logging.getLogger().getEffectiveLevel() <= logging.INFO)
		return 1
