
import argparse
from logging import DEBUG, INFO

from device_controller.demo_device_controller import DemoDeviceController
from sampler.sampler import Sampler
from server.server import Server
from utils.utils import enable_logging

PUBLIC_HOST = "0.0.0.0"
LOCALHOST = "127.0.0.1"

PORT = 65432

DEFAULT_SAMPLING_INTERVAL = 0.2 # sec

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
        "--sampling_interval",
        type=float,
        default=DEFAULT_SAMPLING_INTERVAL,
        help="set sampling interval in seconds (default: 0.2 s)"
    )

    args = parser.parse_args()

    return {
        "allow_public": args.allow_public,
        "verbose": args.verbose,
        "sampling_interval": args.sampling_interval
    }


if __name__ == "__main__":
    args = parse_args()
    log_level = DEBUG if args["verbose"] else INFO
    enable_logging(level=log_level)

    device_controller = DemoDeviceController()
    device_controller.set_output_voltage(5.1)
    device_controller.set_output_current(3.0)
    device_controller.output_on()

    host = PUBLIC_HOST if args["allow_public"] else LOCALHOST
    port = PORT

    s = Server(
        sampler=Sampler(
            device_controller=device_controller,
            output_filename='test.csv',
            sampling_interval=args["sampling_interval"]
        ),
        host=host,
        port=port,
    )

    s.run()
