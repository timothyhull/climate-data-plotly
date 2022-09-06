#!/usr/bin/env pytest
""" Unit tests for ClimateData.py. """

# Imports - Python Standard Library
from datetime import datetime
from json import loads
from pathlib import Path, PosixPath
from typing import Callable, List
from unittest.mock import MagicMock, mock_open, patch
import builtins

# Imports - Third-Party
from plotly.graph_objs._figure import Figure
from pytest import fixture, mark, raises
from requests.exceptions import HTTPError
import requests_mock
import requests_mock.mocker

# Imports - Local
from app.ClimateData import (
    AtmosphericCo2PPM as APP
)
from app.ClimateData import (
    ATMOSPHERIC_CO2_URL, GO_LINE_GRAPH_MODE,
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
MOCK_RAW_CO2_PPM_LIST = [
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
MOCK_CO2_PPM_DATE_DATA_1 = {
    datetime(1958, 3, 1, 0, 0): 315.7,
    datetime(1958, 4, 1, 0, 0): 317.45,
    datetime(1958, 5, 1, 0, 0): 317.51
}
MOCK_CO2_PPM_DATE_DATA_2 = [
    (
        datetime(1958, 3, 1, 0, 0),
        datetime(1958, 4, 1, 0, 0),
        datetime(1958, 5, 1, 0, 0)
    ),
    (
        315.7,
        317.45,
        317.51
    )
]
MOCK_CO2_PPM_GRAPH_DATA = APP.TransposedData(
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
MOCK_RAW_CO2_YOY_LIST = [
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 3, 1, 0, 0),
            'Value': 0.3
        }
    },
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 4, 1, 0, 0),
            'Value': 0.09
        }
    },
    {
        'attributes': {
            'Indicator': 'Year on Year Percentage Change',
            'Code': 'ECNCIC_YOY',
            'Unit': 'Percent',
            'Date': datetime(1959, 5, 1, 0, 0),
            'Value': 0.25
        }
    }
]
MOCK_CO2_YOY_DATE_DATA_1 = {
    datetime(1959, 3, 1, 0, 0): 0.3,
    datetime(1959, 4, 1, 0, 0): 0.09,
    datetime(1959, 5, 1, 0, 0): 0.25
}
MOCK_CO2_YOY_DATE_DATA_2 = [
    (
        datetime(1959, 3, 1, 0, 0),
        datetime(1959, 4, 1, 0, 0),
        datetime(1959, 5, 1, 0, 0),
    ),
    (
        0.3,
        0.09,
        0.25
    )
]
MOCK_CO2_YOY_GRAPH_DATA = APP.TransposedData(
    dates=(
        datetime(1959, 3, 1, 0, 0),
        datetime(1959, 4, 1, 0, 0),
        datetime(1959, 5, 1, 0, 0),
    ),
    values=(
        0.3,
        0.09,
        0.25
    )
)
MOCK_CO2_GRAPH_INPUT = [
    MOCK_CO2_PPM_DATE_DATA_1,
    MOCK_CO2_PPM_DATE_DATA_2,
    MOCK_CO2_YOY_DATE_DATA_1,
    MOCK_CO2_YOY_DATE_DATA_2,
]
MOCK_CO2_GRAPH_OUTPUT = [
    MOCK_CO2_PPM_GRAPH_DATA,
    MOCK_CO2_PPM_GRAPH_DATA,
    MOCK_CO2_YOY_GRAPH_DATA,
    MOCK_CO2_YOY_GRAPH_DATA
]
MOCK_CO2_GRAPH_DATA = zip(
    MOCK_CO2_GRAPH_INPUT,
    MOCK_CO2_GRAPH_OUTPUT
)
MOCK_HTML_PLOT_PROPERTIES_PX = dict(
    date_label='Dates',
    px_plot=True,
    title='Atmospheric Co2 Levels',
    value_label='Atmospheric Co2 PPM'
)
MOCK_CO2_GRAPH_ARGS = dict(
    data_frame=dict(
        dates=MOCK_CO2_PPM_GRAPH_DATA.dates,
        values=MOCK_CO2_PPM_GRAPH_DATA.values
    ),
    labels=dict(
        x=MOCK_HTML_PLOT_PROPERTIES_PX.get('date_label', None),
        y=MOCK_HTML_PLOT_PROPERTIES_PX.get('value_label', None)
    ),
    range_x=[
        MOCK_CO2_PPM_GRAPH_DATA[0],
        MOCK_CO2_PPM_GRAPH_DATA[-1]
    ],
    title=MOCK_HTML_PLOT_PROPERTIES_PX.get('title', None),
    x=MOCK_CO2_PPM_GRAPH_DATA.dates,
    y=MOCK_CO2_PPM_GRAPH_DATA.values
)
MOCK_HTML_PLOT_SNIPPETS_PX = {
    '<html>': True,
    'window.PlotlyConfig = {MathJaxConfig: \'local\'};</script>': True,
    '* plotly.js v': True,
    f'"{MOCK_HTML_PLOT_PROPERTIES_PX.get("date_label")}=%{{x}}<br>': True,
    f'{MOCK_HTML_PLOT_PROPERTIES_PX.get("value_label")}=%{{y}}<extra>': True,
    f'"title":{{"text":"{MOCK_HTML_PLOT_PROPERTIES_PX.get("title")}"}}': True,
    '</body': True,
    '</html>': True,
    '<title>No Plot Content</title>': False,
    '<h1>This plot file contains no content.</h1>': False,
    '<h2>The \'file_content\' parameter accepts HTML content</h2>': False,
}
MOCK_HTML_PLOT_PROPERTIES_GO = dict(
    date_label='Dates',
    px_plot=False,
    title='Atmospheric YOY % Change Levels',
    value_label='Atmospheric YOY % Change'
)
MOCK_YOY_GRAPH_ARGS = dict(
    mode=GO_LINE_GRAPH_MODE,
    name=MOCK_HTML_PLOT_PROPERTIES_GO.get('value_label', None),
    x=MOCK_CO2_YOY_GRAPH_DATA.dates,
    y=MOCK_CO2_YOY_GRAPH_DATA.values
)
MOCK_HTML_PLOT_SNIPPETS_GO = {
    '<html>': True,
    'window.PlotlyConfig = {MathJaxConfig: \'local\'};</script>': True,
    '* plotly.js v': True,
    f'{{"text":"{MOCK_HTML_PLOT_PROPERTIES_GO.get("date_label")}"}},"ra': True,
    f'"name":"{MOCK_HTML_PLOT_PROPERTIES_GO.get("value_label")}","x":[': True,
    f'":{{"text":"{MOCK_HTML_PLOT_PROPERTIES_GO.get("title")}"}},"xaxis': True,
    '</body': True,
    '</html>': True,
    '<title>No Plot Content</title>': False,
    '<h1>This plot file contains no content.</h1>': False,
    '<h2>The \'file_content\' parameter accepts HTML content</h2>': False,
}
MOCK_HTML_FILE_CONTENT = '''
    <html>
        <head>
            <title>Mock Open HTML Data</title>
        </head>
        <body>
            <h1>Mock Open HTML Data</h1>
        </body>
    </html>
'''.strip()
MOCK_HTML_FILE_NAME = 'test_file.html'


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

        # Check for argument to insert an invalid date string into 'json'
        if date_error is True:
            # Update date value in 'json' with an invalid date string
            json['features'][0]['attributes'].update(
                {'Date': DATE_STR_VALUE_ERROR}
            )

        # Create the mock request
        mock_request = requests_mock.request(
            method=method,
            url=url,
            json=json,
            status_code=status_code
        )

        return mock_request

    return _mock_api_request


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
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.convert_date_string method.

        Args:
            date_input (List):
                Mock date string input values.

            date_output (List):
                Mock expected datetime return values.

            mock_api_request (Callable):
                Mock HTTP request and response fixture.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Assert that _convert_date_string returns the expected values
    assert cd._convert_date_string(
        date_str=date_input
    ) == date_output

    return None


