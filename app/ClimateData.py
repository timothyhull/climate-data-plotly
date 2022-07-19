#!/usr/bin/env python3
""" ClimateData class and methods. """

# Imports - Python Standard Library
from datetime import datetime
from typing import Dict, List, Tuple, Union

# Imports - Third-Party
from plotly.offline import init_notebook_mode
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
PPM_UNIT = 'Parts Per Million'
PPM_YOY_UNIT = 'Percent'


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

        # Extract atmospheric Co2 PPM and matching data data
        self.co2_ppm_date_data = self._get_co2_ppm_date_data()

        # Extract atmospheric Co2 YoY % change and matching data data
        self.co2_yoy_change_data = self._get_co2_yoy_change_data()

        # Initialize Plotly in offline mode
        # Reference: https://plot.ly/python/getting-started
        self._init_plotly_offline_mode()

        return None

    def _init_plotly_offline_mode(self) -> None:
        """ Initialize Plotly in offline mode.

            Use plotly.offline.init_notebook_mode to initialize Plotly
            in offline mode.

            Args:
                None.

            Returns:
                None.
        """

        # Initialize Plotly
        init_notebook_mode(
            connected=True
        )

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

            Creates the self.atmospheric_co2_data attribute that
            contains Python-formatted atmospheric CO2 data.

            Args:
                None.

            Returns:
                atmospheric_co2_data (Dict):
                    Formatted dictionary of atmospheric Co2 data.
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

    def _get_co2_ppm_date_data(self) -> Dict:
        """ Extract atmospheric Co2 ppm levels with dates.

            Create a dictionary from data self.atmospheric_co2_data
            that only contains parts per million (PPM) and
            dates of measurement.

            Args:
                None.

            Returns:
                co2_ppm_date_data (Dict):
                    Dictionary of atmospheric Co2 PPM and data data.
        """

        # Create a dictionary comprehension of PPM and dates of measurement
        co2_ppm_date_data = {
            data['attributes']['Date']: data['attributes']['Value']
            for data in self.atmospheric_co2_data
            if data['attributes']['Unit'] == PPM_UNIT
        }

        return co2_ppm_date_data

    def _get_co2_yoy_change_data(self) -> Dict:
        """ Extract atmospheric Co2 ppm YoY changes with dates.

            Create a dictionary from data self.atmospheric_co2_data
            that only contains year over year (YoY) percentage changes
            and dates of measurement.

            Args:
                None.

            Returns:
                co2_yoy_change_data (Dict):
                    Dictionary of atmospheric Co2 YoY changes and
                    data data.
        """

        # Create a dictionary comprehension of YoY % changes with dates
        co2_yoy_change_data = {
            data['attributes']['Date']: data['attributes']['Value']
            for data in self.atmospheric_co2_data
            if data['attributes']['Unit'] == PPM_YOY_UNIT
        }

        return co2_yoy_change_data

    def transpose_data_for_graphing(
        self,
        data: Union[Dict, List[Tuple]]
    ) -> List[Tuple]:
        """ Transpose data for graphing.

            Transpose data set values to X and Y-axis coordinates.

                Args:
                    data (dict or List[Tuple]):
                        Data to be transposed.  Can be a dictionary or
                        one or more lists of tuples.

                Returns:
                    transposed_data (List[Tuple, Tuple]):

            """

        # Create a list of tuples from the data argument value
        transposed_data = list(
            zip(
                # Unpack data.items into two iterables for the zip function
                *data.items()
            )
        )

        return transposed_data

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

        # TODO

        return None
