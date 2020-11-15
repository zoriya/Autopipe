from abc import ABC, abstractmethod
from typing import Generator, List, Union, Callable
from autopipe import ArgumentError
import logging


class APData(ABC):
	@property
	@abstractmethod
	def type(self):
		raise NotImplementedError


class Pipe(ABC):
	@property
	@abstractmethod
	def name(self):
		raise NotImplementedError

	def pipe(self, data: APData) -> APData:
		logging.info(f"Entering pipe: {self.name}")
		return data

	def __call__(self, data: APData) -> APData:
		return self.pipe(data)


class Input(ABC):
	@property
	@abstractmethod
	def name(self):
		raise NotImplementedError

	@abstractmethod
	def generate(self) -> Generator[APData, None, None]:
		raise NotImplementedError

	@property
	@abstractmethod
	def loop_cooldown(self) -> int:
		"""
		If negative or 0, the input can't be chained and once the generator return the program will exit.
		If grater then 0, the generator will be called again after a sleep of x seconds where x is the return of this.
		"""
		raise NotImplementedError

	def __iter__(self):
		return self.generate()


class Output(Pipe):
	def __init__(self, pipe: Union[Pipe, Callable[[APData], APData], APData] = None):
		if callable(pipe):
			self.pipe = pipe
			self.output = None
		else:
			self.output = pipe
			self.pipe = None

	@property
	def name(self):
		if self.pipe is None:
			if self.output:
				return "Static output"
			raise NotImplementedError
		return self.pipe.name if isinstance(self.pipe, Pipe) else self.pipe.__name__

	def pipe(self, data: APData) -> APData:
		super().pipe(data)
		if self.pipe is None:
			if self.output:
				return self.output
			raise NotImplementedError
		return self.pipe(data)


class Coordinator(ABC):
	def __init__(self):
		logging.info(f"Using coordinator: {self.name()}")

	@classmethod
	@abstractmethod
	def name(cls):
		raise NotImplementedError

	@property
	@abstractmethod
	def input(self) -> Input:
		raise NotImplementedError

	@property
	def pipeline(self) -> List[Union[Pipe, Callable[[APData], Union[APData, Pipe]]]]:
		return []

	def default_handler(self, data: APData) -> Union[Pipe, Callable[[APData], Union[APData, Pipe]]]:
		raise ArgumentError(f"No default argument handler for this coordinator, did you forget an Output() wrapper?")
