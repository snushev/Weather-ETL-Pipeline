import pandas as pd
from app.transformer import process_data


def test_process_data_success():
    """Test for success data transformation"""

    input_data = {
        'weather': [{'main': 'Clear', 'description': 'clear sky'}],
        'main': {'humidity': 65, 'pressure': 1013},
        'wind': {'speed': 3.5},
        'sys': {'sunrise': 1698217200, 'sunset': 1698256800},
        'dt': 1698237000
    }

    result = process_data(input_data)

    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['weather', 'description', 'humidity', 'pressure',
                                    'wind_speed', 'sunrise', 'sunset', 'timestamp', 'time_added']


def test_process_data_empty_input():
    """Test for empty input"""

    assert process_data(None) is None
    assert process_data({}) is None


def test_process_data_missing_keys():
    """Test for missing keys"""

    input_data = {
        'weather': [{'main': 'Clear', 'description': 'clear sky'}],
        'main': {'humidity': 65, 'pressure': 1013}
    }

    assert process_data(input_data) is None
