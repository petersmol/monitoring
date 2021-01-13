"""
monitoring.settings
~~~~~~~~~~~~~~~~~~~

Sets common variables and loads application config from the YAML file.

"""

from pathlib import Path
import yaml

# This vars can be used across application
ROOT_DIR = Path(__file__).parent.parent

# Loading config.yaml
config_filename = f"{ROOT_DIR}/config/config.yaml"
with open(config_filename, "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
