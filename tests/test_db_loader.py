import pandas as pd
from app.db_loader import get_connection, create_table, load_to_db


def test_get_connection_success(mocker):
    """Test successful database connection"""
    mock_conn = mocker.Mock()
    mock_connect = mocker.patch('app.db_loader.psycopg2.connect', return_value=mock_conn)

    result = get_connection()

    assert result is not None
    assert result == mock_conn
    mock_connect.assert_called_once()


def test_get_connection_failure(mocker):
    """Test failed database connection"""
    mocker.patch('app.db_loader.psycopg2.connect', side_effect=Exception("Connection failed"))

    result = get_connection()

    assert result is None


def test_create_table_success(mocker):
    """Test successful table creation"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)

    create_table()

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_create_table_no_connection(mocker):
    """Test table creation when connection fails"""
    mocker.patch('app.db_loader.get_connection', return_value=None)

    create_table()


def test_load_to_db_success(mocker):
    """Test successful data load to database"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)
    mocker.patch('app.db_loader.execute_values')

    df = pd.DataFrame({
        'weather': ["Cloudy"],
        'description': ['Partial clouds'],
        'humidity': [67],
        'pressure': [1234],
        'wind_speed': [14],
        'sunrise': [pd.Timestamp.now() + pd.Timedelta(hours=5)],
        'sunset': [pd.Timestamp.now() + pd.Timedelta(hours=17)],
        'time_added': [pd.Timestamp.now()]
    })

    load_to_db(df)

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_load_to_db_empty_dataframe():
    """Test loading empty dataframe"""
    df = pd.DataFrame()
    load_to_db(df)


def test_load_to_db_none():
    """Test loading None input"""
    load_to_db(None)


def test_load_to_db_connection_failure(mocker):
    """Test loading when database connection fails"""
    mocker.patch('app.db_loader.get_connection', return_value=None)
    df = pd.DataFrame({'currency': ['USD']})

    load_to_db(df)


def test_load_to_db_insert_error(mocker):
    """Test handling of insert errors"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)

    df = pd.DataFrame({
        'weather': ["Cloudy"],
        'description': ['Partial clouds'],
        'humidity': [67],
        'pressure': [1234],
        'wind_speed': [14],
        'sunrise': [pd.Timestamp.now() + pd.Timedelta(hours=5)],
        'sunset': [pd.Timestamp.now() + pd.Timedelta(hours=17)],
        'time_added': [pd.Timestamp.now()]
    })

    load_to_db(df)

    mock_conn.close.assert_called_once()
