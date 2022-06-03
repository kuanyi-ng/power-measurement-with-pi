from client.client import Client

from experiment.experiment import Experiment

class Assistant:
    def __init__(self, client: Client, experiment: Experiment) -> None:
        # client is used to communicate with the server
        # that is responsible for power measurement
        self.client = client
        self.experiment = experiment
        pass

    def perform_one_experiment(self):
        output_filename = self.experiment.get_output_filename()

        self.experiment.before_run()

        self.client.req_measurement(output_filename)
        self.experiment.run()
        self.client.stop_measurement()

        self.experiment.after_run()

    def perform_all_experiments(self):
        # TODO: 
        while not self.experiment.all_finished():
            self.perform_one_experiment()
