#!/usr/bin/env pytest
""" Unit tests for climate_data.py. """

# Imports - Python Standard Library
from datetime import datetime
from json import loads
from pathlib import PosixPath
from typing import Callable
from unittest.mock import mock_open, patch
import builtins

# Imports - Third-Party
from _pytest.capture import CaptureFixture
from pytest import fixture
import requests_mock
import requests_mock.mocker

# Imports - Local
from app.climate_data import (
    main, plot_graph, PPM_BAR_PLOT_PROPERTIES
)
from app.ClimateData import (
     ATMOSPHERIC_CO2_URL, ClimateData, TransposedData
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


@fixture
def mock_climate_data_main(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> ClimateData:
    """ Mock climate_data object returned by climate_data.main.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            climate_data (ClimateData):
                Mock instance of the ClimateData.ClimateData class
                returned by the climate_data.main function.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Call the main function
    climate_data = main()

    return climate_data


def test_main(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    mock_climate_data_main: Callable
) -> None:
    """ Test the climate_data.main function.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

            mock_climate_data_main (Callable):
                pytest fixture that creates a mock instance of the
                ClimateData.ClimateData class returned by the
                climate_data.main function.

        Return:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Call the main function
    mock_response = mock_climate_data_main

    assert mock_response._raw_data.json() == loads(MOCK_RAW_CO2_JSON)

    return None


def test_plot_graph(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    mock_climate_data_main: Callable,
    capsys: CaptureFixture
) -> None:
    """ Test the climate_data.plot_graph function.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

            mock_climate_data_main (Callable):
                pytest fixture that creates a mock instance of the
                ClimateData.ClimateData class returned by the
                climate_data.main function.

            capsys (_pytest.capture.CaptureFixture):
                pytest fixture to capture STDOUT data.

        Return:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Add transposed data to the plot_properties dict
    plot_properties = PPM_BAR_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            transposed_data=MOCK_CO2_PPM_GRAPH_DATA
        )
    )

    # Create a mock file open object
    # When called, prevents plot_graph from writing a new file
    mock_file = mock_open()

    # Perform a mock write to the mock file
    with patch.object(
        target=builtins,
        attribute='open',
        new=mock_file
    ):

        # Call the plot_graph function
        mock_response = plot_graph(
            plot_properties=PPM_BAR_PLOT_PROPERTIES,
            climate_data=mock_climate_data_main
        )

    # Assign STDOUT data to a variable
    std_out = capsys.readouterr().out

    # Confirm the mock_file object was called once
    assert mock_file.assert_called_once

    # Confirm the _plot_graph returns True or False
    assert isinstance(mock_response, bool)

    # Confirm expected STDOUT content is present
    assert PPM_BAR_PLOT_PROPERTIES.get('title', None) in std_out
