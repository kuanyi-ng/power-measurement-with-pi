import logging
from io import TextIOWrapper
from typing import Any

def enable_logging(level: int = logging.INFO):
    format = "%(asctime)s:%(message)s"
    date_format = "%H:%M:%S"

    logging.basicConfig(
        format=format,
        level=level,
        datefmt=date_format
    )

def write_csv(csv: TextIOWrapper, items: list[Any]):
    row = ", ".join(map(str, items))
    csv.write(f"{row}\n")
    csv.flush()
