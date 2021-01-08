from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).parent.parent
config_filename = f"{ROOT_DIR}/config/config.yaml"
with open(config_filename, "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)