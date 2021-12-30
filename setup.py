#!/usr/bin/env python

"""
\b
Virtual Environment Management utility
    venv clean
    venv setup
    venv [venv]

\b
TODO:
    Add global config
    Build initial README.md
    Display password hint
"""

# https://python-packaging.readthedocs.io/en/latest/index.html
# https://www.geeksforgeeks.org/command-line-scripts-python-packaging
# https://pythonhosted.org/an_example_pypi_project/setuptools.html
# https://packaging.python.org/tutorials/packaging-projects

import platform
from pathlib import Path
from shutil import rmtree
from subprocess import run


VENV_PATH = Path("./venv")
PYTHON = "python"


'''
def setup(package_name: str) -> None:
    """
    Setup package (venv, setup.py, git, tests)

    Assumes directory structure:
      <PACKAGE>
      |-- <PACKAGE>/
          |-- __init__.py
      |-- tests/
          |-- __init__.py
      |-- README.md
      |-- LICENSE
      |-- setup.py
      |-- requirements.in
      |-- requirements.txt
      |-- venv/
      |-- .gitignore
      |-- .git/
    """
    # TODO: use LICENSE templates
    # TODO: use README.md templates

    path = Path.cwd()

    if not (path / ".git").exists():
        run("git init", shell=True, check=True)
    if not (path / ".gitignore").exists():
        write_gitignore()

    (path / package_name).mkdir(exist_ok=True)
    (path / package_name / "__init__.py").touch(exist_ok=True)
    (path / "tests").mkdir(exist_ok=True)
    (path / "tests" / "__init__.py").touch(exist_ok=True)
    (path / "README.md").touch(exist_ok=True)
    (path / "LICENSE").touch(exist_ok=True)
    (path / "setup.py").touch(exist_ok=True)
'''


def remove(path: Path) -> None:
    """ Remove file or directory specified by path """
    if path.exists():
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()


def modified_after(path1: Path, path2: Path) -> bool:
    """ Return if path1 has a modify time after path2 """
    if path1.exists() and path2.exists():
        return path1.stat().st_mtime > path2.stat().st_mtime
    return False


def clean() -> None:
    """Remove temporary files"""

    remove(VENV_PATH)
    remove(Path("build"))
    remove(Path("dist"))
    for path in Path(".").glob("*.egg-info"):
        remove(path)
    for path in Path(".").rglob("__pycache__"):
        remove(path)


def activate_command() -> str:
    """Return command to activate virtual environment"""
    if platform.system() == "Windows":
        source = ""
        activate_path = VENV_PATH / "Scripts/activate.bat"
        separator = " & "
    else:
        source = ". "
        activate_path = VENV_PATH / "bin/activate"
        separator = "; "

    return f"{source}{activate_path}{separator}"


def main() -> None:
    """
    Make virtual environment

    Create requirements.in if it doesn't exist.
    Clean venv if requirements.in was modified after venv.
    Create venv if it doesn't exist.
    Upgrade pip, setuptools and wheel
    Install modules in requirements.in
    Write installed modules to requirements.txt
    """
    requirements_in_path = Path("./requirements.in")
    requirements_txt_path = Path("./requirements.txt")
    if not requirements_in_path.exists():
        requirements_in_path.touch()
    elif modified_after(requirements_in_path, VENV_PATH):
        clean()

    activate = activate_command()
    commands = f"""
            {PYTHON} -m venv {VENV_PATH};
            {activate} {PYTHON} -m pip install --upgrade pip setuptools wheel pip-tools;
            {activate} {PYTHON} -m pip install -r {requirements_in_path};
            {activate} {PYTHON} -m pip freeze > {requirements_txt_path};
            """
    print(commands)
    # {activate} pip-compile {requirements_in_path} -o {requirements_txt_path}
    # {activate} {PYTHON} -m pip install -r {requirements_txt_path}
    #commands=f"{PYTHON} -m venv {VENV_PATH}"
    run(commands, shell=True, check=True)


if __name__ == "__main__":
    main()

