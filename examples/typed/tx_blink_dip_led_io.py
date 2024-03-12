# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Send App_IO, blinking, typed

# Caution: Requires App_Wings v1.3.2+.
# At this time (early 2024), MWSDK has old version.
# You can download them from below links.
# - https://twelite.net/files/App_Wings_BLUE_L1305_V1-3-2.bin
# - https://twelite.net/files/App_Wings_RED_L1305_V1-3-2.bin
# - https://twelite.net/files/App_Wings_MONOSTICK_BLUE_L1305_V1-3-2.bin
# - https://twelite.net/files/App_Wings_MONOSTICK_RED_L1305_V1-3-2.bin

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
