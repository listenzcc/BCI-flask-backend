"""
File: report_worker.py
Author: Chuncheng Zhang
Date: 2025-05-07
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Worker for generating report.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-07 ------------------------
# Requirements and constants
from pathlib import Path
from loguru import logger

logger.add('log/report.log', rotation='5 MB')

# %% ---- 2025-05-07 ------------------------
# Function and class


class MyReport:
    inventory_path: Path

    def __init__(self, inventory_path: Path):
        self.inventory_path = Path(inventory_path)
        self.inventory_path.mkdir(parents=True, exist_ok=True)
        logger.info(f'Initialize with inventory_path: {inventory_path}')

    def generate_report(self, name, org_id, user_id, project_name, event):
        basename = f'{name}-{org_id}-{user_id}-{project_name}-{event}'

        # Find the good fpath
        fpath = self.inventory_path.joinpath(f'{basename}.html')
        for i in range(10000000):
            fname = f'{basename}-[{i}].html'
            fpath = self.inventory_path.joinpath(fname)
            if not fpath.is_file():
                break
        logger.debug(f'Using fpath: {fpath}')

        with open(fpath, 'w') as f:
            f.writelines([name, org_id, user_id, project_name, event])
        logger.info(f'Wrote report: {fpath}')
        return basename, fpath


# %% ---- 2025-05-07 ------------------------
# Play ground


# %% ---- 2025-05-07 ------------------------
# Pending


# %% ---- 2025-05-07 ------------------------
# Pending
