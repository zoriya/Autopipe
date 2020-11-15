import logging
import shutil
from enum import Enum
from logging import Logger


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


class APLogger(Logger):
	def trace(self, msg, *args, **kwargs):
		if self.isEnabledFor(LogLevel.TRACE.value):
			self._log(LogLevel.TRACE.value, msg, args, **kwargs)

	def separator(self, level: LogLevel = LogLevel.INFO):
		self.log(level.value, "=" * (shutil.get_terminal_size().columns - (len(level.name) + 2)))


logging.setLoggerClass(APLogger)
logging.addLevelName(LogLevel.TRACE.value, LogLevel.TRACE.name)
setattr(logging, LogLevel.TRACE.name, LogLevel.TRACE.value)
setattr(logging, "trace", lambda msg, *args, **kwargs: logging.log(LogLevel.TRACE.value, msg, *args, **kwargs))
setattr(logging, "separator", lambda level=LogLevel.INFO: logging.getLogger(__name__).separator(level))