def test_convert_date_string_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the APP.convert_date_string method.

        Includes an invalid date string, to test the ValueError
        exception handling.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

            tmp_path (pathlib.PosixPath):
                pytest fixture to create a temporary directory.
                Used to pass arguments to the mock_api_request
                pytest fixture.

        Returns:
            None.
    """

    # Use pytest.raises to define the expected exception
    with raises(
        expected_exception=ValueError
    ):
        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock,
            date_error=True
        )

        # Instantiate the ClimateData.AtmosphericCo2PPM class
        APP()

    return None


def test_get_api_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
) -> None:
    """ Test the APP._get_api_data method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _get_api_data method
    mock_response = cd._get_api_data()

    assert mock_response == MOCK_RAW_CO2_PPM_LIST + MOCK_RAW_CO2_YOY_LIST

    return None


def test_get_api_data_http_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath,
) -> None:
    """ Test the APP._get_api_data method.

        Determine if the method properly raises an HTTPError with a
        mock bad HTTP status code.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

                tmp_path (pathlib.PosixPath):
                pytest fixture to create a temporary directory.

        Returns:
            None.
    """

    with raises(
        expected_exception=HTTPError
    ):
        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock,
            status_code=400
        )

        # Create an instance of the ClimateData.AtmosphericCo2PPM class
        cd = APP()

        # Call the _get_api_data method
        cd._get_api_data()

    return None


