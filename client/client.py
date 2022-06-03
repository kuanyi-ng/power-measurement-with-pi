import logging
import socket
import sys

class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def _req(self, command: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                logging.info("Connecting to server...")
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((self.host, self.port))
                logging.info("Connected to server!")

                logging.info(f"Sending command: {command}")
                s.sendall(command.encode('utf-8'))
        except ConnectionRefusedError:
            logging.info("Server is not accepting connection yet. Try starting the server and rerun client app.")
            sys.exit(1)

    def req_measurement(self, output_filename: str):
        logging.info("Request to start measuring...")
        command = f'M_start_{output_filename}'
        self._req(command)

    def stop_measurement(self):
        logging.info("Request to stop measuring...")
        command = 'M_stop'
        self._req(command)
