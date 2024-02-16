# -*- coding:utf-8 -*-
# Written for Python 3.12
# Formatted with Black

# MWings example: Parse local log txt, export as csv or excel, typed

import argparse
from pathlib import Path

import mwings as mw
import pandas as pd


# Command arguments
class CommandArgs(argparse.Namespace):
    input_file: Path
    use_excel: bool
    verbose: bool
    sort: bool


# Main function
def main(args: CommandArgs) -> None:
    if not args.input_file.exists():
        raise argparse.ArgumentTypeError(f"{args.input_file.name} does not exist")

    # Create a twelite object with no port
    twelite = mw.Twelite(port=None)

    # Create a dictionary to store dataframes
    df_dict: dict[str, pd.DataFrame] = {}

    # Closure to append some packet to the dataframe
    def append(packet: mw.common.SomeParsedPacket) -> None:
        nonlocal df_dict
        if packet.packet_type in df_dict:
            df_dict[packet.packet_type] = pd.concat(
                [
                    df_dict[packet.packet_type],
                    packet.to_df(verbose=args.verbose),
                ],
                ignore_index=True,
            )
        else:
            df_dict[packet.packet_type] = pd.DataFrame()
            append(packet)

    # Register event handlers
    @twelite.on(mw.common.PacketType.APP_ARIA)
    def on_app_aria(packet: mw.parsers.app_aria.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_CUE)
    def on_app_cue(packet: mw.parsers.app_cue.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_CUE_PAL_EVENT)
    def on_app_cue_pal_event(packet: mw.parsers.app_cue_pal_event.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_IO)
    def on_app_io(packet: mw.parsers.app_io.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_AMB)
    def on_app_pal_amb(packet: mw.parsers.app_pal_amb.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_MOT)
    def on_app_pal_mot(packet: mw.parsers.app_pal_mot.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_PAL_OPENCLOSE)
    def on_app_pal_openclose(packet: mw.parsers.app_pal_openclose.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_TWELITE)
    def on_app_twelite(packet: mw.parsers.app_twelite.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_UART_ASCII)
    def on_app_uart_ascii(packet: mw.parsers.app_uart_ascii.ParsedPacket) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.APP_UART_ASCII_EXTENDED)
    def on_app_uart_ascii_extended(
        packet: mw.parsers.app_uart_ascii_extended.ParsedPacket,
    ) -> None:
        append(packet)

    @twelite.on(mw.common.PacketType.ACT)
    def on_act(packet: mw.parsers.act.ParsedPacket) -> None:
        append(packet)

    # Start parsing
    try:
        with args.input_file.open(mode="r") as logs:
            # Parse
            for line in logs:
                twelite.parse_line(line)

            # Ensure dict of dataframes is not empty
            if not df_dict:
                raise ValueError("Parsing failed. The given file is invalid.")

            # Write file
            if args.use_excel:
                # Excel
                export_path = args.input_file.with_suffix(".xlsx")
                with pd.ExcelWriter(export_path, engine="xlsxwriter") as writer:
                    for packet_type, df in df_dict.items():
                        # Format dataframe
                        df = df.drop(columns=["time_parsed"])
                        if args.sort:
                            df = df.sort_index(axis="columns")

                        # Write dataframe
                        df.to_excel(writer, sheet_name=packet_type.title(), index=False)

                        # Get the excel sheet
                        sheet = writer.sheets[packet_type.title()]

                        # Write a header row with format
                        header_format = writer.book.add_format(
                            {"bold": True, "align": "left", "valign": "vcenter"}
                        )
                        for col_num, value in enumerate(df.columns.values):
                            sheet.write(0, col_num, value, header_format)

                        # Format body
                        body_format = writer.book.add_format(
                            {"align": "right", "valign": "vcenter"}
                        )
                        sheet.set_column_pixels("A:XFD", 80, body_format)

                        # Alternate row colors
                        body_format_even = writer.book.add_format(
                            {"bg_color": "#efefef"}
                        )
                        sheet.conditional_format(
                            "A1:XFD1048576",
                            {
                                "type": "formula",
                                "criteria": "=MOD(ROW(),2) = 0",
                                "format": body_format_even,
                            },
                        )
            else:
                # CSV
                export_path = args.input_file.with_suffix(".csv")

                # Merge dataframes and format
                df_concat = pd.concat(
                    df_dict.values(), ignore_index=True, join="outer"
                ).drop(columns=["time_parsed"])
                if args.sort:
                    df_concat = df_concat.sort_index(axis="columns")

                # Write dataframe
                df_concat.to_csv(export_path)

            # Result
            print(f"Exported {export_path.resolve()}")

            # Open file if want
            user_input = mw.utils.ask_user(
                f"Open {export_path.name}? [Y/n]: ",
                regex=r"^[YyNn]$|^$",
                on_error="Please type y or n.",
            )
            if not user_input or user_input == "Y" or user_input == "y":
                mw.utils.open_on_system(export_path)

    except KeyboardInterrupt:
        print("...Aborting")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    # Handle command arguments
    parser = argparse.ArgumentParser(description="Parse a log file for App_Wings")
    parser.add_argument(
        "input_file",
        type=Path,
        help="text file contains logs from App_Wings",
        metavar="INPUT_FILE",
    )
    parser.add_argument(
        "-x",
        "--excel",
        dest="use_excel",
        required=False,
        action="store_true",
        help="export an Excel file instead of CSV",
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
