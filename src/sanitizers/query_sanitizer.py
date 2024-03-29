import re


class QuerySanitizer:
    def __init__(self, **kwargs):
        pattern = re.compile(r'(.*)\[(.*)\]')
        keys = list(filter(pattern.findall, kwargs.keys()))
        eq = {k: v for k, v in kwargs.items() if k not in keys}
        my_list = [pattern.findall(k) for k in keys]

        for i, pack in enumerate(my_list):
            k, v = pack[0]
            value = self._changeValuesType(kwargs[keys[i]])
            if k == '_orderBy':
                v = v == 'asc'
                # Arguments are set in opposite way. The reason behind this is that in case of gt or lt, it creates
                # dict like {'gt': {'key': 'value'}} to allow one-command filter later Here we need to create
                # {'_orderBy': {'key': True}} if 'asc'
                self._setDictAttr(k=value, v=k, value=v)
            else:
                self._setDictAttr(k, v, value)

        self._setEqAttr(eq)

    @staticmethod
    def _changeValuesType(s: str):
        try:
            f = float(s)
            return f
        except ValueError:
            return s

    def _setDictAttr(self, k, v, value):
        if hasattr(self, v):
            setattr(self, v, dict(getattr(self, v), **{k: value}))
        else:
            setattr(self, v, {k: value})

    def _setEqAttr(self, eq):
        for k, v in eq.items():
            v = self._changeValuesType(v, )
            setattr(self, k, v)
