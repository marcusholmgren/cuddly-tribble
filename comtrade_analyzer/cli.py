import argparse
from comtrade_analyzer.analyzer import ComtradeAnalyzer

def main():
    """
    The main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="A tool for analyzing COMTRADE files for erroneous patterns."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for conformance analysis
    parser_conformance = subparsers.add_parser(
        "conformance", help="Check for conformance errors in the COMTRADE file."
    )
    parser_conformance.add_argument("cfg_file", help="Path to the COMTRADE .cfg file.")
    parser_conformance.add_argument(
        "--freq", type=float, default=60.0, help="Expected line frequency."
    )

    # Subparser for fault analysis
    parser_faults = subparsers.add_parser(
        "faults", help="Analyze electrical fault patterns."
    )
    parser_faults.add_argument("cfg_file", help="Path to the COMTRADE .cfg file.")
    parser_faults.add_argument(
        "--voltage-ch", required=True, help="ID of the voltage channel to analyze."
    )
    parser_faults.add_argument(
        "--current-ch", required=True, help="ID of the current channel for saturation detection."
    )
    parser_faults.add_argument(
        "--trip-ch", required=True, help="ID of the digital trip channel."
    )
    parser_faults.add_argument(
        "--nominal-v", type=float, required=True, help="Nominal voltage."
    )

    args = parser.parse_args()
    analyzer = ComtradeAnalyzer(args.cfg_file)

    if args.command == "conformance":
        run_conformance_checks(analyzer, args)
    elif args.command == "faults":
        run_fault_analysis(analyzer, args)

def run_conformance_checks(analyzer: ComtradeAnalyzer, args):
    """
    Runs and prints the results of conformance checks.
    """
    print("Running conformance checks...")
    errors = analyzer.check_channel_counts()
    errors.extend(analyzer.check_file_type())
    warnings = analyzer.check_for_missing_information(expected_freq=args.freq)

    if not errors and not warnings:
        print("No conformance issues found.")
    else:
        for error in errors:
            print(error)
        for warning in warnings:
            print(warning)

def run_fault_analysis(analyzer: ComtradeAnalyzer, args):
    """
    Runs and prints the results of fault analysis.
    """
    print("Running fault analysis...")
    sags = analyzer.detect_voltage_sags(args.voltage_ch, args.nominal_v)
    if sags:
        sag = sags[0]
        if "error" in sag:
            print(f"Error detecting voltage sags: {sag['error']}")
            return

        print(f"Voltage sag detected on '{sag['channel_id']}' at {sag['start_time']:.4f}s.")

        trip_info = analyzer.check_relay_operation(args.trip_ch, sag['start_time'])
        if "warning" in trip_info:
            print(f"Relay operation check: {trip_info['warning']}")
        else:
            print(f"Relay trip detected at {trip_info['trip_time']:.4f}s (Delay: {trip_info['trip_delay_ms']:.2f}ms).")
    else:
        print("No voltage sags detected.")

    saturation_info = analyzer.detect_ct_saturation(args.current_ch)
    if saturation_info and "warning" not in saturation_info:
        print(f"Potential CT saturation detected on '{args.current_ch}' at {saturation_info['saturation_start_time']:.4f}s.")
    elif saturation_info and "warning" in saturation_info:
        print(f"CT saturation check: {saturation_info['warning']}")
    else:
        print("No CT saturation detected.")
