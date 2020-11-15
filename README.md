# Autopipe
A tool that allow one to create pipeline of automatic data processing.

## How to use
To create a pipeline, you must create a Coordinator. To do so, create a file and a class implementing the base Coordinator class.
For example, here is the code for a simple coordinator that download images corresponding to a querry from google image.

```python3
from typing import List, Union, Callable
from autopipe import Coordinator, Pipe, APData, Output
from autopipe.input import RssInput
from autopipe.pipe import FileData, DownloaderPipe


class DownloadExample(Coordinator):
	def __init__(self, query: str = "raccoon"):
		super().__init__()
		self.query = query

	@classmethod
	def name(cls):
		return "DownloadExample"

	@property
	def input(self):
		return RssInput(f"http://www.obsrv.com/General/ImageFeed.aspx?{self.query}",
		                lambda x: FileData(None, x["media_content"][0]["url"], False))

	@property
	def pipeline(self) -> List[Union[Pipe, Callable[[APData], Union[APData, Pipe]]]]:
		return [Output(DownloaderPipe())]

```

### For this coordinator to be found by autopipe, you must use one of the three following way
 1) Place your coordinator file into the `autopipe/coordinators` folders, import your coordinator in the `autopipe/coordinators/__init__.py` file and place your coordinator name in the `__all__` array of this file.
 2) Run autopipe with the coordinator argument set to the path of your file followed by ':' and the coordinator's class name. For example if your coordinator's file is named `coordinator.py`, is located in the current directory and your coordinator's name is `DownloadExample`, your coordinator argument would be `../coordinator.py:DownloadExample`
 3) Send your coordinator file to the standard input of autopipe and use `-` as your coordinator name. *SOON*

### To run this, you have three ways
 1) Use the autopipe file in the bin folder like so: ``./autopipe <coordinator> [coordinator_parameters]``
 2) Use the module syntaxe like so: ``python -m autopipe <coordinator> [coordinator_parameters]``
 3) Use the shebang ``#!/usr/bin/env autopipe -``, set your coordinator file executable (``chmod +x file.py``) and execute it. *SOON*

## Coordinators options
A pipeline always start with an `Input`. You specify the instance of thte input manager you will use in the `get_input()` method.

An input will return one or multiples data that will be send to your pipeline one by one.

### The pipeline
Each item is send to the `Pipe` you specify in the `pipeline` property of your coordinator. In this property, you can place instances of pipes or functions that take a single `APData` as parameter and return an `APData` or a `Pipe`.
A pipeline is finished for an item when an `Output` pipe is reached. That can be by using one of the premade output or by wrapping a `Pipe` or an `APData` with an `Output()` call.

### Interceptors
You can add interceptors to your coordinator. An interceptor is a function that will be called between steps of your pipeline if the specified condition matches. This allow you to handle invalid cases of your data or specific cases that don't need a specific step in the pipeline. You can specify an interceptor using the `@autopipe.interceptor(lambda data: condition)` decorator.

### The default handler
A `default_handler` method can be specified in your coordinator. This special method will be called once the whole pipeline has been consumed but no Output has been returned. You can also use this method instead of the `pipeline` property by removing the property from your coordinator (or returning an empty list).

## Usage
```
usage: autopipe [-h] [-V] [-v [lvl]] [-d] [-w dir] coordinator [coordinator ...]

Easily run advanced pipelines in a daemon or in one run sessions.

positional arguments:
  coordinator          The name of your pipeline coordinator.

optional arguments:
  -h, --help           show this help message and exit
  -V, --version        show program's version number and exit
  -v, --verbose [lvl]  Set the logging level. (default: warn ; available: trace, debug, info, warning, error)
  -d, --daemon         Enable the daemon mode (rerun input generators after a sleep cooldown)
  -w, --workdir dir    Change the workdir, default is the pwd.
```

## Instalation
To install autopipe, run ``sudo pip install autopipe``. To use a developement version, you can clone this project and run ``pip install -e .``.
