import subprocess
import logging
import shlex
from time import time

from experiment.experiment import Experiment


class SingleCommandExperiment(Experiment):
    def __init__(self, raw_command: str) -> None:
        self.command = shlex.quote(raw_command)

        self.finished = False

    def before_run(self):
        # do nothing
        pass

    def get_output_filename(self) -> str:
        filename = f'{time()}_single_command_experiment.csv'
        logging.debug(f'output: {filename}')

        return filename

    def run(self):
        logging.debug(f"Running command: {self.command}")
        subprocess.run(shlex.split(self.command), capture_output=True, shell=False)

        self.finished = True
        pass

    def after_run(self):
        # do nothing
        pass

    def all_finished(self) -> bool:
        return self.finished
