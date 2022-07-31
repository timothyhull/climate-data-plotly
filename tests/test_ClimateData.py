#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
import builtins
from datetime import datetime
from json import loads
from pathlib import PosixPath
from typing import Callable, List
from unittest.mock import patch

# Imports - Third-Party
from pytest import fixture, mark, raises
from requests.exceptions import HTTPError
import requests_mock.mocker
import requests_mock

# Imports - Local
from app.ClimateData import (
    ATMOSPHERIC_CO2_URL, ClimateData, TransposedData
)

# Constants
DATE_STR_INPUTS = [
    '1980M05',
    '1980M11',
    '2007M12',
    '2010M09'
]
DATE_STR_OUTPUTS = [
    datetime(1980, 5, 1, 0, 0),
    datetime(1980, 11, 1, 0, 0),
    datetime(2007, 12, 1, 0, 0),
    datetime(2010, 9, 1, 0, 0)
]
DATE_STR_PARAMS = zip(
    DATE_STR_INPUTS,
    DATE_STR_OUTPUTS
)
DATE_STR_VALUE_ERROR = '20220'
DEFAULT_MOCK_METHOD = 'GET'
MOCK_RAW_CO2_JSON = '''
{
    "features": [{
        "attributes": {
            "Indicator": "Monthly Atmospheric Co2 Concentrations",
            "Code": "ECNCIC_PPM",
            "Unit": "Parts Per Million",
            "Date": "1958M03",
            "Value": 315.7
        }
    },
        {
        "attributes": {
            "Indicator": "Monthly Atmospheric Co2 Concentrations",
            "Code": "ECNCIC_PPM",
            "Unit": "Parts Per Million",
            "Date": "1958M04",
            "Value": 317.45
        }
    },
        {
        "attributes": {
            "Indicator": "Monthly Atmospheric Co2 Concentrations",
            "Code": "ECNCIC_PPM",
            "Unit": "Parts Per Million",
            "Date": "1958M05",
            "Value": 317.51
        }
    },
    {
        "attributes": {
            "Indicator": "Year on Year Percentage Change",
            "Code": "ECNCIC_YOY",
            "Unit": "Percent",
            "Date": "1959M03",
            "Value": 0.3
        }
    },
    {
        "attributes": {
            "Indicator": "Year on Year Percentage Change",
            "Code": "ECNCIC_YOY",
            "Unit": "Percent",
            "Date": "1959M04",
            "Value": 0.09
        }
    },
    {
        "attributes": {
            "Indicator": "Year on Year Percentage Change",
            "Code": "ECNCIC_YOY",
            "Unit": "Percent",
            "Date": "1959M05",
            "Value": 0.25
        }
    }]
}'''
MOCK_RAW_CO2_PPM_LIST = [
    {
        'attributes': {
            'Indicator': 'Monthly Atmospheric Co2 Concentrations',
            'Code': 'ECNCIC_PPM',
            'Unit': 'Parts Per Million',
            'Date': datetime(1958, 3, 1, 0, 0),
            'Value': 315.7
        }
    },
    {
        'attributes': {
            'Indicator': 'Monthly Atmospheric Co2 Concentrations',
            'Code': 'ECNCIC_PPM',
            'Unit': 'Parts Per Million',
            'Date': datetime(1958, 4, 1, 0, 0),
            'Value': 317.45
        }
    },
    {
        'attributes': {
            'Indicator': 'Monthly Atmospheric Co2 Concentrations',
            'Code': 'ECNCIC_PPM',
            'Unit': 'Parts Per Million',
            'Date': datetime(1958, 5, 1, 0, 0),
            'Value': 317.51
        }
    }
]
MOCK_CO2_PPM_DATE_DATA_1 = {
    datetime(1958, 3, 1, 0, 0): 315.7,
    datetime(1958, 4, 1, 0, 0): 317.45,
    datetime(1958, 5, 1, 0, 0): 317.51
}
MOCK_CO2_PPM_DATE_DATA_2 = [
    (
        datetime(1958, 3, 1, 0, 0),
        datetime(1958, 4, 1, 0, 0),
        datetime(1958, 5, 1, 0, 0)
    ),
    (
        315.7,
        317.45,
        317.51
    )
]
MOCK_CO2_PPM_GRAPH_DATA = TransposedData(
    dates=(
        datetime(1958, 3, 1, 0, 0),
        datetime(1958, 4, 1, 0, 0),
        datetime(1958, 5, 1, 0, 0)
    ),
    values=(
        315.7,
        317.45,
        317.51
    )
)
MOCK_RAW_CO2_YOY_LIST = [
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 3, 1, 0, 0),
            'Value': 0.3
        }
    },
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 4, 1, 0, 0),
            'Value': 0.09
        }
    },
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 5, 1, 0, 0),
            'Value': 0.25
        }
    }
]
MOCK_CO2_YOY_DATE_DATA_1 = {
    datetime(1959, 3, 1, 0, 0): 0.3,
    datetime(1959, 4, 1, 0, 0): 0.09,
    datetime(1959, 5, 1, 0, 0): 0.25
}
MOCK_CO2_YOY_DATE_DATA_2 = [
    (
        datetime(1959, 3, 1, 0, 0),
        datetime(1959, 4, 1, 0, 0),
        datetime(1959, 5, 1, 0, 0),
    ),
    (
        0.3,
        0.09,
        0.25
    )
]
MOCK_CO2_YOY_GRAPH_DATA = TransposedData(
    dates=(
        datetime(1959, 3, 1, 0, 0),
        datetime(1959, 4, 1, 0, 0),
        datetime(1959, 5, 1, 0, 0),
    ),
    values=(
        0.3,
        0.09,
        0.25
    )
)
MOCK_CO2_GRAPH_INPUT = [
    MOCK_CO2_PPM_DATE_DATA_1,
    MOCK_CO2_PPM_DATE_DATA_2,
    MOCK_CO2_YOY_DATE_DATA_1,
    MOCK_CO2_YOY_DATE_DATA_2,
]
MOCK_CO2_GRAPH_OUTPUT = [
    MOCK_CO2_PPM_GRAPH_DATA,
    MOCK_CO2_PPM_GRAPH_DATA,
    MOCK_CO2_YOY_GRAPH_DATA,
    MOCK_CO2_YOY_GRAPH_DATA
]
MOCK_CO2_GRAPH_DATA = zip(
    MOCK_CO2_GRAPH_INPUT,
    MOCK_CO2_GRAPH_OUTPUT
)
MOCK_HTML_PLOT_INPUTS = {
    'transposed_data': MOCK_CO2_PPM_GRAPH_DATA,
    'date_label': 'Dates',
    'value_label': 'Atmospheric Co2 PPM',
    'title': 'Atmospheric Co2 Levels',
}
MOCK_HTML_PLOT_SNIPPETS = {
    '<html>': True,
    'window.PlotlyConfig = {MathJaxConfig: \'local\'};</script>': True,
    '* plotly.js v': True,
    '"Dates=%{x}<br>Atmospheric Co2 PPM=%{y}<extra></extra>"': True,
    '"title":{"text":"Atmospheric Co2 Levels"}': True,
    '</body': True,
    '</html>': True,
    '<title>No Plot Content</title>': False,
    '<h1>This plot file contains no content.</h1>': False,
    '<h2>The \'file_content\' parameter accepts HTML content</h2>': False,
}


