from ..module import Module
from ...utils import is_number

CLASS_NAME = 'Transient'


class Transient(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keys = kwargs.get('keys', '')

    def process(self, **kwargs):
        return self._data

    def set_data(self, all_data, req_key_values={}, subtract_minimum_keys=[]):
        self._all_data = all_data
        self._data = {}
        if not self._all_data:
            return
        name = list(self._all_data.keys())[0]
        for key in self._keys:
            subdata = self._all_data[name][key]
            subkeys = self._keys[key]
            # Only include data that contains all subkeys
            for entry in subdata:
                if any([x not in entry for x in subkeys]):
                    continue
                skip_key = False
                for qkey in req_key_values:
                    if (qkey in entry and
                            entry[qkey] not in req_key_values[qkey]):
                        skip_key = True
                        break
                if skip_key:
                    continue
                for x in subkeys:
                    if x == 'value':
                        self._data[key] = entry[x]
                    else:
                        self._data.setdefault(x + 's', []).append(entry[x])

        for key in self._data.copy():
            if isinstance(self._data[key], list):
                if not all(is_number(x) for x in self._data[key]):
                    continue
                self._data[key] = [float(x) for x in self._data[key]]
                self._data['min_' + key] = min(self._data[key])
                self._data['max_' + key] = max(self._data[key])
            else:
                if is_number(self._data[key]):
                    self._data[key] = float(self._data[key])

        for qkey in subtract_minimum_keys:
            minv = self._data['min_' + qkey]
            self._data[qkey] = [x - minv for x in self._data[qkey]]