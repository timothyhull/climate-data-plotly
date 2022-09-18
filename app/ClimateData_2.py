#!/usr/bin/env python3
""" ClimateData abstract factory testing only. """

# Imports - Python Standard Library
from abc import ABC, abstractmethod
from datetime import datetime
from os import environ, path
from pathlib import Path
from typing import Callable, Dict, List, NamedTuple, Tuple, Union

# Imports - Third-Party
from plotly.offline import init_notebook_mode
from requests import get
from requests.exceptions import HTTPError
from plotly.graph_objs._figure import Figure
import plotly.express as px
import plotly.graph_objects as go

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
DIR_CREATE_ERROR_MSG = '** Unable to create a directory for file storage **'
FILE_WRITE_ERROR_MSG = '** Unable to write file to disk **'
GO_LINE_GRAPH_MODE = 'lines+markers'
PLOT_DATE_LABEL = 'Dates'
PLOT_VALUE_LABEL = 'Values'
PLOT_TITLE = 'Atmospheric Co2 Data'
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
PLOT_RANGE_SELECTOR = {
    'buttons': [
        dict(count=1, label='1m', step='month', stepmode='backward'),
        dict(count=6, label='6m', step='month', stepmode='backward'),
        dict(count=1, label='YTD', step='year', stepmode='todate'),
        dict(count=1, label='1y', step='year', stepmode='backward'),
        dict(count=5, label='5y', step='year', stepmode='backward'),
        dict(count=10, label='10y', step='year', stepmode='backward'),
        dict(count=25, label='25y', step='year', stepmode='backward'),
        dict(step='all')
    ]
}
PPM_UNIT = 'Parts Per Million'
PPM_YOY_UNIT = 'Percent'
PYTEST_ENV_VAR = 'PYTEST_CURRENT_TEST'
PYTEST_WRITE_PLOT_HTML_DIR_FUNC = 'test_write_plot_html_dir_error'
PYTEST_WRITE_PLOT_HTML_FILE_FUNC = 'test_write_plot_html_file_error'
SRTPTIME_FORMAT = '%YM%m'


# NamedTuple objects
class PlotProperties(NamedTuple):
    """ Properties for formatting a graphed plot.

        Typed version of the collections.namedtuple object with
        field names, type hints, and default values.

        Field names, type hints, and default values:

            line_graph (bool, optional):
                Specifies whether the plot will be a line graph
                or not.  When True, the plot will be a line graph.
                When False, the plot will be a bar graph.  Default
                is True.

            date_label (str, optional):
                Label of plot y-axis.  Default is PLOT_DATE_LABEL.

            value_label (str, optional):
                Label of plot y-axis.  Default is PLOT_VALUE_LABEL.

            title (str, optional):
                Title of plot. Default is PLOT_TITLE.

            compress_y_axis (str, optional):
                Determine whether the y-axis starts at 0, which
                displays well with PPM data although poorly with
                YOY data.  When True, compresses the y-axis range
                to 95% of the first value of the y-axis data,
                and 100.5% of the last value in the y-axis data.
                Default is False.

            file_name (str, optional):
                Name of an HTML file to create with plot results,
                without the .html suffix.
                Default is PLOT_FILE_DEFAULT_NAME,

            px_plot (bool, optional):
                Specifies the type of plot for Plotly to render.
                True renders the plot with plotly.express.
                False renders the plot with plotly.graph_objects.
                Default is False.
    """

    # Field names and default values
    line_graph: bool = True,
    date_label: str = PLOT_DATE_LABEL,
    value_label: str = PLOT_VALUE_LABEL,
    title: str = PLOT_TITLE,
    compress_y_axis: bool = False,
    file_name: str = PLOT_FILE_DEFAULT_NAME,
    px_plot: bool = False


class TransposedData(NamedTuple):
    """ Object to store data transposed plot data.

        Typed version of the collections.namedtuple object with
        field names and type hints.

            dates (datetime.datetime):
                Date values for the X axis.

            values (float)
                Numeric values for the Y axis.
    """

    # Field names and type hints:
    dates: datetime
    values: float


