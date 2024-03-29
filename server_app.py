
import argparse
from logging import DEBUG, INFO

from device_controller.kikusui import Kikusui
from sampler.sampler import Sampler
from server.server import Server
from utils.utils import enable_logging

PUBLIC_HOST = "0.0.0.0"
LOCALHOST = "127.0.0.1"

PORT = 65432

DEFAULT_OUTPUT_VOLTAGE = 5.1 # V
DEFAULT_OUTPUT_CURRENT = 3.0 # A
DEFAULT_SAMPLING_INTERVAL = 0.05 # sec

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--allow_public",
        action="store_true",
        default=False,
        help="set --allow-public to allow socket connection from another machine (default: False)"
    )

    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        default=False,
        help="set -V to get more detailed logs (default: False)"
    )

    parser.add_argument(
        "--output_voltage",
        type=float,
        default=DEFAULT_OUTPUT_VOLTAGE,
        help=f"set output voltage of power supply in volt (default: {DEFAULT_OUTPUT_VOLTAGE} V)"
    )

    parser.add_argument(
        "--output_current",
        type=float,
        default=DEFAULT_OUTPUT_CURRENT,
        help=f"set output current of power supply in ampere (default: {DEFAULT_OUTPUT_CURRENT} A)"
    )

    parser.add_argument(
        "--sampling_interval",
        type=float,
        default=DEFAULT_SAMPLING_INTERVAL,
        help=f"set sampling interval in seconds (default: {DEFAULT_SAMPLING_INTERVAL} s)"
    )

    parser.add_argument(
        "--device_id",
        required=True,
        help="set which measuring device to use. Choose from [14, 15, 21, 87]"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    log_level = DEBUG if args.verbose else INFO
    enable_logging(level=log_level)

    device_controller = Kikusui(device_id=args.device_id)
    device_controller.set_output_voltage(args.output_voltage)
    device_controller.set_output_current(args.output_current)
    device_controller.output_on()

    host = PUBLIC_HOST if args.allow_public else LOCALHOST
    port = PORT

    s = Server(
        sampler=Sampler(
            device_controller=device_controller,
            output_filename='test.csv',
            sampling_interval=args.sampling_interval
        ),
        host=host,
        port=port,
    )

    s.run()
