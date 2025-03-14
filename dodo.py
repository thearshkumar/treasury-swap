"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based

"""

#######################################
## Configuration and Helpers for PyDoit
#######################################
## Make sure the src folder is in the path
import sys

sys.path.insert(1, "./src/")

import shutil
from os import environ, getcwd, path
from pathlib import Path

from colorama import Fore, Style, init

## Custom reporter: Print PyDoit Text in Green
# This is helpful because some tasks write to sterr and pollute the output in
# the console. I don't want to mute this output, because this can sometimes
# cause issues when, for example, LaTeX hangs on an error and requires
# presses on the keyboard before continuing. However, I want to be able
# to easily see the task lines printed by PyDoit. I want them to stand out
# from among all the other lines printed to the console.
from doit.reporter import ConsoleReporter

from settings import config

try:
    in_slurm = environ["SLURM_JOB_ID"] is not None
except:
    in_slurm = False


class GreenReporter(ConsoleReporter):
    def write(self, stuff, **kwargs):
        doit_mark = stuff.split(" ")[0].ljust(2)
        task = " ".join(stuff.split(" ")[1:]).strip() + "\n"
        output = (
            Fore.GREEN
            + doit_mark
            + f" {path.basename(getcwd())}: "
            + task
            + Style.RESET_ALL
        )
        self.outstream.write(output)


if not in_slurm:
    DOIT_CONFIG = {
        "reporter": GreenReporter,
        # other config here...
        # "cleanforget": True, # Doit will forget about tasks that have been cleaned.
        "backend": "sqlite3",
        "dep_file": "./.doit-db.sqlite",
    }
else:
    DOIT_CONFIG = {"backend": "sqlite3", "dep_file": "./.doit-db.sqlite"}
init(autoreset=True)


BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")
OUTPUT_DIR = config("OUTPUT_DIR")


## Helpers for handling Jupyter Notebook tasks
# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --log-level WARN --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --log-level WARN --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --log-level WARN --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def copy_file(origin_path, destination_path, mkdir=True):
    """Create a Python action for copying a file."""

    def _copy_file():
        origin = Path(origin_path)
        dest = Path(destination_path)
        if mkdir:
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)

    return _copy_file


##################################
## Begin rest of PyDoit tasks here
##################################


def task_config():
    """Create empty directories for data and output if they don't exist"""
    return {
        "actions": ["ipython ./src/settings.py"],
        "targets": [DATA_DIR, OUTPUT_DIR],
        "file_dep": ["./src/settings.py"],
        "clean": [],
    }

##############################$
## Pulling Data
##############################$

def task_pull_bloomberg():
    """Pulls treasury and swap yields from Bloomberg"""
    file_dep = [
        "./src/settings.py",
        "./src/pull_bloomberg.py",
    ]
    targets = [
        DATA_DIR / 'bbg' / "raw_tyields.pkl",
        DATA_DIR / 'bbg' / "raw_syields.pkl",
    ]

    return {
        "actions": [
            "ipython ./src/settings.py",
            "ipython ./src/pull_bloomberg.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": [],
    }

##############################$
## Calculating the spread
##############################$

def task_calc_swap_spreads():
    """Calculates the swap spreads"""
    file_dep = [
        "./src/settings.py",
        "./src/calc_swap_spreads.py",
    ]
    targets = [
        DATA_DIR / 'calc_spread' / 'calc_merged.pkl',
    ]

    return {
        "actions": [
            "ipython ./src/settings.py",
            "ipython ./src/calc_swap_spreads.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": [],
    }

##############################$
## Supplementary
##############################$

def task_supplementary():
    """Runs the supplementary functions for plots and a table"""
    file_dep = [
        "./src/settings.py",
        "./src/supplementary.py",
    ]
    targets = [
        OUTPUT_DIR / 'table.txt',
    ]

    return {
        "actions": [
            "ipython ./src/settings.py",
            "ipython ./src/supplementary.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": [],
    }


##############################$
## Plotting
##############################$

def task_plot_figure():
    """Create the replicated, updated, and supplementary plots"""
    files = ["plot_figure.py"]
    file_dep = [Path("./src") / x for x in files]
    file_output = ["replicated_swap_spread_arb_figure.png", 
                   'updated_swap_spread_arb_figure.png']
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/plot_figure.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


##############################$
## LaTeX compilation
##############################$


def task_compile_latex_docs():
    """Compile the LaTeX documents to a PDF report"""
    file_dep = [
        "./reports/main_report.tex",
    ]
    targets = [
        "./reports/main_report.pdf",
    ]

    return {
        "actions": [
            # My custom LaTeX templates
            "latexmk -xelatex -halt-on-error -cd ./reports/main_report.tex",  # Compile
            "latexmk -xelatex -halt-on-error -c -cd ./reports/main_report.tex",  # Clean
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }