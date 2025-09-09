import comtrade
import numpy as np

class ComtradeAnalyzer:
    """
    A class to analyze COMTRADE files for conformance errors and fault patterns.
    """
    def __init__(self, cfg_path: str):
        """
        Initializes the ComtradeAnalyzer with a path to the .cfg file.

        :param cfg_path: The path to the COMTRADE .cfg file.
        """
        self.cfg_path = cfg_path
        self.dat_path = cfg_path.replace('.cfg', '.dat').replace('.CFG', '.DAT')
        self.recorder = comtrade.load(self.cfg_path, self.dat_path)

    @property
    def cfg(self):
        """
        Returns the CFG data of the COMTRADE file.
        """
        return self.recorder.cfg

    @property
    def analog_channels(self):
        """
        Returns the analog channels' data.
        """
        return self.recorder.analog

    @property
    def status_channels(self):
        """
        Returns the status channels' data.
        """
        return self.recorder.status

    @property
    def time(self):
        """
        Returns the time vector of the COMTRADE recording.
        """
        return self.recorder.time

    @property
    def trigger_time(self):
        """
        Returns the trigger time of the COMTRADE recording.
        """
        return self.recorder.trigger_time

    def check_channel_counts(self) -> list:
        """
        Checks if the total number of channels in the CFG file matches the sum
        of analog and digital channels.

        :return: A list of error messages. An empty list means no errors.
        """
        errors = []
        expected_total = self.cfg.analog_count + self.cfg.status_count
        if self.cfg.channels_count != expected_total:
            error_msg = (
                f"Error: Mismatched channel counts. "
                f"Total in CFG: {self.cfg.channels_count}, "
                f"Sum of analog and status: {expected_total}"
            )
            errors.append(error_msg)
        return errors

    def check_file_type(self) -> list:
        """
        Checks if the file type in the CFG is valid.

        :return: A list of error messages.
        """
        errors = []
        if self.cfg.ft not in ['ASCII', 'BINARY']:
            errors.append(f"Error: Invalid file type '{self.cfg.ft}'")
        return errors

    def check_for_missing_information(self, expected_freq: float = 60.0) -> list:
        """
        Checks for missing or invalid metadata, like line frequency.

        :param expected_freq: The expected line frequency (e.g., 50.0 or 60.0).
        :return: A list of warning or error messages.
        """
        warnings = []
        if self.cfg.frequency == 0.0 or abs(self.cfg.frequency - expected_freq) > 1.0:
            warnings.append(
                f"Warning: Unexpected frequency detected ({self.cfg.frequency} Hz)."
            )
        return warnings

    def _find_channel_index(self, channel_id: str, channel_type: str = "analog") -> int | None:
        """
        Finds the index of a channel by its ID, case-insensitively.

        :param channel_id: The ID of the channel to find.
        :param channel_type: The type of channel ('analog' or 'status').
        :return: The index of the channel, or None if not found.
        """
        channel_list = self.recorder.analog_channel_ids if channel_type == "analog" else self.recorder.status_channel_ids
        for i, ch_id in enumerate(channel_list):
            if ch_id.strip().lower() == channel_id.lower():
                return i
        return None

    def detect_voltage_sags(
        self,
        voltage_channel_id: str,
        nominal_voltage: float,
        threshold: float = 0.8,
        window_size: int = 50,
    ) -> list:
        """
        Detects voltage sags in a specific analog channel.

        :param voltage_channel_id: The ID of the voltage channel to analyze.
        :param nominal_voltage: The nominal voltage value for calculating the sag threshold.
        :param threshold: The sag threshold (e.g., 0.8 for 80% of nominal voltage).
        :param window_size: The size of the rolling window for RMS calculation.
        :return: A list of dictionaries, each representing a detected sag event.
        """
        sags = []
        voltage_index = self._find_channel_index(voltage_channel_id, "analog")

        if voltage_index is None:
            return [{"error": f"Voltage channel '{voltage_channel_id}' not found."}]

        voltage_data = self.analog_channels[voltage_index]
        rms_values = np.sqrt(
            np.convolve(np.array(voltage_data)**2, np.ones(window_size) / window_size, mode="valid")
        )
        sag_threshold = nominal_voltage * threshold

        sag_indices = np.where(rms_values < sag_threshold)[0]
        if sag_indices.size > 0:
            start_index = sag_indices[0]
            start_time = self.time[start_index]
            sags.append(
                {
                    "channel_id": voltage_channel_id,
                    "start_time": start_time,
                    "min_rms_voltage": rms_values[start_index],
                }
            )
        return sags

    def check_relay_operation(self, trip_channel_id: str, fault_start_time: float) -> dict:
        """
        Checks for a relay trip signal after a fault has occurred.

        :param trip_channel_id: The ID of the status trip channel.
        :param fault_start_time: The time when the fault started.
        :return: A dictionary with the trip time and delay, or a warning if no trip is found.
        """
        trip_index = self._find_channel_index(trip_channel_id, "status")

        if trip_index is None:
            return {"warning": f"Trip channel '{trip_channel_id}' not found."}

        trip_data = self.status_channels[trip_index]
        trip_times = [self.time[i] for i, val in enumerate(trip_data) if val == 1]

        if trip_times and trip_times[0] > fault_start_time:
            trip_time = trip_times[0]
            trip_delay = trip_time - fault_start_time
            return {
                "trip_time": trip_time,
                "trip_delay_ms": trip_delay * 1000,
            }
        else:
            return {"warning": "No trip signal detected after the fault."}

    def detect_ct_saturation(self, current_channel_id: str, saturation_window: int = 5) -> dict | None:
        """
        Detects potential CT saturation by looking for flattened waveforms.

        :param current_channel_id: The ID of the current channel to analyze.
        :param saturation_window: The number of consecutive identical samples to consider as saturation.
        :return: A dictionary with the saturation start time, or None if no saturation is detected.
        """
        current_index = self._find_channel_index(current_channel_id, "analog")

        if current_index is None:
            return {"warning": f"Current channel '{current_channel_id}' not found."}

        current_data = self.analog_channels[current_index]
        for i in range(len(current_data) - saturation_window):
            window = current_data[i : i + saturation_window]
            if np.all(window == window[0]):
                return {"saturation_start_time": self.time[i]}
        return None
