#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
from datetime import datetime

# Imports - Third-Party
from pytest import mark

# Imports - Local
from app.ClimateData import ClimateData

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


def test_get_atmospheric_co2_data() -> None:
    """ Test the ClimateData._get_atmospheric_co2_data method.

            Args:
                None.

            Returns:
                None.
        """

    # TODO

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
