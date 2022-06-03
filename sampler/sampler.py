import logging
import queue
import time

from device_controller.device_controller import DeviceController
from utils.utils import write_csv


class Sampler():
    def __init__(
        self,
        device_controller: DeviceController,
        output_filename: str,
        sampling_interval: float,
    ) -> None:
        self.device_controller = device_controller
        logging.info(f"Sampling at {sampling_interval}[s]")
        self.sampling_interval = sampling_interval

        self.queue = queue.Queue()
        self.output_filename = output_filename
        self.output_file = None
    
    def set_output_filename(self, filename: str):
        if self.output_file:
            self.output_file.close()

        self.output_filename = f"measurement_data/{filename}"
        self.output_file = open(filename, 'w')

    def _close_output_file(self):
        if self.output_file:
            self.output_file.close()
            self.output_file = None

    def close(self):
        self.device_controller.close()

    def _get_one_sample(self) -> list[float]:
        return list(self.device_controller.get_values())

    def measure(self, stop_event, pause_event):
        while not stop_event.is_set():
            logging.debug("First measure while loop")
            # | end | loop? |
            # | --- | ---   |
            # | 0   | 1     |
            # | 1   | 0     |
            #
            # loop as long as it's not the end,
            # can be
            # - taking measurements
            # - waiting for command to start measurements

            if self.output_file == None:
                self.output_file = open(self.output_filename, 'w')

            last_measured_time = None
            num_sample_cycles = 0

            while not stop_event.is_set() and not pause_event.is_set():
                logging.debug("Second measure while loop")
                logging.debug(f"Last measured time: {last_measured_time}")
                # | stop    | measure?  |
                # | ---     | ---       |
                # | 0       | 1         |
                # | 1       | 0         |
                #
                # measure when it's not the end && not stop measurements
                current_time = time.perf_counter()
                duration_from_last_measured = (current_time - last_measured_time)\
                                                if (last_measured_time is not None)\
                                                else self.sampling_interval

                remaining_time = self.sampling_interval - duration_from_last_measured
                logging.debug(f"remaining time: {remaining_time}")

                # need to take sample
                if remaining_time <= 0:
                    last_measured_time = current_time
                    values = [ current_time ] + self._get_one_sample()
                    logging.info(f"Measured value: {values}")

                    write_csv(csv=self.output_file, items=values)

                    num_sample_cycles += 1
                elif remaining_time > 0.01:
                    time.sleep(remaining_time / 2.0)

        logging.info("end measuring")
