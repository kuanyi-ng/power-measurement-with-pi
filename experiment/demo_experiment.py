import logging
import time

from experiment.experiment import Experiment


class DemoExperiment(Experiment):
    def __init__(self) -> None:
        super().__init__()

        self.all_i = 5
        self.next_i = 1

    def before_run(self):
        # do nothing
        pass

    def get_output_filename(self) -> str:
        filename = f'{time.time()}_demo_experiment.csv'
        logging.debug(f"output: {filename}")

        return filename
    
    def run(self):
        logging.info(f"Sleeping for {self.next_i} s...")
        time.sleep(self.next_i)
        self.next_i += 1

    def after_run(self):
        # do nothing
        pass

    def all_finished(self) -> bool:
        return self.next_i > self.all_i
