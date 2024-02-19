# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Receive data, export as csv, durable, typed

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

import mwings as mw


# Command arguments
class CommandArgs(argparse.Namespace):
    verbose: bool
    sort: bool


# Main function
def main(args: CommandArgs) -> None:
    # Create a twelite object
    twelite = mw.Twelite(mw.utils.ask_user_for_port())

    # Use JST for received data
    twelite.set_timezone(ZoneInfo("Asia/Tokyo"))

    # Dictionary of saved csv files
    saved_files: dict[str, Path] = {}
    packet_types: dict[str, str] = {}

    # Closure to append some packet to the dataframe
    def append(packet: mw.common.SomeParsedPacket) -> None:
        # Create df
        df = packet.to_df(verbose=args.verbose)

        # Sort if necessary
        if args.sort:
            df = df.sort_index(axis="columns")

        # Check for existance
        if packet.source_serial_id.hex() not in saved_files.keys():
            # Prepare csv path
            export_path = (
                Path.cwd()
                .joinpath(
                    f"{datetime.now(twelite.timezone).strftime('%Y-%m-%d-%H-%M')}-{packet.packet_type.title()}-{packet.source_serial_id.hex().upper()}"
                )
                .with_suffix(".csv")
            )
            # Create file
            with open(export_path, "x") as f:
                df.to_csv(f, header=True, index=False)
            saved_files[packet.source_serial_id.hex()] = export_path
            packet_types[packet.source_serial_id.hex()] = packet.packet_type
        else:
            with open(saved_files[packet.source_serial_id.hex()], "a") as f:
                if packet_types[packet.source_serial_id.hex()] == packet.packet_type:
                    df.to_csv(f, header=False, index=False)

    # Register event handlers
    @twelite.on(mw.common.PacketType.APP_ARIA)
    def on_app_aria(packet: mw.parsers.app_aria.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_CUE)
    def on_app_cue(packet: mw.parsers.app_cue.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_CUE_PAL_EVENT)
    def on_app_cue_pal_event(packet: mw.parsers.app_cue_pal_event.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_IO)
    def on_app_io(packet: mw.parsers.app_io.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_AMB)
    def on_app_pal_amb(packet: mw.parsers.app_pal_amb.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_MOT)
    def on_app_pal_mot(packet: mw.parsers.app_pal_mot.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_OPENCLOSE)
    def on_app_pal_openclose(packet: mw.parsers.app_pal_openclose.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_TWELITE)
    def on_app_twelite(packet: mw.parsers.app_twelite.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_UART_ASCII)
    def on_app_uart_ascii(packet: mw.parsers.app_uart_ascii.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.APP_UART_ASCII_EXTENDED)
    def on_app_uart_ascii_extended(
        packet: mw.parsers.app_uart_ascii_extended.ParsedPacket,
    ) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

    @twelite.on(mw.common.PacketType.ACT)
    def on_act(packet: mw.parsers.act.ParsedPacket) -> None:
        print(
            f"Received {packet.packet_type.title()} data from the device 0x{packet.source_serial_id.hex().upper()}"
        )
        append(packet)

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
        print("...Stopping")
        twelite.stop()
        print("Stopped")

    # Show result
    for serial_id_str, saved_file in saved_files.items():
        print(
            f"Saved {packet_types[serial_id_str].title()} data for the device 0x{serial_id_str.upper()} as {saved_file.resolve()}"
        )


if __name__ == "__main__":
    # Handle command arguments
    parser = argparse.ArgumentParser(
        description="Log packets from App_Wings to csv, line by line"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        required=False,
        action="store_true",
        help="include system information",
    )
    parser.add_argument(
        "-s",
        "--sort",
        dest="sort",
        required=False,
        action="store_true",
        help="sort columns in the output",
    )
    args = parser.parse_args(namespace=CommandArgs())

    # Call the main function
    main(args)
