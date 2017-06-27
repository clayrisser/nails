import os
import sys
import re
import yaml
import namedtupled

base_dir = os.path.dirname(os.path.realpath(os.getcwd() + '/' + sys.argv[0]))

def set_app_config(app_name):
    config[app_name] = load_app_config(os.path.dirname(base_dir + '/' + app_name + '/config/'))

def load_app_config(dirpath):
    app_config = {}
    for filename in os.listdir(dirpath):
        matches = re.findall(r'^.+(?=.yml$)', filename)
        if len(matches) > 0:
            app_config[matches[0]] = load_config_file(os.path.realpath(dirpath + '/' + filename))
    return app_config

def load_config_file(filepath):
    with open(filepath) as f:
        try:
            content = env_override(f)
            return yaml.load(content)
        except yaml.YAMLError as err:
            print(err)

def env_override(f):
    lines = []
    for line in f.readlines():
        matches = re.findall(r'(?<=\${).+(?=})', line)
        if len(matches) > 0:
            for match in matches:
                match_split = match.split(':')
                value = (os.environ[match_split[0]] if match_split[0] in os.environ
                        else (match_split[1] if len(match_split) > 1 else ''))
                line = line.replace('${' + match + '}', value)
        lines.append(line)
    return ''.join(lines)

config = load_app_config(os.path.dirname(base_dir + '/config/'))
config['base_dir'] = base_dir