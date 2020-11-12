from .notify_example import NotifyExample

__all__ = [NotifyExample]


def __getattr__(name):
	obj = next((x for x in __all__ if x.name().casefold() == name.casefold()), None)
	if obj is None:
		raise AttributeError(f"No coordinator found with the name: {name}.")
	return obj
