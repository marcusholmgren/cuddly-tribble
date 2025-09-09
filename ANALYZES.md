An electrical engineer analyzes COMTRADE files to understand what happened during a power system disturbance or fault. The goal is to identify patterns that indicate whether the protective equipment operated correctly or if there was an issue. The analysis can be broken down into two main areas: **conformance errors** and **data analysis to find electrical fault patterns**.

### Analyzing for Erroneous Patterns

  * **Conformance Errors:** These are issues with the file format itself that can make the data unreliable or unreadable. An engineer would check for things like:
      * **Mismatched Channel Counts:** The number of analog or digital channels listed in the .CFG file does not match the actual number of channels with data in the .DAT file.
      * **Incorrect File Type:** The file type specified in the .CFG file doesn't correspond to the data format (.ASCII or .BINARY).
      * **Missing or Incorrect Information:** Critical metadata like the sampling rate, line frequency, or station name is missing or corrupted.
  * **Electrical Fault Patterns:** An engineer analyzes the waveform data to see if it matches the expected behavior for a particular event. This involves looking at the following:
      * **Pre-fault vs. Post-fault Data:** The waveform should be stable and sinusoidal before the fault, then show a sudden, significant change in magnitude (e.g., a massive spike in current or a dip in voltage) at the fault inception time.
      * **Correct Relay Operation:** The digital channels for the relay trip signals should show a change of state (e.g., from 0 to 1) at the appropriate time after the fault is detected, and the circuit breaker status channel should change state shortly after. An erroneous pattern would be a slow trip or a trip that occurs when no fault is present.
      * **Current Transformer (CT) Saturation:** A CT is used to step down high currents. If the waveform for a current channel suddenly flattens or distorts during a high-current event, it could indicate the CT has saturated, which means it is no longer accurately measuring the current.

-----

### Implementation with Python and `python-comtrade`

The `python-comtrade` library can be used to load the files and access the data for analysis. The library handles the parsing of the `.CFG`, `.DAT`, and `.HDR` files, making it easy to work with the data in Python.

Here are some examples of how an engineer could use the library to detect erroneous patterns.

#### 1\. Loading the Data

First, you need to load the COMTRADE files. Assuming your files are named `fault_record.CFG` and `fault_record.DAT`, you can load them like this:

```python
import comtrade

try:
    rec = comtrade.load('fault_record.CFG', 'fault_record.DAT')
    print("COMTRADE file loaded successfully.")
except Exception as e:
    print(f"Error loading COMTRADE files: {e}")
```

#### 2\. Checking for Conformance Errors

You can check some basic conformance properties using the loaded `rec` object.

```python
# Check for a valid frequency and channel count
expected_frequency = 60.0  # Or 50.0 Hz
if rec.cfg.frequency == 0.0 or abs(rec.cfg.frequency - expected_frequency) > 1.0:
    print(f"Warning: Unexpected frequency detected ({rec.cfg.frequency} Hz).")

if rec.cfg.channels_count != (rec.cfg.analog_count + rec.cfg.digital_count):
    print("Error: The total number of channels does not match the sum of analog and digital channels.")
```

#### 3\. Analyzing Electrical Fault Patterns

To detect electrical patterns, you can analyze the analog and digital channel data. Here's an example of how to identify a voltage sag (a common fault pattern) and check for a corresponding relay trip.

