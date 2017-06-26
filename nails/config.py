import yaml
import sys
import os
import re
from inspect import getsourcefile
from os.path import abspath

base_dir = os.path.dirname(os.path.realpath(os.path.realpath(os.getcwd() + '/' + sys.argv[0])))
config_files = os.listdir(os.path.realpath(base_dir + '/config/'))

class _Config:
    def __init__(self):
        self.base_dir = base_dir
        for filename in config_files:
            matches = re.findall(r'^.+(?=\.yml$)', filename)
            if len(matches) > 0:
                with open(os.path.realpath(base_dir + '/config/' + filename)) as f:
                    try:
                        content = self.env_override(f)
                        self.__dict__[matches[0]] = yaml.load(content)
                    except yaml.YAMLError as err:
                        print(err)

    def env_override(self, f):
        lines = []
        for line in f:
            matches = re.findall(r'(?<=\${).+(?=})', line)
            if len(matches) > 0:
                for match in matches:
                    match_split = match.split(':')
                    value = (os.environ[match_split[0]] if match_split[0] in os.environ
                             else (match_split[1] if len(match_split) > 1 else ''))
                    line = line.replace('${' + match + '}', value)
            lines.append(line)
        return ''.join(lines)

config = _Config()
