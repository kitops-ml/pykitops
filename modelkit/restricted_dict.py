from typing import TypeAlias, Any, Dict, List, Set

class RestrictedDict(Dict[str,Any]):
    _Keys: TypeAlias = Set[str]

    def __init__(self, name:str, 
                 string_valued_keys:_Keys|None = None,
                 list_valued_keys:_Keys|None = None,
                 dict_valued_keys:_Keys|None = None,
                 data: Dict[str,Any]| None = None):
        super().__init__()

        # save the this dictionary's attributes
        self._name = name
        self._string_valued_keys = string_valued_keys or set()
        self._list_valued_keys = list_valued_keys or set()
        self._dict_valued_keys = dict_valued_keys or set()
        self._allowed_keys = \
            self._string_valued_keys.union(
                self._list_valued_keys).union(
                    self._dict_valued_keys)
        
        #return if the input data dict is empty
        if not data:
            return
        
        # raise an error if the input data isn't 
        # a dictionary
        if not isinstance(data, dict):
            raise TypeError(f"data: '{self._name}' is not a " +
                            "dictionary object")
        
        # raise an error if any unallowed keys are present
        # in the input data dict
        data_keys = set(data.keys())
        unallowed_keys = data_keys.difference(self._allowed_keys)
        if len(unallowed_keys) > 0:
            # some unallowed keys were present in the 
            # data dict, so raise an error
            raise KeyError(f"data: '{self._name}' contains " +
                            "the following invalid keys: " +
                            f"{', '.join(unallowed_keys)}. " +
                            "Allowed keys are: " +
                            f"{', '.join(self._allowed_keys)}.")
        
        # all keys in the data dict are allowed, so set
        # this dictionary's values from the data dict
        self.update(data)

    def __setitem__(self, key, value):
        # we still need to check for key validity anytime additional
        # updates are made to this dictionary
        if not (key in self._allowed_keys):
            raise KeyError(f"Key '{key}' is not allowed. " +
                           f"Allowed keys are: {', '.join(self._allowed_keys)}")
        
        # this item is safe to add
        super().__setitem__(key, value)

            
