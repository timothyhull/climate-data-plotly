#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
from datetime import datetime
from json import loads
from typing import List

# Imports - Third-Party
from pytest import fixture, mark, raises
# from requests import HTTPError
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


# pytest fixtures
@fixture
def mock_api_request(
    requests_mock: requests_mock.mocker
):
    """ Mock of the HTTP request to the climate data source API.

        Args:
            requests_mock (requests_mock.mocker):
                pytest fixture to mock requests HTTP objects.

        Returns:
            mock_request (requests_mock.mocker):
                Mock requests HTTP request and response objects.
    """

    # Setup mock request arguments
    method = DEFAULT_MOCK_METHOD
    url = ATMOSPHERIC_CO2_URL
    json = loads(MOCK_RAW_CO2_JSON)

    # Create the mock request
    mock_request = requests_mock.request(
        method=method,
        url=url,
        json=json
    )

    return mock_request


@fixture
def mock_api_request_date_error(
    requests_mock: requests_mock.mocker,
):
    """ Mock of the HTTP request to the climate data source API.

        Includes an invalid date string, to test the ValueError
        exception handling.

        Args:
            requests_mock (requests_mock.mocker):
                pytest fixture to mock requests HTTP objects.

        Returns:
            mock_request (requests_mock.mocker):
                Mock requests HTTP request and response objects.
    """

    # Setup mock request arguments
    method = DEFAULT_MOCK_METHOD
    url = ATMOSPHERIC_CO2_URL
    json = loads(MOCK_RAW_CO2_JSON)

    # Insert an invalid date string in the json variable
    json['features'][0]['attributes'].update(
        {'Date': DATE_STR_VALUE_ERROR}
    )

    # Create the mock request
    mock_request = requests_mock.request(
        method=method,
        url=url,
        json=json
    )

    return mock_request


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
    mock_api_request: requests_mock.mocker
) -> None:
    """ Test the ClimateData.convert_date_string method.

            Args:
                date_input (List):
                    Mock date string input values.

                date_output (List):
                    Mock expected datetime.datetime return values.

                mock_api_request (requests_mock.mocker):
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
    mock_api_request_date_error: requests_mock.mocker
) -> None:
    """ Test the ClimateData.convert_date_string method.

        Includes an invalid date string, to test the ValueError
        exception handling.

            Args:
                mock_api_request_date_error (requests_mock.mocker):
                    Mock HTTP request and response fixture that
                    includes an invalid date string.

            Returns:
                None.
        """

    # Use pytest.raises to define the expected exception
    with raises(
        expected_exception=ValueError
    ):
        # Call the mock_api_request_date_error fixture
        mock_api_request_date_error

        # Create an instance of the ClimateData.ClimateData class
        ClimateData()

    return None


def test_get_atmospheric_co2_data(
    mock_api_request: requests_mock.mocker
) -> None:
    """ Test the ClimateData._get_atmospheric_co2_data method.

            Args:
                mock_api_request (requests_mock.mocker):
                    Mock HTTP request and response fixture.

            Returns:
                None.
        """

    # Call the mock_api_request fixture
    mock_api_request

    # Create an instance of the ClimateData.ClimateData class
    cd = ClimateData()

    # Call the _get_atmospheric_co2_data method
    mock_response = cd._get_atmospheric_co2_data()

    assert mock_response == MOCK_RAW_CO2_LIST

    return None


def test_transpose_data_for_graphing() -> None:
    """ Test the ClimateData.transpose_data_for_graphing method.

            Args:
                None.

            Returns:
                None.
        """

    # TODO

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
