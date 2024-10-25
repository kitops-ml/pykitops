from typing import TypeAlias

class RestrictedDict(dict):
    _KeyList: TypeAlias = list[str]

    def __init__(self, allowed_keys: _KeyList):
        super().__init__()
        self._allowed_keys = allowed_keys

    def __setitem__(self, key, value):
        if key in self._allowed_keys:
            super().__setitem__(key, value)
        else:
            raise KeyError(f"Key '{key}' is not allowed. Allowed keys are: {', '.join(self._allowed_keys)}")
