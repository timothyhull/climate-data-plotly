#!/usr/bin/env pytest
""" Unit tests for climate_data.py. """

# Imports - Python Standard Library
from json import loads
from pathlib import PosixPath
from typing import Callable

# Imports - Third-Party
from pytest import fixture
import requests_mock
import requests_mock.mocker

# Imports - Local
from app.climate_data import main
from app.ClimateData import (
     ATMOSPHERIC_CO2_URL,  # ClimateData
)

# Constants
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

        # Create the mock request
        mock_request = requests_mock.request(
            method=method,
            url=url,
            json=json,
            status_code=status_code
        )

        return mock_request

    return _mock_api_request


def test_main(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the climate_data.main function.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Return:
            None.
    """

    mock_api_request(
        requests_mock=requests_mock
    )

    mock_response = main()

    assert mock_response._raw_data.json() == loads(MOCK_RAW_CO2_JSON)

    return None
