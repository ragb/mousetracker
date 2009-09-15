import json
import os.path

class Settings(object):

    def __init__(self, config_file=None):
        if config_file is None:
            self._config_file = self._getDefaultConfigFile()
        try:
            with open(self._config_file, "r") as f:
                self._config = json.load(f)
        except IOError:
                self._config = {}

    def flush(self):
        with open(self._config_file, "w") as f:
            json.dump(self._config, f)

    def _getDefaultConfigFile(self):
        home = os.path.expanduser("~")
        xdbg_config_path = ".config/mousetracker"
        return os.path.join(home, xdbg_config_path)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __delitem__(self, key):
        self._config[key]

    def __contains__(self, key):
        return key in self._config