def test_get_co2_ppm_date_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the APP._get_co2_ppm_date_data method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

                tmp_path (pathlib.PosixPath):
                pytest fixture to create a temporary directory.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _get_co2_ppm_date_data method
    mock_response = cd._get_co2_ppm_date_data(
        atmospheric_co2_data=MOCK_RAW_CO2_PPM_LIST
    )

    assert mock_response == MOCK_CO2_PPM_DATE_DATA_1

    return None


def test_get_co2_yoy_change_data(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker,
    tmp_path: PosixPath
) -> None:
    """ Test the APP._get_co2_yoy_change_data method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

                tmp_path (pathlib.PosixPath):
                pytest fixture to create a temporary directory.
        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _get_co2_yoy_change_data method
    mock_response = cd._get_co2_yoy_change_data(
        atmospheric_co2_data=MOCK_RAW_CO2_YOY_LIST
    )

    assert mock_response == MOCK_CO2_YOY_DATE_DATA_1

    return None


def test_compress_y_axis(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP._compress_y_axis method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _compress_y_axis method
    mock_response = cd._compress_y_axis(
        transposed_data_values=MOCK_CO2_PPM_GRAPH_DATA.values
    )

    valid_response = dict(
        range=[
            MOCK_CO2_PPM_GRAPH_DATA.values[0] * .95,
            MOCK_CO2_PPM_GRAPH_DATA.values[-1] * 1.05
        ]
    )

    assert mock_response == valid_response

    return None


def test_plot_px(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP._plot_px method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _plot_px method
    mock_response = cd._plot_px(
        plot_properties=APP.PlotProperties(
            **MOCK_HTML_PLOT_PROPERTIES_PX
        ),
        graph_args=MOCK_CO2_GRAPH_ARGS
    )

    assert isinstance(mock_response, Figure)

    return None


def test_plot_go(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP._plot_go method.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the _plot_px method
    mock_response = cd._plot_go(
        plot_properties=APP.PlotProperties(
            **MOCK_HTML_PLOT_PROPERTIES_GO
        ),
        graph_args=MOCK_YOY_GRAPH_ARGS
    )

    assert isinstance(mock_response, Figure)

    return None


@mark.parametrize(
    argnames=[
        'co2_data',
        'co2_graphing_data'
    ],
    argvalues=list(MOCK_CO2_GRAPH_DATA)
)
def test_transpose_data_for_graphing(
    co2_data: List[List],
    co2_graphing_data: APP.TransposedData,
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.transpose_data_for_graphing method.

        Args:
            co2_data: (List[List]):
                List of lists with mock Co2 data.

            co2_graphing_data (TransposedData):
                TransposedData object with mock Co2 data in a graph-
                compatible format.

            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the transpose_data_for_graphing method
    mock_response = cd.transpose_data_for_graphing(
        data=co2_data
    )

    assert (
        mock_response == co2_graphing_data
    )

    return None


@mark.parametrize(
    argnames=[
        'html_search_string',
        'expected_value'
    ],
    argvalues=list(MOCK_HTML_PLOT_SNIPPETS_PX.items()),
)
def test_plot_atmospheric_co2_data_px(
    html_search_string: List[str],
    expected_value: List[bool],
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.plot_atmospheric_co2_data method.

        Test with plotly.express.

        Args:
            html_search_string (List[str]):
                Mock Plotly HTML file snippets to search for.

            expected_value (List[bool]):
                Mock expected boolean return values.

            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the plot_atmospheric_co2_data_px method
    mock_response = cd.plot_atmospheric_co2_data(
        transposed_data=MOCK_CO2_PPM_GRAPH_DATA,
        plot_properties=APP.PlotProperties(
            **MOCK_HTML_PLOT_PROPERTIES_PX
        )
    )

    assert (html_search_string in mock_response) is expected_value

    return None


@mark.parametrize(
    argnames=[
        'html_search_string',
        'expected_value'
    ],
    argvalues=list(MOCK_HTML_PLOT_SNIPPETS_GO.items()),
)
def test_plot_atmospheric_co2_data_go(
    html_search_string: List[str],
    expected_value: List[bool],
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.plot_atmospheric_co2_data method.

        Test with plotly.graph_objects.

        Args:
            html_search_string (List[str]):
                Mock Plotly HTML file snippets to search for.

            expected_value (List[bool]):
                Mock expected boolean return values.

            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

            requests_mock (requests_mock.mocker):
                Mock HTTP request and response pytest fixture.

        Returns:
            None.
        """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Call the plot_atmospheric_co2_data_go method
    mock_response = cd.plot_atmospheric_co2_data(
        transposed_data=MOCK_CO2_PPM_GRAPH_DATA,
        plot_properties=APP.PlotProperties(
            **MOCK_HTML_PLOT_PROPERTIES_GO
        )
    )

    assert (html_search_string in mock_response) is expected_value

    return None


