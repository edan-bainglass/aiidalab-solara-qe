from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from solara import Reactive, reactive


class ReactiveMeta(type):
    def __new__(cls, name, bases, class_dict):
        def make_reactive(class_dict: dict):
            new_dict = {}
            for key, value in class_dict.items():
                if (
                    not key.startswith("__")  # built-in method/property
                    and not callable(value)  # added method/property
                    and not hasattr(value, "__annotations__")  # nested reactive class
                ):
                    new_dict[key] = reactive(value)
                else:
                    new_dict[key] = value
            return new_dict

        return super().__new__(cls, name, bases, make_reactive(class_dict))


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class ReactiveDataclass:
    def __init__(self, **data):
        for key, value in data.items():
            setattr(getattr(self, key), "value", value)

    def __post_init__(self):
        print("hello")

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{key}={getattr(self, key).value}' for key in self.__annotations__.keys()])})"

    def __getattr__(self, name):
        attr = getattr(self, name)
        if isinstance(attr, Reactive):
            return attr.value
        return attr

    def __setattr__(self, name: str, value) -> None:
        attr = getattr(self, name)
        if isinstance(attr, Reactive):
            setattr(attr, "value", value)
        attr = value
