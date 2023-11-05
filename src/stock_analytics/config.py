import os
from pathlib import Path
from dynaconf import Dynaconf

from stock_analytics import logger

ENV_MODE = 'dev'

CONFIG_FILES = [
    # 'configs/params.yaml',
    # 'src/configs/params.yaml',
    # 'configs/schema.yaml',
    # 'src/configs/schema.yaml',
    Path('configs/settings.yaml'),
    # 'stock_analytics/configs/settings.yaml',
]

avialable_configs = [C for C in CONFIG_FILES if os.path.isfile(C)]

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=avialable_configs,
#     environments=True,
#     env=ENV_MODE,
# )



def get_setting_configs(env_mode: str) -> Dynaconf:

    logger.info(f"Load settings variables from configs; {avialable_configs}")
    
    return Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=avialable_configs,
        environments=True,
        env=env_mode,
    )