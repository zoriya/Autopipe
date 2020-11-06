#!/usr/bin/env python3
import autopipe
import logging
from argparse import ArgumentParser


if __name__ == "__main__":
	parser = ArgumentParser(description="Easily run advanced pipelines in a daemon or in one run sessions.")
	parser.add_argument("coordinator", help="The name of your pipeline coordinator.")
	parser.add_argument("-v", "--verbose", choices=["debug", "info", "warn", "error"], nargs="?", const="info",
	                    default="warn", dest="log_level", metavar="loglevel",
	                    help="Set the logging level.", type=str.lower)
	args = parser.parse_args()

	autopipe.Autopipe(args.coordinator, log_level=getattr(logging, args.log_level.upper()))