# pytest fixtures
@fixture
def mock_api_request(
    tmp_path: PosixPath
) -> Callable:
    """ Mock of the HTTP request to the climate data source API.

        Args:
            tmp_path (pathlib.PosixPath):
                pytest fixture to create a temporary directory.

        Returns:
            _mock_api_request (Callable):
                Call to the _mock_api_request function with arguments.
    """

    def _mock_api_request(
        requests_mock: requests_mock.mocker,
        date_error: bool = False,
        status_code: int = 200
    ) -> requests_mock.mocker:
        """ Mock of the HTTP request to the climate data source API.

            Args:
                requests_mock (requests_mock.mocker):
                    pytest fixture to mock requests HTTP objects.

                date_error (bool, optional):
                    Optional date error boolean, default is False.
                    Set to True to raise a ValueError exception.

                status_code (int, optional:
                    Optional HTTP status code, default value is 200.
                    Set to a value between 400-599 to raise an
                    HTTPError exception.

            Returns:
                mock_request (requests_mock.mocker):
                    Mock requests HTTP request and response objects.
        """

        # Setup mock request arguments
        method = DEFAULT_MOCK_METHOD
        url = ATMOSPHERIC_CO2_URL
        json = loads(MOCK_RAW_CO2_JSON)

        # Check for argument to insert an invalid date string into 'json'
        if date_error is True:
            # Update date value in 'json' with an invalid date string
            json['features'][0]['attributes'].update(
                {'Date': DATE_STR_VALUE_ERROR}
            )

        # Create the mock request
        mock_request = requests_mock.request(
            method=method,
            url=url,
            json=json,
            status_code=status_code
        )

        return mock_request

    return _mock_api_request


