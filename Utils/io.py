import os
import os.path as osp
import shutil


def start_dir(folder: str, restart: bool = False):
    if osp.exists(folder) and restart:
        shutil.rmtree(folder)

    os.makedirs(folder, exist_ok=True)
