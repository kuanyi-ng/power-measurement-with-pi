#!/usr/bin/env python3

import argparse
from logging import DEBUG, INFO

from assistant.assistant import Assistant
from client.client import Client
from experiment.demo_experiment import DemoExperiment
from utils.utils import enable_logging

LOCALHOST = "127.0.0.1"

PORT = 65432

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
        help="set -V to get more detailed logs"
    )

    parser.add_argument(
        "--server_ip",
        default=LOCALHOST,
        help="specify the server's ip addr when using `--allow_public` option"
    )

    parser.add_argument(
        "--num_threads",
        type=int,
        default=1,
        help="set the number of threads used to run TFLite inference (default: 1)"
    )

    args = parser.parse_args()

    return {
        "allow_public": args.allow_public,
        "verbose": args.verbose,
        "server_ip": args.server_ip,
        "num_threads": args.num_threads,
    }



if __name__ == "__main__":
    args = parse_args()
    log_level = DEBUG if args["verbose"] else INFO
    enable_logging(level=log_level)

    host = args["server_ip"]
    port = PORT

    client = Client(host=host, port=port)

    # NOTE: change the experiment class to your own experiment class
    # experiment = InputZeroRatioExperiment(num_threads=args["num_threads"])
    experiment = DemoExperiment()
    assistant = Assistant(client=client, experiment=experiment)

    assistant.perform_all_experiments()
