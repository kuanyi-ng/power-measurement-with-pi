from abc import ABC, abstractmethod


class Experiment(ABC):
    @abstractmethod
    def get_output_filename(self) -> str:
        '''
        the filename to store experiment outputs
        '''
        pass

    @abstractmethod
    def before_run(self):
        '''
        preparation required before run
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        main part of the experiment (1 experiment out of all defined experiemnts)

        things done in this function are measured and profiled.
        '''
        pass

    @abstractmethod
    def after_run(self):
        '''
        things to do after the main part of the experiment
        '''
        pass

    @abstractmethod
    def all_finished(self) -> bool:
        '''
        whether all prepared experiment are done
        '''
        pass