```python
import numpy as np
import matplotlib.pyplot as plt

# Access the voltage data and find the channel
# The channel ID is in rec.analog_channel_ids. For this example, let's assume 'VA' is a phase voltage.
voltage_channel_id = 'VA'
try:
    voltage_index = rec.analog_channel_ids.index(voltage_channel_id)
except ValueError:
    print(f"Voltage channel '{voltage_channel_id}' not found.")
    voltage_index = None

if voltage_index is not None:
    voltage_data = rec.analog[voltage_index]

    # Calculate the RMS voltage in a rolling window to detect a sag
    # This is a simplified example; a real-world application might use a more sophisticated algorithm
    window_size = 50  # 50 samples
    rms_values = np.sqrt(np.convolve(voltage_data**2, np.ones(window_size)/window_size, mode='valid'))

    # Define a threshold for a voltage sag (e.g., 80% of nominal voltage)
    nominal_voltage = 120.0  # Example nominal voltage
    sag_threshold = nominal_voltage * 0.8

    # Find the time and index of the first sag
    sag_start_index = np.where(rms_values < sag_threshold)[0]

    if sag_start_index.size > 0:
        sag_start_time = rec.time[sag_start_index[0]]
        print(f"Possible voltage sag detected on channel '{voltage_channel_id}' at {sag_start_time:.4f} seconds.")

        # Now check if a digital trip signal occurred after the sag
        # Let's assume a trip signal channel named 'TRIP' exists
        trip_channel_id = 'TRIP'
        try:
            trip_index = rec.digital_channel_ids.index(trip_channel_id)
            trip_data = rec.digital[trip_index]

            # Find the first '1' in the trip data after the sag
            # The '1' indicates the trip signal is active
            trip_times = [rec.time[i] for i, val in enumerate(trip_data) if val == 1]

            if trip_times and trip_times[0] > sag_start_time:
                trip_time = trip_times[0]
                print(f"Relay trip signal detected at {trip_time:.4f} seconds.")
                trip_delay = trip_time - sag_start_time
                print(f"Trip delay: {trip_delay * 1000:.2f} ms. Check if this is within acceptable limits.")
            else:
                print("Warning: No trip signal detected after the voltage sag.")
        except ValueError:
            print(f"Trip channel '{trip_channel_id}' not found.")

# You can also use matplotlib to plot the data for visual analysis
plt.figure()
plt.plot(rec.time, rec.analog[voltage_index])
plt.title(f'Voltage Channel: {voltage_channel_id}')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.axvline(x=rec.trigger_time, color='r', linestyle='--', label='Trigger Time')
plt.legend()
plt.grid(True)
plt.show()
```

This code demonstrates how to use `python-comtrade` to not only load the data but also perform basic calculations and visual analysis to identify potential issues, mirroring how an engineer would approach the problem manually.An electrical engineer analyzes COMTRADE files to understand what happened during a power system disturbance or fault. The goal is to identify patterns that indicate whether the protective equipment operated correctly or if there was an issue. The analysis can be broken down into two main areas: **conformance errors** and **data analysis to find electrical fault patterns**.

### Analyzing for Erroneous Patterns

  * **Conformance Errors:** These are issues with the file format itself that can make the data unreliable or unreadable. An engineer would check for things like:
      * **Mismatched Channel Counts:** The number of analog or digital channels listed in the .CFG file does not match the actual number of channels with data in the .DAT file.
      * **Incorrect File Type:** The file type specified in the .CFG file doesn't correspond to the data format (.ASCII or .BINARY).
      * **Missing or Incorrect Information:** Critical metadata like the sampling rate, line frequency, or station name is missing or corrupted.
  * **Electrical Fault Patterns:** An engineer analyzes the waveform data to see if it matches the expected behavior for a particular event. This involves looking at the following:
      * **Pre-fault vs. Post-fault Data:** The waveform should be stable and sinusoidal before the fault, then show a sudden, significant change in magnitude (e.g., a massive spike in current or a dip in voltage) at the fault inception time.
      * **Correct Relay Operation:** The digital channels for the relay trip signals should show a change of state (e.g., from 0 to 1) at the appropriate time after the fault is detected, and the circuit breaker status channel should change state shortly after. An erroneous pattern would be a slow trip or a trip that occurs when no fault is present.
      * **Current Transformer (CT) Saturation:** A CT is used to step down high currents. If the waveform for a current channel suddenly flattens or distorts during a high-current event, it could indicate the CT has saturated, which means it is no longer accurately measuring the current.

-----

### Implementation with Python and `python-comtrade`

The `python-comtrade` library can be used to load the files and access the data for analysis. The library handles the parsing of the `.CFG`, `.DAT`, and `.HDR` files, making it easy to work with the data in Python.

Here are some examples of how an engineer could use the library to detect erroneous patterns.

