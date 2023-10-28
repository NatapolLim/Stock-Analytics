import os
from dynaconf import Dynaconf

ENV_MODE = 'dev'

CONFIG_FILES = [
    # 'configs/params.yaml',
    # 'src/configs/params.yaml',
    # 'configs/schema.yaml',
    # 'src/configs/schema.yaml',
    'configs/settings.yaml',
    'src/configs/settings.yaml',
]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[C for C in CONFIG_FILES if os.path.isfile(C)],
    environments=True,
    env=ENV_MODE,
)