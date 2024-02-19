# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Receive data, print dictionary, typed

from zoneinfo import ZoneInfo

import mwings as mw


# Main function
def main() -> None:
    # Create a twelite object
    twelite = mw.Twelite(mw.utils.ask_user_for_port())

    # Use JST for received data
    twelite.set_timezone(ZoneInfo("Asia/Tokyo"))

    # Register an event handlers
    @twelite.on(mw.common.PacketType.APP_ARIA)
    def on_app_aria(packet: mw.parsers.app_aria.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_CUE)
    def on_app_cue(packet: mw.parsers.app_cue.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_CUE_PAL_EVENT)
    def on_app_cue_pal_event(packet: mw.parsers.app_cue_pal_event.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_IO)
    def on_app_io(packet: mw.parsers.app_io.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_TWELITE)
    def on_app_twelite(packet: mw.parsers.app_twelite.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_PAL_AMB)
    def on_app_pal_amb(packet: mw.parsers.app_pal_amb.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_PAL_MOT)
    def on_app_pal_mot(packet: mw.parsers.app_pal_mot.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_PAL_OPENCLOSE)
    def on_app_pal_openclose(packet: mw.parsers.app_pal_openclose.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_UART_ASCII)
    def on_app_uart_ascii(packet: mw.parsers.app_uart_ascii.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.APP_UART_ASCII_EXTENDED)
    def on_app_uart_ascii_extended(
        packet: mw.parsers.app_uart_ascii_extended.ParsedPacket,
    ) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    @twelite.on(mw.common.PacketType.ACT)
    def on_act(packet: mw.parsers.act.ParsedPacket) -> None:
        print(packet.to_dict(verbose=False, spread=True))

    # Start receiving
    try:
        # Set as daemon thread
        twelite.daemon = True
        # Start the thread, Join to the main thread
        twelite.start()
        print("Started receiving")
        while True:
            twelite.join(0.5)
    except KeyboardInterrupt:
        # Stop the thread
        print("Flushing...")
        twelite.stop()
        print("Completed")


if __name__ == "__main__":
    # Call the main function
    main()
