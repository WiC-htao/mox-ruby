import os
import yaml
import warnings


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.load(f)


def dump_yaml(dt, path):
    assert not os.path.exists(path), f"File<{path}> exists. Use overwrite_yaml instead"
    with open(path, "w") as f:
        return yaml.dump(dt, f)


def overwrite_yaml(dt, path):
    if os.path.exists(path):
        warnings.warn(
            f"File<{path}> not exists. Encourage using dump_yaml instead to be more safety"
        )
    with open(path, "w") as f:
        return yaml.dump(dt, f)
