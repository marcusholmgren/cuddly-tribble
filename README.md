# COMTRADE Analysis Tool

This project is a Python-based library and command-line tool for analyzing Common Format for Transient Data Exchange (COMTRADE) files. It helps electrical engineers identify conformance errors and electrical fault patterns in power system disturbance data.

## Features

- **Conformance Checking:** Validates COMTRADE files for common formatting errors.
- **Fault Analysis:** Detects electrical patterns like voltage sags, relay trips, and CT saturation.
- **Library and CLI:** Can be used as a standalone command-line tool or as a library integrated into other Python applications.

## Installation

To use this tool, you need Python 3.12+ and `uv`.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd cuddly-tribble
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Usage

### As a Command-Line Tool

The CLI provides two main commands: `conformance` and `faults`.

#### Information

You can use it to display information about a COMTRADE file, including the available channel IDs, which should help with using the faults command.

For example:
```bash
uv run main.py info comtrade_files/sample_1999_bin.cfg
```

#### Conformance Analysis

Checks for file format issues.

```bash
uv run main.py conformance /path/to/your/file.cfg
```

**Example:**
```bash
uv run main.py conformance comtrade_files/sample_1999_bin.cfg
```

#### Fault Pattern Analysis

Analyzes the waveform data to find electrical fault patterns.

```bash
uv run main.py faults /path/to/your/file.cfg --voltage-ch <ID> --current-ch <ID> --trip-ch <ID> --nominal-v <voltage>
```

**Arguments:**

-   `--voltage-ch`: The channel ID for voltage analysis (e.g., `VA`).
-   `--current-ch`: The channel ID for current analysis (e.g., `IA`).
-   `--trip-ch`: The channel ID for the relay trip signal (e.g., `TRIP`).
-   `--nominal-v`: The nominal voltage of the system.

**Example:**
```bash
uv run main.py faults comtrade_files/sample_1999_bin.cfg --voltage-ch VA --current-ch IA --trip-ch TRIP --nominal-v 230
```

### As a Library

You can integrate the `ComtradeAnalyzer` class into your own Python scripts.

```python
from comtrade_analyzer.analyzer import ComtradeAnalyzer

# Initialize the analyzer
analyzer = ComtradeAnalyzer("comtrade_files/sample_1999_bin.cfg")

# Perform conformance checks
conformance_errors = analyzer.check_channel_counts()
conformance_errors.extend(analyzer.check_file_type())
print(f"Conformance Errors: {conformance_errors}")

# Detect voltage sags
sags = analyzer.detect_voltage_sags("VA", nominal_voltage=230)
print(f"Voltage Sags: {sags}")

# Check relay operation if a sag is detected
if sags:
    trip_info = analyzer.check_relay_operation("TRIP", sags[0]['start_time'])
    print(f"Trip Info: {trip_info}")
```

## Running Tests

To run the test suite, use the following command:
```bash
uv run pytest
```
