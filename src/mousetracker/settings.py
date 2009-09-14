from ConfigParser import SafeConfigParser

import os.path


_config = None
_config_file = None

def _getDefaultConfigFile():
    return os.path.join(os.path.expanduser("~"), ".config/mousetracker")

def init(config_file=None):
    global _config, _config_file
    _config = SafeConfigParser()
    if config_file is None:
        config_file = _getDefaultConfigFile()
    _config_file = config_file
    _config.read(_config_file)

def get(section, option):
    return _config.get(section, option)

def set(section, option, value, flush=True):
    _config.set(section, option, value)
    if flush:
        flush()

def flush():
    _config.write(_config_file)

def getSection(section):
    dict = {}
    if not _config.has_section(section):
        return dict
    for k, v in _config.items(section):
        dict[k] = v
    return dict