# Test functions
@mark.parametrize(
    argnames=[
        'date_input',
        'date_output'
    ],
    argvalues=list(
        DATE_STR_PARAMS
    )
)
def test_convert_date_string(
    date_input: List,
    date_output: List,
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the ClimateData.convert_date_string method.

            Args:
                date_input (List):
                    Mock date string input values.

                date_output (List):
                    Mock expected datetime return values.

                mock_api_request (Callable):
                    Mock HTTP request and response fixture.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Assert that _convert_date_string returns the expected values
    assert cd._convert_date_string(
        date_str=date_input
    ) == date_output

    return None


def test_convert_date_string_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the ClimateData.convert_date_string method.

        Includes an invalid date string, to test the ValueError
        exception handling.

            Args:
                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

                tmp_path (pathlib.PosixPath):
                    pytest fixture to create a temporary directory.
                    Used to pass arguments to the mock_api_request
                    pytest fixture.

            Returns:
                None.
        """

    # Use pytest.raises to define the expected exception
    with raises(
        expected_exception=ValueError
    ):
        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock,
            date_error=True
        )

        # Instantiate the ClimateData.ClimateData class
        ClimateData()

    return None


def test_get_atmospheric_co2_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
) -> None:
    """ Test the ClimateData._get_atmospheric_co2_data method.

            Args:
                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the _get_atmospheric_co2_data method
    mock_response = cd._get_atmospheric_co2_data()

    assert mock_response == MOCK_RAW_CO2_PPM_LIST + MOCK_RAW_CO2_YOY_LIST

    return None


def test_get_atmospheric_co2_data_http_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath,
) -> None:
    """ Test the ClimateData._get_atmospheric_co2_data method.

        Determine if the method properly raises an HTTPError with a
        mock bad HTTP status code.

            Args:
                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

                 tmp_path (pathlib.PosixPath):
                    pytest fixture to create a temporary directory.

            Returns:
                None.
        """

    with raises(
        expected_exception=HTTPError
    ):
        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock,
            status_code=400
        )

        # Create an instance of the ClimateData.ClimateData class
        cd = ClimateData()

        # Call the _get_atmospheric_co2_data method
        cd._get_atmospheric_co2_data()

    return None


def test_get_co2_ppm_date_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the ClimateData._get_co2_ppm_date_data method.

            Args:
                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

                 tmp_path (pathlib.PosixPath):
                    pytest fixture to create a temporary directory.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the _get_co2_ppm_date_data method
    mock_response = cd._get_co2_ppm_date_data(
        atmospheric_co2_data=MOCK_RAW_CO2_PPM_LIST
    )

    assert mock_response == MOCK_CO2_PPM_DATE_DATA_1

    return None


def test_get_co2_yoy_change_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the ClimateData._get_co2_yoy_change_data method.

            Args:
                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

                 tmp_path (pathlib.PosixPath):
                    pytest fixture to create a temporary directory.
            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the _get_co2_yoy_change_data method
    mock_response = cd._get_co2_yoy_change_data(
        atmospheric_co2_data=MOCK_RAW_CO2_YOY_LIST
    )

    assert mock_response == MOCK_CO2_YOY_DATE_DATA_1

    return None


@mark.parametrize(
    argnames=[
        'co2_data',
        'co2_graphing_data'
    ],
    argvalues=list(MOCK_CO2_GRAPH_DATA)
)
def test_transpose_data_for_graphing(
    co2_data: List[List],
    co2_graphing_data: TransposedData,
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the ClimateData.transpose_data_for_graphing method.

            Args:
                co2_data: (List[List]):

                co2_graphing_data (TransposedData):

                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the transpose_data_for_graphing method
    mock_response = cd.transpose_data_for_graphing(
        data=co2_data
    )

    assert (
        mock_response == co2_graphing_data
    )

    return None


@mark.parametrize(
    argnames=[
        'html_search_string',
        'expected_value'
    ],
    argvalues=list(MOCK_HTML_PLOT_SNIPPETS.items()),
)
def test_plot_atmospheric_co2_data(
    html_search_string: List[str],
    expected_value: List[bool],
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the ClimateData.plot_atmospheric_co2_data method.

            Args:
                html_search_string (List[str]):
                    Mock Plotly HTML file snippets to search for.

                expected_value (List[bool]):
                    Mock expected boolean return values.

                mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the plot_atmospheric_co2_data method
    mock_response = cd.plot_atmospheric_co2_data(
        **MOCK_HTML_PLOT_INPUTS
    )

    assert (html_search_string in mock_response) is expected_value

    return None


@patch.object(
    target=builtins,
    attribute='open',
    return_value='',
)
def test_write_plot_html_file(
    file_open,
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the ClimateData.write_plot_html_file method.

        Args:
            mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    mock_api_request(
        requests_mock
    )

    cd = ClimateData()

    file_open

    cd.write_plot_html_file(
        'test_1',
        'test_2'
    )

    # with raises(OSError):
    #     cd.write_plot_html_file(

    #     )

    return None
