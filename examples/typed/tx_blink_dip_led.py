# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Send App_Twelite, blinking, typed

from time import sleep
from typing import Any

import mwingslite as mw


def main() -> None:
    # Create twelite objec
    twelite = mw.Twelite("/dev/ttyS0")  # For RasPi (serial0)
    # twelite = mw.Twelite("/dev/ttyUSB0") # For RasPi (USB)
    # twelite = mw.Twelite(mw.utils.ask_user_for_port())

    # Create command (initialize in pydantic style)
    initial: dict[str, Any] = {
        "destination_logical_id": 0x78,
        "di_to_change": [True, False, False, False],
        "di_state": [False, False, False, False],
    }
    command = mw.serializers.app_twelite.Command(**initial)

    # Blinking
    while True:
        command.di_state[0] = not command.di_state[0]
        twelite.send(command)
        print(f"Flip DO1: {command.di_state[0]}")
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("...Aborting")
