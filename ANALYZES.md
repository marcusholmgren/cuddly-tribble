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
      * **Voltage Sags and Swells**: A voltage sag is a short-duration reduction in RMS voltage, while a swell is a short-duration increase. Both can indicate a fault or other power quality issue.
      * **Frequency Deviations**: The power system frequency should remain stable. Deviations from the nominal frequency can indicate a significant imbalance between generation and load.