# Abstract factory class
class ClimateData(ABC):
    """ Abstract factory class for all climate data classes. """

    # Abstract factory methods
    @abstractmethod
    def create_climate_data_plot(self) -> None:
        """ Create an HTML plot with climate data. """
        pass


# Abstract product classes
class PXPlot(ABC):
    """ Abstract product class for Plotly Express plots. """

    # Abstract product methods
    @abstractmethod
    def px_plot(self) -> None:
        """ Create an HTML plot with climate data. """


# Concrete factory classes
class ClimatePlot(ClimateData):
    """ Concrete factory class for climate data classes. """

    # Concrete factory functions, from the ClimateData class
    def create_climate_data_plot(self) -> Callable:
        # Return an instance of the AtmosphericCo2PPMPlot class
        return AtmosphericCo2PPMPlot()


# Concrete product classes
class AtmosphericCo2PPMPlot(ClimatePlot):
    """ Atmospheric Co2 PPM class object. """

    def __init__(self) -> None:
        """ AtmosphericCo2PPM initialization method.

            Args:
                None.

            Returns:
                None.
        """

        # Retrieve atmospheric Co2 levels data
        self.atmospheric_co2_data = self._get_api_data()

        # Extract atmospheric Co2 PPM per month and matching date data
        self.co2_ppm_date_data = self._get_co2_ppm_date_data()

        # Transpose self.co2_ppm_date_data to graph input data
        self.transposed_co2_ppm_date_data = self.transpose_data_for_graphing(
            data=self.co2_ppm_date_data
        )

        # Extract atmospheric Co2 YoY % change and matching data data
        self.co2_yoy_change_data = self._get_co2_yoy_change_data()

        # Transpose self.co2_yoy_change_data to graph input data
        self.transposed_co2_yoy_change_data = self.transpose_data_for_graphing(
            data=self.co2_yoy_change_data
        )

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

    def _get_api_data(self) -> Dict:
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

    def _setup_graph_args_px(
        self,
        plot_properties: PlotProperties,
        transposed_data: TransposedData[Tuple[datetime], Tuple[float]]
    ) -> dict:

        """ Prepare a dictionary of graph arguments.

            This method supports Plotly Express plots.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axes
                    respectively.

            Returns:
                graph_args (dict):
                    Dictionary of arguments to pass to a plotting
                    function.
        """

        # Set default range values for the x and y-axes
        range_x = [
            transposed_data.dates[0],
            transposed_data.dates[-1]
        ]

        # Create a dictionary of arguments for the graph object
        graph_args = dict(
            data_frame=dict(
                dates=transposed_data.dates,
                values=transposed_data.values
            ),
            labels=dict(
                x=plot_properties.date_label,
                y=plot_properties.value_label
            ),
            range_x=range_x,
            title=plot_properties.title,
            x=transposed_data.dates,
            y=transposed_data.values
        )

        return graph_args

    def _setup_graph_args_go(
        self,
        plot_properties: PlotProperties,
        transposed_data: TransposedData[Tuple[datetime], Tuple[float]]
    ) -> dict:

        """ Prepare a dictionary of graph arguments.

            This method supports Plotly Graph Objects plots.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axes
                    respectively.

            Returns:
                graph_args (dict):
                    Dictionary of arguments to pass to a plotting
                    function.
        """

        # Create a dictionary of arguments for the graph object
        graph_args = dict(
            mode=GO_LINE_GRAPH_MODE,
            name=plot_properties.value_label,
            x=transposed_data.dates,
            y=transposed_data.values
        )

        return graph_args

    def _setup_layout_args(
        self,
        plot_properties: PlotProperties,
    ) -> dict:
        """ Prepare a dictionary of graph layout arguments.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

            Returns:
                layout_args (dict):
                    Dictionary of arguments to pass to a plotting
                    function.
        """

        # Create a dictionary of arguments for graph layout options
        layout_args = dict(
            showlegend=True,
            title=plot_properties.title,
            xaxis_title=plot_properties.date_label,
            yaxis_title=plot_properties.value_label
        )

        return layout_args

    def _update_graph_x_axis(
        self,
        graph: Figure,
        range_x: List
    ) -> Figure:

        """ Modify default properties of the x-axis.

            Args:
                graph (plotly.graph_objs._figure.Figure):
                    Plotly graph Figure object.

                range_x (List):
                    List of starting and end values for the x-axis.

            Returns:
                graph (plotly.graph_objs._figure.Figure):
                    Modified Plotly graph Figure object.
        """

        # x-axis modifiers
        graph.update_xaxes(
            # Add a slider to pan and zoom the x-axis
            rangeslider_visible=True,
            rangeselector=PLOT_RANGE_SELECTOR,
            rangeslider_range=range_x
        )

        return graph

    def _update_graph_y_axis(
        self,
        graph: Figure,
        range: List
    ) -> Figure:

        """ Modify default properties of the y-axis.
            Args:
                graph (plotly.graph_objs._figure.Figure):
                    Plotly graph Figure object.
                range (List):
                    List of starting and end values for the y-axis.
            Returns:
                graph (plotly.graph_objs._figure.Figure):
                    Modified Plotly graph Figure object.
        """

        # y-axis modifiers
        graph.update_yaxes(
            # Set a dynamic axis numeric range
            **range,

            # Format the zero line
            zeroline=True,
            zerolinecolor='#F00',
            zerolinewidth=2
        )

        return graph

    def _compress_y_axis(
        self,
        transposed_data_values: Tuple[float],
    ) -> dict:

        """ Compress the range of the y_axis to simplify plot view.

            Args:
                transposed_data_values (Tuple[float]):
                    Y-axis data to compress.

            Returns:
                range (dict):
                    dict with a single List value of compressed range
                    values. Based on the first and last indices in
                    transposed_data_values.
        """

        # Set a new, compressed y_axis range
        range = dict(
                range=[
                    transposed_data_values[0] * .95,
                    transposed_data_values[-1] * 1.05,
                ]
            )

        return range

    def _plot_px(
        self,
        plot_properties: PlotProperties,
        graph_args: dict
    ) -> Figure:

        """ Create a graph with plotly.express.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                graph_args(dict):
                    Dictionary of graph arguments.

            Returns:
                Tuple of two values for use with multiple variable
                assignment by the calling function:

                    graph (plotly.graph_objs._figure.Figure):
                        Modified Plotly graph Figure object.
        """

        # Create a line graph with plotly.express
        if plot_properties.line_graph is True:
            graph = px.line(
                **graph_args,
                markers=True
            )

        # Create a bar graph with plotly.express
        else:
            graph = px.bar(**graph_args)

        return graph

    def _plot_go(
        self,
        plot_properties: PlotProperties,
        graph_args: dict
    ) -> Figure:

        """ Create a graph with plotly.graph_objects.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                graph_args(dict):
                    Dictionary of graph arguments.

            Returns:
                Tuple of two values for use with multiple variable
                assignment by the calling function:

                    graph (plotly.graph_objs._figure.Figure):
                        Modified Plotly graph Figure object.
        """

        # Create a go.Figure object
        graph = go.Figure()

        # Create a line graph with plotly.graph_objects
        if plot_properties.line_graph is True:

            # Add a line trace to the figure object
            graph.add_trace(
                go.Scatter(**graph_args)
            )

        # Create a bar graph with plotly.graph_objects
        else:
            # Remove the mode key from graph_args
            del graph_args['mode']

            # Add a line trace to the figure object
            graph.add_trace(
                go.Bar(**graph_args)
            )

        return graph

    def _create_graph_px(
        self,
        plot_properties: PlotProperties,
        transposed_data: TransposedData
    ) -> Tuple[Figure, dict]:

        """ Create a graph with plotly.express.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axes
                    respectively.

            Returns:
                Tuple of two values for use with multiple variable
                assignment by the calling function:

                    graph (plotly.graph_objs._figure.Figure):
                        Modified Plotly graph Figure object.

                    graph_args (dict):
                        Dictionary of graph arguments.
        """

        # Setup arguments to use in a graph/plot function
        graph_args = self._setup_graph_args_px(
            plot_properties=plot_properties,
            transposed_data=transposed_data
        )

        # Create the Plotly Express plot
        graph = self._plot_px(
            plot_properties=plot_properties,
            graph_args=graph_args
        )

        return graph, graph_args

    def _create_graph_go(
        self,
        plot_properties: PlotProperties,
        transposed_data: TransposedData
    ) -> Tuple[Figure, dict]:

        """ Create a graph with plotly.graph_objects.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axes
                    respectively.

            Returns:
                Tuple of two values for use with multiple variable
                assignment by the calling function:

                    graph (plotly.graph_objs._figure.Figure):
                        Modified Plotly graph Figure object.

                    graph_args (dict):
                        Dictionary of graph arguments.
        """

        # Setup arguments to use in a graph/plot function
        graph_args = self._setup_graph_args_go(
            plot_properties=plot_properties,
            transposed_data=transposed_data
        )

        # Setup layout arguments to use in a graph/plot function
        layout_args = self._setup_layout_args(
            plot_properties=plot_properties
        )

        graph = self._plot_go(
            plot_properties=plot_properties,
            graph_args=graph_args
        )

        # Update the graph layout
        graph.update_layout(**layout_args)

        return graph, graph_args

    def _set_plot_file_path(
        self,
        file_name: str = PLOT_FILE_DEFAULT_NAME
    ) -> tuple[str, str]:
        """ Create the file path for the plot output file.

            Args:
                file_name (str, optional):
                    Name of the plot file to write.  The '.html' file
                    extension will append the file_name value.  Default
                    value is PLOT_FILE_DEFAULT_NAME.

            Returns:
                plot_abs_path (str):
                    Absolute path for the plot output file.
        """

        # Get the absolute path to the file running this code
        current_file = path.abspath(__file__)

        # Extract the parent directory from current_file
        current_dir = Path(current_file).parent

        # Set a directory path for plot files
        plot_dir = path.join(current_dir, PLOT_FILE_PATH)

        # Set the absolute path for the plot file
        plot_abs_path = path.join(
            plot_dir,
            f'{file_name}.{PLOT_FILE_EXTENSION}'
        )

        return (plot_dir, plot_abs_path)

    def _create_plot_dir(
        self,
        plot_dir: str,
        exist_ok: bool = bool
    ) -> None:
        """ Create the file path for the plot output file.

            Args:
                plot_dir (str):
                    Name of the plot directory to create.

                exist_ok (str, optional):
                    Determines whether or not Path.mkdir may continue
                    when the directory to create already exists.
                    Default is True.

            Returns:
                None.
        """

        # Create a file storage directory with a context manager
        try:
            with Path(plot_dir) as pd:
                pd.mkdir(
                    exist_ok=exist_ok
                )

        except FileExistsError as e:
            # Display an error message
            print(
                f'\n{DIR_CREATE_ERROR_MSG}\n'
                f'\n{e!r}\n'
            )

            # Re-raise the exception
            raise

        return None

    def _create_plot_file(
        self,
        plot_file_path: str,
        file_content: str
    ) -> tuple([str, int]):
        """ Create a plot output file.

            Args:
                plot_file_path (str):
                    Absolute path for the file to create.

                file_content (str, optional):
                    HTML content for the plot file.

            Returns:
                Tuple of plot_file and plot_char_count:
                    plot_file (str):
                        Absolute path for the new file.

                    plot_char_count (int):
                        Integer of the number of characters written to the
                        plot file.
        """

        # Write the file using a context manager
        try:
            with open(
                file=plot_file_path,
                mode='wt',
                encoding='utf=8'
            ) as file:
                plot_char_count = file.write(file_content)

        except FileNotFoundError as e:
            # Display an error message
            print(
                f'\n{FILE_WRITE_ERROR_MSG}\n'
                f'\n{e!r}\n'
            )

            # Re-raise the exception
            raise

        return plot_file_path, plot_char_count

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
        transposed_data = self.TransposedData(
            dates=tuple(data.keys()),
            values=tuple(data.values())
        )

        return transposed_data

    def plot_atmospheric_co2_data(
        self,
        plot_properties: PlotProperties,
        transposed_data: TransposedData[Tuple[datetime], Tuple[float]]
    ) -> str:
        """ Display atmospheric Co2 Data using Plotly.

            Renders the self.atmospheric_co2_data in a graph using
            either plotly.express or plotly.graph_objects methods.

            Args:
                plot_properties (PlotProperties):
                    Instance of the PlotProperties class object,
                    which is an instance of the NamedTuple class,
                    that contains the following properties and
                    default values:

                    line_graph (bool, optional):
                        Specifies whether the plot will be a line
                        graph or not.  When True, the plot will be a
                        line graph. When False, the plot will be a
                        bar graph.  Default is True.

                    date_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_DATE_LABEL.

                    value_label (str, optional):
                        Label of plot y-axis.  Default is
                        PLOT_VALUE_LABEL.

                    title (str, optional):
                        Title of plot. Default is PLOT_TITLE.

                    compress_y_axis (str, optional):
                        Determine whether the y-axis starts at 0, which
                        displays well with PPM data although poorly
                        with YOY data.  When True, compresses the
                        y-axis range to 95% of the first value of the
                        y-axis data, and 100.5% of the last value in
                        the y-axis data. Default is False.

                    file_name (str, optional):
                        Name of an HTML file to create with plot results,
                        without the .html suffix.

                    px_plot (str, optional):
                        Specifies the type of plot for Plotly to render.
                        True renders the plot with plotly.express.
                        False renders the plot with plotly.graph_objects.
                        Default is False.

                transposed_data(
                    TransposedData[Tuple[datetime], Tuple[float]]
                ):
                    TransposedData object with 'dates' and 'values
                    properties with values for the X and Y axes
                    respectively.

            Returns:
                line_graph_html (str):
                    HTML content for a plotly.express graph file.
        """

        # Graph with plotly.express
        if plot_properties.px_plot is True:
            graph, graph_args = self._create_graph_px(
                plot_properties=plot_properties,
                transposed_data=transposed_data
            )

        # Graph with plotly.graph_objects
        else:
            graph, graph_args = self._create_graph_go(
                plot_properties=plot_properties,
                transposed_data=transposed_data
            )

        # Update x-axis properties
        graph = self._update_graph_x_axis(
            graph=graph,
            range_x=graph_args.get('range_x', None)
        )

        # Adjust y-axis range values based on the value of compress_y_axis
        if plot_properties.compress_y_axis is True:
            range = self._compress_y_axis(
                transposed_data_values=transposed_data.values
            )
        else:
            range = dict()

        # Update y-axis properties
        graph = self._update_graph_y_axis(
            graph=graph,
            range=range
        )

        # Create HTML content for a plot file
        graph_html = graph.to_html()

        return graph_html

    def write_plot_html_file(
        self,
        file_name: str = PLOT_FILE_DEFAULT_NAME,
        file_content: str = PLOT_FILE_DEFAULT_HTML
    ) -> int:
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
                Integer of the number of characters written to the
                    plot file.
        """

        # Set a default value for use in the exist_os parameter of os.mkdir
        exist_ok = True

        # Determine if pytest calls the function
        pytest_1 = PYTEST_ENV_VAR in str(environ.keys())
        pytest_2 = PYTEST_WRITE_PLOT_HTML_DIR_FUNC in str(environ.values())
        pytest_3 = PYTEST_WRITE_PLOT_HTML_FILE_FUNC in str(environ.values())

        # pytest calls test_...dir_error, set vars to raise an exception
        if pytest_1 is True and pytest_2 is True:

            # Set plot_dir to a directory that already exists
            # Set plot file to an invalid name
            # Set a variable for use in the exist_os parameter of os.mkdir
            plot_dir, plot_file, exist_ok = ('../', '', False)

        # pytest calls test_...file_error, set vars to raise an exception
        elif pytest_1 is True and pytest_3 is True:

            # Set plot_dir to the current directory
            # Set plot file to an invalid name
            plot_dir, plot_file = ('', '')

        else:
            # Determine the local path to the plot directory and file
            plot_dir, plot_file = self._set_plot_file_path(
                file_name=file_name
            )

        # Create a file storage directory with a context manager
        self._create_plot_dir(
            plot_dir=plot_dir,
            exist_ok=exist_ok
        )

        # Write the file using a context manager
        plot_file_path, plot_char_count = self._create_plot_file(
            plot_file_path=plot_file,
            file_content=file_content
        )

        return plot_file_path, plot_char_count
