"""Deal with the config files.

BEM will try sequentially:

    #) config_file as it comes.
    #) os.getcwd() + config_file, i.e. the path from where the library is
    called plus the name that is passed to the function.
    #) os.environ["BEM_CONFIG"]. If "BEM_CONFIG" is configured, use it.

"""

import ConfigParser
import os


def read_config_values(config_file_path):
    """Load and return the config_file_path parsed."""

    config = ConfigParser.SafeConfigParser()

    if config_file_path and os.path.isfile(config_file_path):
        config.readfp(open(config_file_path))
        return config

    return False


def get_config_file(config_file_path):
    """Generate and return the apropriate config parsed ."""

    fallbacks = []
    if config_file_path:
        fallbacks = [config_file_path,
                     os.path.join(os.getcwd(), config_file_path)]

    fallbacks.append(os.environ.get("BEM_CONFIG"))

    for step in fallbacks:
        config = read_config_values(step)
        if config:
            return config

    raise IOError("Config not found in {0}.".format(config_file_path or "-"))
