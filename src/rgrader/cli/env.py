from pprint import pprint
from pathlib import Path
from typing import Annotated, Dict, Optional

import typer
from dotenv import dotenv_values

from rgrader.settings import settings

app = typer.Typer()


def load(
    env_dir: Path,  # the place where we read *.env files
    additional_pairs: Dict[str, str] = {},  # additional variables we want to pass
) -> Dict[str, Dict[str, Optional[str]]]:
    ## load environment files

    ## Initialize the return dict
    env_vars: Dict[str, Dict[str, Optional[str]]] = dict()
    for name in settings.env_names:
        env_vars[name] = {}

    ## Fill the env dict with values from the <app>.<env>.env files
    for app in settings.app_names:
        for env_name in settings.env_names:
            default_pairs: Dict[str, Optional[str]] = dotenv_values(
                Path(
                    env_dir,
                    f"{app}.default.env",  # e.g. examaddin.docker-dev.env
                )
            )
            env_vars[env_name].update(default_pairs)

            pairs: Dict[str, Optional[str]] = dotenv_values(
                Path(
                    env_dir,
                    f"{app}.{env_name}.env",  # e.g. examaddin.docker-dev.env
                )
            )
            env_vars[env_name].update(pairs)

    ## Add the env_name
    for aname in settings.env_names:
        env_vars[aname]["ENV_NAME"] = aname

    ## Add additional pairs
    for iname in settings.env_names:
        for key in additional_pairs:
            env_vars[iname][key] = additional_pairs[key]

    return env_vars


@app.command()
def print(
    env_dir: Annotated[
        Path, typer.Argument(help="Directory path from which we read *.env files")
    ] = Path(".env")
):
    env = load(env_dir, additional_pairs={"RAZALT_DIR_DEV": ".."})
    pprint(env)
