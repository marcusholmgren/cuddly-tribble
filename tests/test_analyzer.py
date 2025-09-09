import pytest
from comtrade_analyzer.analyzer import ComtradeAnalyzer


@pytest.fixture
def cfg_analyzer():
    """
    Pytest fixture to create a ComtradeAnalyzer instance for testing with a .cfg file.
    """
    return ComtradeAnalyzer("comtrade_files/sample_1999_bin.cfg")


@pytest.fixture
def cff_analyzer():
    """
    Pytest fixture to create a ComtradeAnalyzer instance for testing with a .cff file.
    """
    return ComtradeAnalyzer("comtrade_files/sample_2013_ascii.cff")


def test_load_cff_file(cff_analyzer):
    """
    Tests if a .cff file can be loaded successfully.
    """
    assert cff_analyzer.recorder is not None
    assert cff_analyzer.cfg.station_name == "SMARTSTATION"


def test_load_with_encoding():
    """
    Tests loading a file with a specific encoding.
    """
    analyzer = ComtradeAnalyzer(
        "comtrade_files/sample_2013_ascii_utf8.cfg", encoding="utf-8"
    )
    assert analyzer.recorder is not None
    assert (
        analyzer.cfg.station_name
        == "SMARTSTATION testing text encoding: hgvcj터파크387"
    )


def test_check_channel_counts(cfg_analyzer):
    """
    Tests the check_channel_counts method.
    """
    errors = cfg_analyzer.check_channel_counts()
    assert not errors


def test_check_file_type(cfg_analyzer):
    """
    Tests the check_file_type method.
    """
    errors = cfg_analyzer.check_file_type()
    assert not errors


def test_check_for_missing_information(cfg_analyzer):
    """
    Tests the check_for_missing_information method.
    """
    warnings = cfg_analyzer.check_for_missing_information()
    assert not warnings


def test_detect_voltage_sags(cfg_analyzer):
    """
    Tests the detect_voltage_sags method.
    """
    # This is a placeholder test. The sample file may not have a sag.
    # In a real scenario, we would use a file with a known sag.
    sags = cfg_analyzer.detect_voltage_sags("VA", nominal_voltage=230)
    assert isinstance(sags, list)


def test_detect_voltage_swells(cfg_analyzer):
    """
    Tests the detect_voltage_swells method.
    """
    # This is a placeholder test. The sample file may not have a swell.
    # In a real scenario, we would use a file with a known swell.
    swells = cfg_analyzer.detect_voltage_swells("VA", nominal_voltage=230)
    assert isinstance(swells, list)


def test_check_relay_operation(cfg_analyzer):
    """
    Tests the check_relay_operation method.
    """
    # This is a placeholder test.
    trip_info = cfg_analyzer.check_relay_operation("TRIP", fault_start_time=0.1)
    assert "warning" in trip_info or "trip_time" in trip_info


def test_detect_ct_saturation(cfg_analyzer):
    """
    Tests the detect_ct_saturation method.
    """
    # This is a placeholder test.
    saturation_info = cfg_analyzer.detect_ct_saturation("IA")
    assert (
        saturation_info is None
        or "warning" in saturation_info
        or "saturation_start_time" in saturation_info
    )