#### 1\. Loading the Data

First, you need to load the COMTRADE files. Assuming your files are named `fault_record.CFG` and `fault_record.DAT`, you can load them like this:

```python
import comtrade

try:
    rec = comtrade.load('fault_record.CFG', 'fault_record.DAT')
    print("COMTRADE file loaded successfully.")
except Exception as e:
    print(f"Error loading COMTRADE files: {e}")
```

#### 2\. Checking for Conformance Errors

You can check some basic conformance properties using the loaded `rec` object.

```python
# Check for a valid frequency and channel count
expected_frequency = 60.0  # Or 50.0 Hz
if rec.cfg.frequency == 0.0 or abs(rec.cfg.frequency - expected_frequency) > 1.0:
    print(f"Warning: Unexpected frequency detected ({rec.cfg.frequency} Hz).")

if rec.cfg.channels_count != (rec.cfg.analog_count + rec.cfg.digital_count):
    print("Error: The total number of channels does not match the sum of analog and digital channels.")
```

#### 3\. Analyzing Electrical Fault Patterns

To detect electrical patterns, you can analyze the analog and digital channel data. Here's an example of how to identify a voltage sag (a common fault pattern) and check for a corresponding relay trip.

```python
import numpy as np
import matplotlib.pyplot as plt

# Access the voltage data and find the channel
# The channel ID is in rec.analog_channel_ids. For this example, let's assume 'VA' is a phase voltage.
voltage_channel_id = 'VA'
try:
    voltage_index = rec.analog_channel_ids.index(voltage_channel_id)
except ValueError:
    print(f"Voltage channel '{voltage_channel_id}' not found.")
    voltage_index = None

if voltage_index is not None:
    voltage_data = rec.analog[voltage_index]

    # Calculate the RMS voltage in a rolling window to detect a sag
    # This is a simplified example; a real-world application might use a more sophisticated algorithm
    window_size = 50  # 50 samples
    rms_values = np.sqrt(np.convolve(voltage_data**2, np.ones(window_size)/window_size, mode='valid'))

    # Define a threshold for a voltage sag (e.g., 80% of nominal voltage)
    nominal_voltage = 120.0  # Example nominal voltage
    sag_threshold = nominal_voltage * 0.8

    # Find the time and index of the first sag
    sag_start_index = np.where(rms_values < sag_threshold)[0]

    if sag_start_index.size > 0:
        sag_start_time = rec.time[sag_start_index[0]]
        print(f"Possible voltage sag detected on channel '{voltage_channel_id}' at {sag_start_time:.4f} seconds.")

        # Now check if a digital trip signal occurred after the sag
        # Let's assume a trip signal channel named 'TRIP' exists
        trip_channel_id = 'TRIP'
        try:
            trip_index = rec.digital_channel_ids.index(trip_channel_id)
            trip_data = rec.digital[trip_index]

            # Find the first '1' in the trip data after the sag
            # The '1' indicates the trip signal is active
            trip_times = [rec.time[i] for i, val in enumerate(trip_data) if val == 1]

            if trip_times and trip_times[0] > sag_start_time:
                trip_time = trip_times[0]
                print(f"Relay trip signal detected at {trip_time:.4f} seconds.")
                trip_delay = trip_time - sag_start_time
                print(f"Trip delay: {trip_delay * 1000:.2f} ms. Check if this is within acceptable limits.")
            else:
                print("Warning: No trip signal detected after the voltage sag.")
        except ValueError:
            print(f"Trip channel '{trip_channel_id}' not found.")

# You can also use matplotlib to plot the data for visual analysis
plt.figure()
plt.plot(rec.time, rec.analog[voltage_index])
plt.title(f'Voltage Channel: {voltage_channel_id}')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.axvline(x=rec.trigger_time, color='r', linestyle='--', label='Trigger Time')
plt.legend()
plt.grid(True)
plt.show()
```

This code demonstrates how to use `python-comtrade` to not only load the data but also perform basic calculations and visual analysis to identify potential issues, mirroring how an engineer would approach the problem manually.
