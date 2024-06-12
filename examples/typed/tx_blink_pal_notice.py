# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Send App_PAL (NOTICE), blinking, typed

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
        "destination_logical_id": 0x01,
        "color": mw.common.AppPalNoticeColor.RED,
        "blink_speed": mw.common.AppPalNoticeBlinkSpeed.FAST,
        "brightness": 0xF,
        "duration_in_sec": 3,
    }
    command = mw.serializers.app_pal_notice.Command(**initial)

    # Blinking for 5 seconds (Recommend to set PAL interval as 2s)
    for color in mw.common.AppPalNoticeColor:
        command.color = color
        twelite.send(command)
        print(f"Blink for 3s in color {color.name}")
        sleep(8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("...Aborting")
