"""Shared reader for config/tf/*.yaml (not a launch file).

Usage from a launch file in launch/ or a subfolder of it:
    import sys
    from os import path
    sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))  # adjust depth
    import nissan_tf_config
"""
from os import path

import yaml
from ament_index_python.packages import get_package_share_directory

BASE_LINK_SOURCES = ('nova', 'duro')


def _load(name):
    file = path.join(get_package_share_directory('nissan_bringup'), 'config', 'tf', name)
    with open(file, 'r') as f:
        return yaml.safe_load(f)


def map_origins():
    """{name: {'x': .., 'y': .., 'z': ..}} from map_origins.yaml."""
    return _load('map_origins.yaml')['map_origins']


def localization():
    """{'base_link_source': 'nova'|'duro', 'map_origin': name, 'origin': {x, y, z}}."""
    cfg = _load('localization.yaml')
    source = cfg['base_link_source']
    if source not in BASE_LINK_SOURCES:
        raise ValueError(f"localization.yaml: base_link_source must be one of "
                         f"{BASE_LINK_SOURCES}, got '{source}'")
    origins = map_origins()
    name = cfg['map_origin']
    if name not in origins:
        raise ValueError(f"localization.yaml: map_origin '{name}' is not in "
                         f"map_origins.yaml ({', '.join(origins)})")
    return {'base_link_source': source, 'map_origin': name, 'origin': origins[name]}
