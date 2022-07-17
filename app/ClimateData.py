#!/usr/bin/env python3
""" ClimateData class and methods. """

# Imports - Python Standard Library
from datetime import datetime
from typing import Dict

# Imports - Third-Party
from requests import get
from requests.exceptions import HTTPError

# Imports - Local

# Constants
ATMOSPHERIC_CO2_URL = (
    'https://services9.arcgis.com'
    '/weJ1QsnbMYJlCHdG/arcgis/rest/services'
    '/Indicator_3_2_Climate_Indicators'
    '_Monthly_Atmospheric_Carbon_Dioxide_concentrations'
    '/FeatureServer/0/query?'
    'where=1%3D1&outFields=Indicator,Code,Unit,Date,Value&'
    'outSR=4326&f=json'
)
SRTPTIME_FORMAT = '%YM%m'


class ClimateData:
    """ Climate Data class object. """

    def __init__(self) -> None:
        """ ClimateData initialization method.

            Args:
                None.

            Returns:
                None.
        """

        # Retrieve atmospheric Co2 levels data
        self.atmospheric_co2_data = self._get_atmospheric_co2_data()

        return None

    def _convert_date_string(
        self,
        date_str: str,
        strptime_format: str = SRTPTIME_FORMAT
    ) -> datetime:
        """ Convert date string to a datetime.datetime object.

            Args:
                date_str (str):
                    Date string to convert to a datetime.datetime
                    object.

                strptime_format (str, optional):
                    Datetime format code string that matches the
                    date_str object.  Default is STRPTIME_FORMAT.  See:
                    https://docs.python.org/3/library/datetime.html
                    #strftime-and-strptime-format-codes

            Returns:
                date_obj (datetime.datetime):
                    datetime.datetime object resulting from the
                    converted date_str value.
        """

        # Convert date_str to a datetime.datetime object
        date_obj = datetime.strptime(
            date_str,
            strptime_format
        )

        return date_obj

    def _get_atmospheric_co2_data(self) -> Dict:
        """ Retrieve atmospheric Co2 levels data.

            Creates the self.atmospheric_co2_data attribute that contains
            Python-formatted atmospheric CO2 data.

            Args:
                None.

            Returns:
                atmospheric_co2_data (Dict):
                    Formatted Dict of atmospheric Co2 data.
        """

        try:
            # Attempt to retrieve atmospheric Co2 data
            raw_data = get(
                url=ATMOSPHERIC_CO2_URL,
                timeout=5
            )

            if raw_data.ok is True:
                # Set the self._raw_data variable to the Response object
                self._raw_data = raw_data

                # Get the data in the atmospheric_co2_data 'features' key
                atmospheric_co2_data = raw_data.json().get('features', None)

                # convert the dates in _atmospheric_co2_data to datetime objs
                for record in atmospheric_co2_data:
                    record['attributes']['Date'] = self._convert_date_string(
                        date_str=record['attributes']['Date']
                    )

            else:
                # TODO
                pass

        except HTTPError as e:
            # Handle HTTPError exceptions
            print(f'\n{e!r}\n')

            # Raise the exception
            raise

        return atmospheric_co2_data

    def plot_atmospheric_co2_data(
        self,
        atmospheric_co2_data: Dict
    ) -> None:
        """ Display atmospheric Co2 Data.

            Renders the self.atmospheric_co2_data in a graph.

            Args:
                atmospheric_co2_data (Dict):
                    Formatted Dict of atmospheric Co2 data.


            Returns:
                None.
        """

        return None
