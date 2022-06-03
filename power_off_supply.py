import argparse

from device_controller.kikusui import Kikusui

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--device_id",
        type=str,
        required=True,
        help="specify which device to control (refer to device_controller/device_info.py)"
    )

    args = parser.parse_args()

    return {
        "device_id": args.device_id,
    }

if __name__ == "__main__":
    args = parse_args()
    device_controller = Kikusui(device_id=args["device_id"])

    device_controller.output_off()
