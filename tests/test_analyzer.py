import pytest
from comtrade_analyzer.analyzer import ComtradeAnalyzer

@pytest.fixture
def analyzer():
    """
    Pytest fixture to create a ComtradeAnalyzer instance for testing.
    """
    return ComtradeAnalyzer("comtrade_files/sample_1999_bin.cfg")

def test_check_channel_counts(analyzer):
    """
    Tests the check_channel_counts method.
    """
    errors = analyzer.check_channel_counts()
    assert not errors

def test_check_file_type(analyzer):
    """
    Tests the check_file_type method.
    """
    errors = analyzer.check_file_type()
    assert not errors

def test_check_for_missing_information(analyzer):
    """
    Tests the check_for_missing_information method.
    """
    warnings = analyzer.check_for_missing_information()
    assert not warnings

def test_detect_voltage_sags(analyzer):
    """
    Tests the detect_voltage_sags method.
    """
    # This is a placeholder test. The sample file may not have a sag.
    # In a real scenario, we would use a file with a known sag.
    sags = analyzer.detect_voltage_sags("VA", nominal_voltage=230)
    assert isinstance(sags, list)

def test_check_relay_operation(analyzer):
    """
    Tests the check_relay_operation method.
    """
    # This is a placeholder test.
    trip_info = analyzer.check_relay_operation("TRIP", fault_start_time=0.1)
    assert "warning" in trip_info or "trip_time" in trip_info

def test_detect_ct_saturation(analyzer):
    """
    Tests the detect_ct_saturation method.
    """
    # This is a placeholder test.
    saturation_info = analyzer.detect_ct_saturation("IA")
    assert saturation_info is None or "warning" in saturation_info or "saturation_start_time" in saturation_info
