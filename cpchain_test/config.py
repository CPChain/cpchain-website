import configparser
import os

parser = configparser.ConfigParser()

if 'config.ini' in os.listdir(os.path.dirname(__file__)):
    parser.read(os.path.join(os.path.dirname(__file__),'config.ini'))
else:
    parser.read(os.path.join(os.path.dirname(__file__),'config.default.ini'))

cfg = parser