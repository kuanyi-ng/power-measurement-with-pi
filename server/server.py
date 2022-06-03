import logging
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from sampler.sampler import Sampler

class Server:
    def __init__(self,
        sampler: Sampler,
        host: str,
        port: int,
    ) -> None:
        # set() -> stop everything (cannot resume)
        self.stop_event = threading.Event()
        
        # set() -> pause measurements (can resume)
        self.pause_event = threading.Event()
        self.pause_event.set()

        # sampler that performs measurements
        self.sampler = sampler

        self.host = host
        self.port = port

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logging.info(f"Listening on port {self.port}...")

            while not self.stop_event.is_set():
                conn = None
                try:
                    logging.info("(accept) Waiting for connection...")
                    conn, addr = s.accept()
                    with conn:
                        logging.info(f"Connected by: {addr}")

                        while not self.stop_event.is_set():
                            msg_from_client = conn.recv(1024)
                            logging.debug(f"From client: {msg_from_client}")

                            if not msg_from_client: break
                            else:
                                if msg_from_client.startswith(b'M_start'):
                                    output_filename = msg_from_client.decode('utf-8').replace('M_start_', '')
                                    self.sampler.set_output_filename(output_filename)
                                    self.pause_event.clear()
                                    logging.info("Start new measurement")
                                elif msg_from_client.startswith(b'M_stop'):
                                    self.pause_event.set()
                                    logging.info("Stop measurement")

                except KeyboardInterrupt:
                    if conn: conn.close()
                    break

            logging.info("Stopping server...")

    def run(self):
        # 3 workers
        # - 1 for socket server
        # - 1 for taking measurement
        # - 1 for recording measurement
        with ThreadPoolExecutor(max_workers=3) as executor:
            run_server_future = executor.submit(self.run_server)
            measure_future = executor.submit(self.sampler.measure, self.stop_event, self.pause_event)

            try:
                for future in as_completed([run_server_future, measure_future]):
                    future.result()
            except KeyboardInterrupt:
                logging.debug("KeyboardInterrupt captured!")
                self.stop_event.set()
                self.sampler.close()
                logging.info("⚠️\tWait for all measured values to be recorded before stopping the socket server.")
                logging.info("⚠️\tAfter that, ^C twice to stop the socket server.")

        logging.info("All threads ended.")


