import subprocess

import typer
import uvicorn
import multiprocessing
from tortoise import Tortoise

from app.core import config

cmd = typer.Typer()


@cmd.command(help="run develop server using uvicorn")
def runserver(
    host: str = typer.Argument("127.0.0.1"),
    port: int = typer.Argument(8000),
    reload: bool = True,
    workers: int = multiprocessing.cpu_count(),
):
    uvicorn.run("app.main:app", reload=reload, host=host, port=port, workers=workers)


@cmd.command(help="update all dependencies' versions and apply in requirements folder")
def update_dep():
    files = [
        "pip-compile requirements/production.in --no-emit-index-url -U -i https://mirrors.aliyun.com/pypi/simple/ -o requirements/production.txt -o requirements.txt",
        "pip-compile requirements/test.in --no-emit-index-url -U -i https://mirrors.aliyun.com/pypi/simple/ -o requirements/test.txt",
        "pip-compile requirements/dev.in --no-emit-index-url -U -i https://mirrors.aliyun.com/pypi/simple/ -o requirements/dev.txt"
    ]
    for file in files:
        subprocess.call( file.split(" "))


@cmd.command(help="django-like dbshell command use pgcli")
def dbshell():
    subprocess.call(["pgcli", config.settings.postgres_dsn])


@cmd.command(help="django-like shell command use ipython")
def shell():
    try:
        import IPython  # pylint: disable=import-outside-toplevel
        from traitlets.config import Config  # pylint: disable=import-outside-toplevel
    except ImportError:
        return

    models = Tortoise._discover_models("app.models", "models")  # pylint: disable=protected-access
    models_names = ", ".join([model.__name__ for model in models])
    preload_scripts = [
        "from app.main import app",
        "from app.core import config",
        "from tortoise import Tortoise",
        f"from app.models import {models_names}",
        "await Tortoise.init(config=config.db_config)",
    ]
    typer.secho("\n".join(preload_scripts), fg=typer.colors.GREEN)
    c = Config()
    c.PrefilterManager.multi_line_specials = True
    c.InteractiveShell.editor = "vim"
    c.InteractiveShellApp.exec_lines = preload_scripts
    c.TerminalIPythonApp.display_banner = False
    IPython.start_ipython(argv=[], config=c)


if __name__ == "__main__":
    cmd()
