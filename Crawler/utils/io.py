import os
import os.path as osp
import shutil

def restart(fpath: str):
    if osp.exists(fpath):
        shutil.rmtree(fpath)
        