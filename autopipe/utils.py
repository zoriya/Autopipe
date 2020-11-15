from enum import Enum


def to_dict(obj):
	if isinstance(obj, Enum):
		return obj
	if isinstance(obj, dict):
		return {i: to_dict(j) for (i, j) in obj.items()}
	if hasattr(obj, "__dict__") and hasattr(obj, "__slots__"):
		return to_dict(dict([(i, getattr(obj, i)) for i in (list(obj.__slots__) + list(obj.__dict__)) if hasattr(obj, i)]))
	if hasattr(obj, "__dict__"):
		return to_dict(obj.__dict__)
	if hasattr(obj, "__slots__"):
		return to_dict({i: getattr(obj, i) for i in obj.__slots__})
	return obj
