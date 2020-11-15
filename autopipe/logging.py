import logging
from enum import Enum


class LogLevel(Enum):
	TRACE = 5
	VV = 5
	DEBUG = logging.DEBUG
	V = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARN
	WARN = logging.WARN
	ERROR = logging.ERROR

	def __str__(self):
		return self.name.lower()

	@classmethod
	def parse(cls, x):
		for name, value in cls.__members__.items():
			if x.upper() == name:
				return value


def _log(self, msg, *args, **kwargs):
	if self.isEnabledFor(LogLevel.TRACE.value):
		self._log(LogLevel.TRACE.value, msg, args, **kwargs)


logging.addLevelName(LogLevel.TRACE.value, LogLevel.TRACE.name)
setattr(logging, LogLevel.TRACE.name, LogLevel.TRACE.value)
setattr(logging.getLoggerClass(), "trace", _log)
setattr(logging, "trace", lambda msg, *args, **kwargs: logging.log(LogLevel.TRACE.value, msg, *args, **kwargs))
