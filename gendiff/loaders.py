import json
import os
from yaml import load as YAMLloads
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader


LOADERS = {
    '.json': json.loads,
    '.yml': lambda f: YAMLloads(f, YAMLLoader),
    '.yaml': lambda f: YAMLloads(f, YAMLLoader),
    '.txt': lambda f: f.strip()
}


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def load(filename):
    file = read_file(filename)
    _, ext = os.path.splitext(filename)
    return LOADERS[ext](file) or {}