@patch.object(
    target=Path,
    attribute='mkdir'
)
def test_write_plot_html_file(
    mock_mkdir: MagicMock,
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.write_plot_html_file method.

        Args:
            mock_mkdir (unittest.mock.MagicMock):
                Mock pathlib.Path.mkdir function to prevent creating a
                new directory with the test_write_plot_html_file
                function.

            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    # Call the mock_api_request fixture
    mock_api_request(
        requests_mock=requests_mock
    )

    # Create an instance of the ClimateData.AtmosphericCo2PPM class
    cd = APP()

    # Define a mock_open object with mock_html_data
    write_html_mock = mock_open(
        read_data=MOCK_HTML_FILE_CONTENT
    )

    # Mock the builtins.open function
    with patch.object(
        target=builtins,
        attribute='open',
        new=write_html_mock
    ):

        # Call the cd.write_plot_html_file function
        cd.write_plot_html_file(
            file_name=MOCK_HTML_FILE_NAME.split(sep='.')[0],
            file_content=MOCK_HTML_FILE_CONTENT
        )

    # Assign the mock write() return value to a variable
    mock_write_value = write_html_mock.mock_calls[2].call_list()[0]

    # Convert mock_write_value to a string and extract the mock file contents
    mock_write_value = str(mock_write_value).split(sep="'")[1]

    # Replace literal \n characters with new line characters
    mock_write_value = mock_write_value.replace('\\n', '\n')

    # Confirm write_html_mock was called once
    assert write_html_mock.assert_called_once

    # Confirm the mock file name is in the write_html_mock.call_args_list
    assert MOCK_HTML_FILE_NAME in str(write_html_mock.call_args_list)

    # Confirm the mock file input value matches the mock file write value
    assert MOCK_HTML_FILE_CONTENT == mock_write_value

    # Confirm the number of chars written matches the expected value
    assert len(MOCK_HTML_FILE_CONTENT) == len(mock_write_value)

    return None


def test_write_plot_html_dir_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.write_plot_html_file method exceptions.

        Check for proper handling of an OSError exception when
        Python is unable to create a directory in storage.

        Args:
            mock_api_request (Callable):
                    Callable pytest fixture factory function that
                    allows passing arguments to the _mock_api_request
                    function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    with raises(
        expected_exception=FileExistsError
    ):

        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock
        )

        # Create an instance of the ClimateData.AtmosphericCo2PPM class
        cd = APP()

        # Call the write_plot_html_file method
        cd.write_plot_html_file()

    return None


def test_write_plot_html_file_error(
    mock_api_request: Callable,
    requests_mock: requests_mock.mocker
) -> None:
    """ Test the APP.write_plot_html_file method exceptions.

        Check for proper handling of a FileNotFound exception when
        Python is unable to write a file to storage.

        Args:
            mock_api_request (Callable):
                Callable pytest fixture factory function that
                allows passing arguments to the _mock_api_request
                function.

                requests_mock (requests_mock.mocker):
                    Mock HTTP request and response pytest fixture.

        Returns:
            None.
    """

    with raises(
        expected_exception=FileNotFoundError
    ):
        # Call the mock_api_request fixture
        mock_api_request(
            requests_mock=requests_mock
        )

        # Create an instance of the ClimateData.AtmosphericCo2PPM class
        cd = APP()

        # Call the write_plot_html_file method
        cd.write_plot_html_file()

    return None


# Add pytest functions for new AtmosphericCo2PPM methods
