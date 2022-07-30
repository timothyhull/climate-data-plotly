#!/usr/bin/env python3
""" ClimateData class and methods. """

# Imports - Python Standard Library
from collections import namedtuple
from datetime import datetime
from os import path
from pathlib import Path
from typing import Dict, List, Tuple, Union

# Imports - Third-Party
from plotly.offline import init_notebook_mode
from requests import get
from requests.exceptions import HTTPError
import plotly.express as px

# Imports - Local

# namedtuple objects:
TransposedData = namedtuple(
    typename='TransposedData',
    field_names=[
        'dates',
        'values'
    ]
)

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
PLOT_FILE_EXTENSION = 'html'
PLOT_FILE_DEFAULT_NAME = 'test_plot'
PLOT_FILE_DEFAULT_HTML = (
    '''
    <html>
        <head>
            <title>No Plot Content</title>
        </head>
        <body>
            <h1>This plot file contains no content.</h1>
            <h2>The 'file_content' parameter accepts HTML content</h2>
        </body>
    </html>
    '''
).strip()
PLOT_FILE_PATH = 'plot_files'
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

        try:
            # Attempt to convert date_str to a datetime.datetime object
            date_obj = datetime.strptime(
                date_str,
                strptime_format
            )

        except ValueError as e:
            # Handle ValueError exceptions
            print(f'\n{e!r}\n')

            # Raise the exception
            raise

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
                raw_data.raise_for_status()

        except HTTPError as e:
            # Handle HTTPError exceptions
            print(f'\n{e!r}\n')

            # Raise the exception
            raise

        return atmospheric_co2_data

    def _get_co2_ppm_date_data(
        self,
        atmospheric_co2_data: List[Dict] = None
    ) -> Dict:
        """ Extract atmospheric Co2 ppm levels with dates.

            Create a dictionary from data in self.atmospheric_co2_data
            that only contains parts per million (PPM) and
            dates of measurement.

            Args:
                atmospheric_co2_data (List[Dict]):
                    List of dictionaries in the format:

                        'attributes': {
                            'Indicator': 'Monthly Atmospheric...s',
                            'Code': 'ECNCIC_PPM',
                            'Unit': 'Parts Per Million',
                            'Date': datetime(1958, 4, 1, 0, 0),
                            'Value': 317.45

                    Default is None.

            Returns:
                co2_ppm_date_data (Dict):
                    Dictionary of atmospheric Co2 PPM and data data.
        """

        # Uses self.atmospheric_co2_data as a data source by default
        if not isinstance(atmospheric_co2_data, list):
            atmospheric_co2_data = self.atmospheric_co2_data

        # Create a dictionary comprehension of PPM and dates of measurement
        co2_ppm_date_data = {
            data['attributes']['Date']: data['attributes']['Value']
            for data in atmospheric_co2_data
            if data['attributes']['Unit'] == PPM_UNIT
        }

        return co2_ppm_date_data

    def _get_co2_yoy_change_data(
        self,
        atmospheric_co2_data: List[Dict] = None
    ) -> Dict:
        """ Extract atmospheric Co2 ppm YoY changes with dates.

            Create a dictionary from data in self.atmospheric_co2_data
            that only contains year over year (YoY) percentage changes
            and dates of measurement.

            Args:
                atmospheric_co2_data (List[Dict]):
                    List of dictionaries in the format:

                        'attributes': {
                            'Indicator': 'Monthly Atmospheric...s',
                            'Code': 'ECNCIC_PPM',
                            'Unit': 'Parts Per Million',
                            'Date': datetime(1958, 4, 1, 0, 0),
                            'Value': 317.45

                    Default is None.

            Returns:
                co2_yoy_change_data (Dict):
                    Dictionary of atmospheric Co2 YoY changes and
                    data data.
        """

        # Uses self.atmospheric_co2_data as a data source by default
        if not isinstance(atmospheric_co2_data, list):
            atmospheric_co2_data = self.atmospheric_co2_data

        # Create a dictionary comprehension of YoY % changes with dates
        co2_yoy_change_data = {
            data['attributes']['Date']: data['attributes']['Value']
            for data in atmospheric_co2_data
            if data['attributes']['Unit'] == PPM_YOY_UNIT
        }

        return co2_yoy_change_data

    def transpose_data_for_graphing(
        self,
        data: Union[Dict, Union[List[Tuple], Tuple[Tuple]]]
    ) -> TransposedData[Tuple[datetime], Tuple[float]]:
        """ Transpose data for graphing.

            Transpose data set values to X and Y-axis coordinates.

                Args:
                    data (Dict or List[Tuple]):
                        Data to be transposed.  Can be a dictionary or
                        one or more lists of tuples.

                Returns:
                    transposed_data (
                        Union[Dict, Union[List[Tuple], Tuple[Tuple]]]
                    ):
                        - transposed_data.dates = Tuple of
                          datetime.datetime objects.

                        - transposed_data.values: Tuple of float
                          objects.

        """

        # Determine if the object class for 'data' is list or dictionary
        if isinstance(data, list):
            # Convert a list of two dictionaries to a dict using a zip function
            d = zip(
                data[0],
                data[1]
            )
            data = dict(d)

        # Convert a list of two dictionaries to a TransposedData object
        # Create a TransposedData namedtuple object
        transposed_data = TransposedData(
            dates=tuple(data.keys()),
            values=tuple(data.values())
        )

        return transposed_data

    def plot_atmospheric_co2_data(
        self,
        transposed_data: TransposedData[Tuple[datetime], Tuple[float]]
    ) -> str:
        """ Display atmospheric Co2 Data using Plotly Express.

            Renders the self.atmospheric_co2_data in a graph.

            Args:
                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axises
                    respectively.

            Returns:
                line_graph_html (str):
                    HTML content for a line graph file.
        """

        # Create a line graph
        line_graph = px.line(
            data_frame=dict(
                dates=transposed_data.dates,
                values=transposed_data.values
            ),
            labels=dict(
                dates='Date',
                values='Atmospheric Co2 PPM'
            ),
            markers=True,
            title='Atmospheric Co2 Levels',
            x='dates',
            y='values'
        )

        # Create HTML content for a plot file
        line_graph_html = line_graph.to_html()

        return line_graph_html

    def write_plot_html_file(
        self,
        file_name: str = PLOT_FILE_DEFAULT_NAME,
        file_content: str = PLOT_FILE_DEFAULT_HTML
    ) -> None:
        """ Write a plot file to HTML on local storage.

            Args:
                file_name (str, optional):
                    Name of the plot file to write.  The '.html' file
                    extension will append the file_name value.  Default
                    value is PLOT_FILE_DEFAULT_NAME.

                file_content (str, optional):
                    File contents to write to the HTML file. Default
                    value is PLOT_FILE_DEFAULT_HTML.

            Returns:
                None
        """

        # Determine the local path to the plot file directory
        current_file = path.abspath(__file__)
        current_dir = Path(current_file).parent
        plot_dir = path.join(current_dir, PLOT_FILE_PATH)
        plot_file = path.join(plot_dir, f'{file_name}.{PLOT_FILE_EXTENSION}',)

        # Create a file storage directory with a context manager
        with Path(plot_dir) as pd:
            pd.mkdir(
                exist_ok=True
            )

        # Write a file with a context manager
        with open(
            file=plot_file,
            mode='w',
            encoding='utf=8'
        ) as file:

            file.write(file_content)

        return None
