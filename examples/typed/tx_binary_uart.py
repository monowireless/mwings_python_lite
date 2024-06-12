# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Send App_Uart (Mode A), beef, typed

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
        "command_id": 0x01,
        "data": bytes([0xBE, 0xEF]),
    }
    command = mw.serializers.app_uart_ascii.Command(**initial)

    # Send repeatedly
    while True:
        twelite.send(command)
        print(f"Send beef to the device (0x{command.data.hex().upper()})")
        sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("...Aborting")
