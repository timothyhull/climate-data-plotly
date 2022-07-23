#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
from datetime import datetime
from json import loads

# Imports - Third-Party
from pytest import mark
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
MOCK_RAW_CO2_DICT = {
    'features': [
        {
            'attributes': {
                'Indicator': 'Monthly Atmospheric Co2 Concentrations',
                'Code': 'ECNCIC_PPM',
                'Unit': 'Parts Per Million',
                'Date': '1958M03',
                'Value': 315.7
            }
        },
        {
            'attributes': {
                'Indicator': 'Monthly Atmospheric Co2 Concentrations',
                'Code': 'ECNCIC_PPM',
                'Unit': 'Parts Per Million',
                'Date': '1958M04',
                'Value': 317.45
            }
        },
        {
            'attributes': {
                'Indicator': 'Monthly Atmospheric Co2 Concentrations',
                'Code': 'ECNCIC_PPM',
                'Unit': 'Parts Per Million',
                'Date': '1958M05',
                'Value': 317.51
            }
        }
    ]
}


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
    date_input, date_output
) -> None:
    """ Test the ClimateData.convert_date_string method.

            Args:
                None.

            Returns:
                None.
        """

    # Assert that _convert_date_string returns the expected values
    assert ClimateData._convert_date_string(
        self=ClimateData,
        date_str=date_input
    ) == date_output

    return None


def test_get_atmospheric_co2_data(
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the ClimateData._get_atmospheric_co2_data method.

            Args:
                None.

            Returns:
                None.
        """

    # Setup mock request arguments
    method = DEFAULT_MOCK_METHOD
    url = ATMOSPHERIC_CO2_URL
    json = loads(MOCK_RAW_CO2_JSON)

    # Create the mock request
    requests_mock.request(
        method=method,
        url=url,
        json=json
    )

    # Call the _get_atmospheric_co2_data method
    mock_response = ClimateData._get_atmospheric_co2_data(
        self=ClimateData
    )

    # Extract data from the 'features' key
    mock_response = mock_response.json().get('features', None)

    assert mock_response == MOCK_RAW_CO2_DICT

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
