
import argparse
from logging import DEBUG, INFO

from device_controller.kikusui import Kikusui
from sampler.sampler import Sampler
from server.server import Server
from utils.utils import enable_logging

PUBLIC_HOST = "0.0.0.0"
LOCALHOST = "127.0.0.1"

PORT = 65432

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
        "--sampling_interval",
        type=float,
        default=DEFAULT_SAMPLING_INTERVAL,
        help=f"set sampling interval in seconds (default: {DEFAULT_SAMPLING_INTERVAL} s)"
    )

    parser.add_argument(
        "--device_id",
        required=True,
        help="set which measuring device to use. Choose from [14, 15]"
    )

    args = parser.parse_args()

    return {
        "allow_public": args.allow_public,
        "verbose": args.verbose,
        "sampling_interval": args.sampling_interval,
        "device_id": args.device_id,
    }


if __name__ == "__main__":
    args = parse_args()
    log_level = DEBUG if args["verbose"] else INFO
    enable_logging(level=log_level)

    device_controller = Kikusui(device_id=args["device_id"])
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
