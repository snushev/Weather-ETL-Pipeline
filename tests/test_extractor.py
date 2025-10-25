import pytest
import requests
from app.extractor import fetch_data


def test_fetch_data_success(mocker):
    """Test successful API data fetch with correct parameters"""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'weather': [{'main': 'Clear'}],
        'main': {'temp': 25.5},
        'name': 'Sofia'
    }

    mock_response.status_code = 200
    mock_get = mocker.patch('app.extractor.requests.get', return_value=mock_response)

    result = fetch_data()

    assert result is not None
    assert 'weather' in result
    assert result['main']['temp'] == 25.5
    mock_get.assert_called_once()

    call_kwargs = mock_get.call_args.kwargs
    assert 'params' in call_kwargs
    assert call_kwargs['params']['units'] == 'metric'
    assert call_kwargs['params']['cng'] == 4


def test_fetch_data_timeout(mocker):
    """Test API timeout handling"""
    mocker.patch('app.extractor.requests.get', side_effect=requests.exceptions.Timeout())

    result = fetch_data()

    assert result is None


def test_fetch_data_missing_api_key(mocker):
    """Test behavior when API key is missing"""
    mocker.patch('app.config.API_URL', '')

    result = fetch_data()

    assert result is None


def test_fetch_data_httperror(mocker):
    """Test handling of server error"""
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch('app.extractor.requests.get', return_value=mock_response)

    result = fetch_data()

    assert result is None


@pytest.mark.integration
def test_fetch_data_real_api():
    """Integration test with real API"""
    result = fetch_data()

    if result:
        assert 'weather' in result
        assert 'main' in result
