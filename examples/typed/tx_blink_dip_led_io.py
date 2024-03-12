# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Send App_IO, blinking, typed

from time import sleep
from typing import Any

import mwings as mw


def main() -> None:
    # Create twelite object
    twelite = mw.Twelite(mw.utils.ask_user_for_port())

    # Create command (initialize in pydantic style)
    initial: dict[str, Any] = {
        "destination_logical_id": 0x78,
        "di_to_change": [True for _ in range(12)],
        "di_state": [False for _ in range(12)],
    }
    command = mw.serializers.app_io.Command(**initial)

    # Blinking
    while True:
        command.di_state[0] = not command.di_state[0]
        twelite.send(command)
        print(f"Flip Output1: {command.di_state[0]}")
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("...Aborting")
