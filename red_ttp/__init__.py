import os
import glob

RED_TTP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_ttp_list():
    scripts = []
    for script in sorted(glob.glob(os.path.join(RED_TTP_PATH, "*.py"))):
        if os.path.basename(script) not in ("__init__.py", "common.py"):
            scripts.append(script)

    return scripts


def get_ttp_names():
    names = []
    for script in get_ttp_list():
        basename, ext = os.path.splitext(os.path.basename(script))
        names.append(basename)
    return names
