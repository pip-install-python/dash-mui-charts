"""Dash MUI Charts - Dash components wrapping MUI X Charts"""
import os as _os
import json

from ._imports_ import *
from ._imports_ import __all__

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, 'package-info.json'))

with open(_filepath) as f:
    package = json.load(f)

package_name = package['name'].replace(' ', '_').replace('-', '_')
__version__ = package['version']

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_js_dist = [
    {
        'relative_package_path': '{}.min.js'.format(package_name),
        'namespace': package_name,
    },
    {
        'relative_package_path': '{}.min.js.map'.format(package_name),
        'namespace': package_name,
        'dynamic': True,
    },
]

for _component in __all__:
    setattr(locals()[_component], '_js_dist', _js_dist)
