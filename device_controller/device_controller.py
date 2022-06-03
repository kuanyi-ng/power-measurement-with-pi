from abc import ABC, abstractmethod

class DeviceController(ABC):
    @abstractmethod
    def close(self):
        '''
        Required: called before shutdown for general cleanup
        '''
        pass

    @abstractmethod
    def _write(self, command: str) -> int:
        pass
    
    @abstractmethod
    def _read(self, command: str) -> str:
        pass

    @abstractmethod
    def _query(self, command: str) -> str:
        '''
        _query = _write + _read (in sequence)
        '''
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_output_current(self, val: float) -> int:
        pass

    @abstractmethod
    def set_output_voltage(self, val: float) -> int:
        pass

    @abstractmethod
    def output_on(self) -> int:
        pass

    @abstractmethod
    def output_off(self) -> int:
        pass

    @abstractmethod
    def get_current(self) -> float:
        pass

    @abstractmethod
    def get_voltage(self) -> float:
        pass

    @abstractmethod
    def get_titles(self) -> list[str]:
        '''
        Required: returns tuple of titles for first row of CSV file
        '''
        pass

    @abstractmethod
    def get_values(self) -> tuple[float, float]:
        '''
        Required: returns tuple of values for rows in CSV file
        '''
        pass

    @abstractmethod
    def is_meter_ready(self) -> bool:
        pass
