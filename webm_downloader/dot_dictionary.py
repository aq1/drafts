class DotDictionary(dict):

    def __init__(self, init_value):
        if not isinstance(init_value, dict):
            raise TypeError('Expected dict, got {}'.format(type(init_value)))

        self._dict_to_self(init_value)
        super(DotDictionary, self).__init__()

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, val):
        if isinstance(val, dict):
            val = DotDictionary(val)
        self[name] = val

    def __setitem__(self, name, val):
        if isinstance(val, dict):
            val = DotDictionary(val)

        super(DotDictionary, self).__setitem__(name, val)

    def __delattr__(self, name):
        del self[name]

    def _dict_to_self(self, dct):
        for key, value in dct.items():
            if isinstance(value, (tuple, list)):
                for i, _ in enumerate(value):
                    if isinstance(value[i], dict):
                        value[i] = DotDictionary(value[i])
            self[key] = value
