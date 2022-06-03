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
        help="set -V to get more detailed logs (default: False)"
    )

    args = parser.parse_args()

    return {
        "allow_public": args.allow_public,
        "verbose": args.verbose
    }


if __name__ == "__main__":
    args = parse_args()
    log_level = DEBUG if args["verbose"] else INFO
    enable_logging(level=log_level)

    host = input("Server's IP:\t") if args["allow_public"] else LOCALHOST
    port = PORT

    client = Client(host=host, port=port)
    assistant = Assistant(client=client, experiment=DemoExperiment())

    assistant.perform_all_experiments()
