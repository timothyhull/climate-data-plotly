#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
from datetime import datetime
from json import loads
from pathlib import PosixPath
from typing import Callable, List

# Imports - Third-Party
from pytest import fixture, mark, raises
from requests.exceptions import HTTPError
import requests_mock.mocker
import requests_mock

# Imports - Local
from app.ClimateData import (
    ATMOSPHERIC_CO2_URL, ClimateData
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
    }]
}'''
MOCK_RAW_CO2_LIST = [
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
MOCK_TRANSPOSED_GRAPHING_DATA = [
    (
        datetime(1958, 3, 1, 0, 0),
        datetime(1958, 4, 1, 0, 0),
        datetime(1958, 5, 1, 0, 0)
    ),
    (
        315.7, 317.45, 317.51
    )
]


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
) -> None:
    """ Test the ClimateData.convert_date_string method.

            Args:
                date_input (List):
                    Mock date string input values.

                date_output (List):
                    Mock expected datetime.datetime return values.

                mock_api_request (Callable):
                    Mock HTTP request and response fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request

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

                 tmp_path (pathlib.PosixPath):
                    pytest fixture to create a temporary directory.
                    Used to pass arguments to the mock_api_request
                    pytest fixture.

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

    assert mock_response == MOCK_RAW_CO2_LIST

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


def test_transpose_data_for_graphing(
    mock_api_request: Callable,
) -> None:
    """ Test the ClimateData.transpose_data_for_graphing method.

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
    mock_api_request

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Create a dictionary comprehension of the data in MOCK_RAW_CO2_LIST
    cd._get_co2_ppm_date_data()

    # Call the transpose_data_for_graphing method
    mock_response = cd.transpose_data_for_graphing(
        data=MOCK_RAW_CO2_LIST
    )

    assert mock_response == MOCK_TRANSPOSED_GRAPHING_DATA

    return None


def test_plot_atmospheric_co2_data() -> None:
    """ Test the ClimateData.plot_atmospheric_co2_data method.

            Args:
                None.

            Returns:
                None.
        """

    # TODO

    return None


def test_get_co2_ppm_date_data() -> None:
    """ Test the ClimateData._get_co2_ppm_date_data method.

            Args:
                None.

            Returns:
                None.
        """

    # TODO

    return None


def test_get_co2_yoy_change_data() -> None:
    """ Test the ClimateData._get_co2_yoy_change_data method.

            Args:
                None.

            Returns:
                None.
        """

    # TODO

    return None
