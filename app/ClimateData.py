#!/usr/bin/env python3
""" ClimateData class and methods. """

# Imports - Python Standard Library
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


class ClimateData:
    """ Climate Data class object. """

    def __init__(self) -> None:
        """ ClimateData initialization method:

            Args:
                None.

            Returns:
                None.
        """

        # Retrieve atmospheric Co2 levels data
        self.atmospheric_co2_data = self.get_atmospheric_co2_data()

        return None

    def get_atmospheric_co2_data(self) -> Dict:
        """ Retrieve atmospheric Co2 levels data:

            Creates the self.atmospheric_co2_data attribute that contains
            Python-formatted atmospheric CO2 data.

            Args:
                None.

            Returns:
                atmospheric_co2_data (Dict):
                    Formatted Dict of atmospheric Co2 data
        """

        try:
            # Attempt to retrieve atmospheric Co2 data
            raw_data = get(
                url=ATMOSPHERIC_CO2_URL,
                timeout=5
            )

            if raw_data.ok is True:
                # Get the data in the atmospheric_co2_data 'features' key
                atmospheric_co2_data = raw_data.json().get('features', None)

            else:
                # TODO
                pass

        except HTTPError as e:
            # Handle HTTPError exceptions
            print(f'{e!r}')

            # Raise the exception
            raise

        return atmospheric_co2_data
