import ConfigParser
import os


def get_config_values():
    '''Load and return the config.cfg parser plus config.cfg path'''
    config = ConfigParser.RawConfigParser()
    #First try the config.cfg in the same directory
    if os.path.isfile(os.path.join(os.getcwd(), "config.cfg")):
        return config.read(os.path.join(os.getcwd(), "config.cfg"))
    #And then the file in the executable directory
    elif os.path.isfile(os.path.join(
            os.path.realpath(__file__), "config.cfg")):
        return config  # , config.read(os.path.join(
            #os.path.realpath(__file__), "config.cfg"))
