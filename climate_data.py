#!/usr/bin/env python3
""" Climate Data App Main Application. """

# Imports - Python Standard Library

# Imports - Third-Party

# Imports - Local
from app.ClimateData import (
    ClimateData, PlotProperties
)

# Constants
FILE_SUFFIX = '.html'
GO_PREFIX = 'go_'
PX_PREFIX = 'px_'
PLOT_FILE_NAME_STR = '\nGenerated the file {}{}\n'
PLOT_FILE_NAME_ERROR_STR = '\nUnable to generate a plot file\n'
PLOT_BAR_GRAPH_STR = 'bar'
PLOT_LINE_GRAPH_STR = 'line'
PLOT_UNKNOWN_GRAPH_STR = 'unknown type'
PLOT_PRINT_GRAPH_TYPE = {
        'True': PLOT_LINE_GRAPH_STR,
        'False': PLOT_BAR_GRAPH_STR,
        'None': PLOT_UNKNOWN_GRAPH_STR
    }
PLOT_RESULT_STR = '\nCreated the {} graph "{}"\n'
PLOT_RESULT_ERROR_STR = '\nUnable to successfully generate a plot file.'
# Plotly output file names
BAR_PPM_FILE_NAME = 'ppm_bar_plot_1a'
LINE_PPM_FILE_NAME = 'ppm_line_plot_1a'
BAR_YOY_FILE_NAME = 'yoy_bar_plot_1a'
LINE_YOY_FILE_NAME = 'yoy_line_plot_1a'
# Plotly graph properties
PPM_LABELS = dict(
    date_label='Dates',
    title='Monthly Atmospheric Co2 PPM Levels History',
    value_label='Atmospheric Co2 PPM'
)
YOY_LABELS = dict(
    date_label='Dates',
    title='YoY Monthly Atmospheric Co2 Delta % History',
    value_label='YoY PPM Delta %'
)
PPM_BAR_PLOT_PROPERTIES = dict(
    compress_y_axis=True,
    line_graph=False,
    **PPM_LABELS
)
PPM_LINE_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    line_graph=True,
    **PPM_LABELS
)
YOY_BAR_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    line_graph=False,
    **YOY_LABELS
)
YOY_LINE_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    line_graph=True,
    **YOY_LABELS
)


# Plotly Express (px) function
def _plot_graph(
    plot_properties: dict,
    climate_data: ClimateData
) -> bool:
    """ Generate a line or bar graph HTML file of atmospheric Co2 data.

        Args:
            plot_properties (dict):
                dict object with plot-specific properties.
                Use one of PPM_BAR_PLOT_PROPERTIES,
                PPM_LINE_PLOT_PROPERTIES, YOY_BAR_PLOT_PROPERTIES,
                or YOY_LINE_PLOT_PROPERTIES constants.

            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.
                Default is creating a new instance of
                ClimateData.ClimateData.

        Returns:
            plot_status (bool):
                Boolean value for whether or not the function
                runs successfully.
    """

    # Extract and remove the transposed plot data from plot_properties
    transposed_data = plot_properties.get('transposed_data', None)
    del plot_properties['transposed_data']

    # Convert the plot_properties dict to a PlotProperties object
    plot_properties = PlotProperties(**plot_properties)

    # Call the climate_data.plot_atmospheric_co2_data method
    plot_data = climate_data.plot_atmospheric_co2_data(
        transposed_data=transposed_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    plot_file_path, plot_char_count = climate_data.write_plot_html_file(
        file_name=plot_properties.file_name,
        file_content=plot_data
    )

    # Determine if the plot file generation is successful
    plot_valid = _validate_new_plot(
        plot_file_path=plot_file_path,
        plot_char_count=plot_char_count
    )

    # Print the result of the plot file generation
    _print_plot_result(
        plot_valid=plot_valid,
        plot_properties=plot_properties
    )

    return plot_valid


def plot_graph(
    climate_data: ClimateData,
    plot_properties: dict
) -> bool:
    """ Helper function for the _plot_graph function.

        Reduces duplicate instances of calling the _plot_graph
        function directly.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        plot_properties (dict):
            dict object with plot-specific properties.
            Use one of PPM_BAR_PLOT_PROPERTIES,
            PPM_LINE_PLOT_PROPERTIES, YOY_BAR_PLOT_PROPERTIES,
            or YOY_LINE_PLOT_PROPERTIES constants.

        Returns:
            plot_status (bool):
                Boolean value for whether or not the function
                runs successfully.
    """

    # Generate a PPM bar graph
    plot_status = _plot_graph(
        plot_properties=plot_properties,
        climate_data=climate_data
    )

    # Display the generated file name with a status indication
    if plot_status is True:
        # Display the generated file name
        print(PLOT_FILE_NAME_STR.format(
            plot_properties.get('file_name', 'unknown'),
            FILE_SUFFIX)
        )
    else:
        # Display an error message
        print(PLOT_FILE_NAME_ERROR_STR)

    return plot_status


def _create_ppm_plot_properties(
    plot_properties: dict,
    file_name: str,
    climate_data: ClimateData
) -> dict:
    """ Create a plot_properties dictionary for Co2 PPM date data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

            plot_properties (dict):
                dict object with plot-specific properties.
                Use one of PPM_BAR_PLOT_PROPERTIES,
                PPM_LINE_PLOT_PROPERTIES, YOY_BAR_PLOT_PROPERTIES,
                or YOY_LINE_PLOT_PROPERTIES constants.

            file_name (str):
                Name of the plot file to write.

        Returns:
            plot_properties (dict):
                dict of plot properties.
    """

    # Update the plot_properties dict with Co2 PPM date data and a file name
    plot_properties.update(
        dict(
            transposed_data=climate_data.transposed_co2_ppm_date_data,
            file_name=file_name
        )
    )

    return plot_properties


def _create_yoy_plot_properties(
    plot_properties: dict,
    file_name: str,
    climate_data: ClimateData
) -> dict:
    """ Create a plot_properties dictionary for Co2 YoY change data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

            plot_properties (dict):
                dict object with plot-specific properties.
                Use one of PPM_BAR_PLOT_PROPERTIES,
                PPM_LINE_PLOT_PROPERTIES, YOY_BAR_PLOT_PROPERTIES,
                or YOY_LINE_PLOT_PROPERTIES constants.

            file_name (str):
                Name of the plot file to write.

        Returns:
            plot_properties (dict):
                dict of plot properties.
    """

    # Update the plot_properties dict with Co2 PPM date data and a file name
    plot_properties.update(
        dict(
            transposed_data=climate_data.transposed_co2_yoy_change_data,
            file_name=file_name
        )
    )

    return plot_properties


def _validate_new_plot(
    plot_file_path: str,
    plot_char_count: int
) -> bool:
    """ Checks to determine if a plot file generates successfully.

        Args:
            plot_file_path (str):
                Absolute path for the new file.

            plot_char_count (int):
                Integer of the number of characters written to the
                plot file.

        Returns:
            plot_valid (bool):
                True if the file generates successfully.  False if the
                file fails to generate.
    """

    # Read the plot file
    with open(
        file=plot_file_path,
        mode='rt',
        encoding='utf-8'
    ) as file:
        # Get the number of characters in the plot file
        file_char_count = len(file.read())

    # Determine if the plot file generation is successful
    if file_char_count == plot_char_count:
        plot_valid = True
    else:
        plot_valid = False

    return plot_valid


def _print_plot_result(
    plot_valid: bool,
    plot_properties: PlotProperties
) -> None:
    """ Display the result of the plot file generation status.

        Args:
            plot_valid (bool):
                Status of the plot generation validation.

            plot_properties (PlotProperties):
                Plot-specific information for us in result display.

        Returns:
            None.
    """

    # Determine the graph type with a dictionary lookup of str(plot_valid)
    graph_type = PLOT_PRINT_GRAPH_TYPE.get(str(plot_valid), 'None')

    # Display a success or error message
    print(PLOT_RESULT_STR.format(graph_type, plot_properties.title))

    return None


def plot_px_ppm_bar(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Express bar graph with monthly PPM data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_ppm_plot_properties(
        plot_properties=PPM_BAR_PLOT_PROPERTIES,
        file_name=f'{PX_PREFIX}{BAR_PPM_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_px_ppm_line(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Express line graph.

        Use monthly PPM data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_ppm_plot_properties(
        plot_properties=PPM_LINE_PLOT_PROPERTIES,
        file_name=f'{PX_PREFIX}{LINE_PPM_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_px_yoy_bar(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Express bar graph.

        Use PPM YoY monthly % change data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_yoy_plot_properties(
        plot_properties=YOY_BAR_PLOT_PROPERTIES,
        file_name=f'{PX_PREFIX}{BAR_YOY_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_px_yoy_line(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Express bar graph.

        Use PPM YoY monthly % change data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_yoy_plot_properties(
        plot_properties=YOY_LINE_PLOT_PROPERTIES,
        file_name=f'{PX_PREFIX}{LINE_YOY_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_go_ppm_bar(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Graph Object bar graph.

        Use monthly PPM data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_ppm_plot_properties(
        plot_properties=PPM_BAR_PLOT_PROPERTIES,
        file_name=f'{GO_PREFIX}{BAR_PPM_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_go_ppm_line(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Graph Object line graph.

        Use monthly PPM data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_ppm_plot_properties(
        plot_properties=PPM_LINE_PLOT_PROPERTIES,
        file_name=f'{GO_PREFIX}{LINE_PPM_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_go_yoy_bar(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Graph Object bar graph.

        Use PPM YoY monthly % change data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_yoy_plot_properties(
        plot_properties=YOY_BAR_PLOT_PROPERTIES,
        file_name=f'{GO_PREFIX}{BAR_YOY_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def plot_go_yoy_line(
    climate_data: ClimateData
) -> None:
    """ Create a Plotly Graph Object line graph.

        Use PPM YoY monthly % change data.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Setup plot properties object with a plot-specific file name
    plot_properties = _create_yoy_plot_properties(
        plot_properties=YOY_LINE_PLOT_PROPERTIES,
        file_name=f'{GO_PREFIX}{LINE_YOY_FILE_NAME}',
        climate_data=climate_data
    )

    # Call the _plot_graph function
    plot_graph(climate_data=climate_data, plot_properties=plot_properties)

    return None


def px_graph_all(
    climate_data: ClimateData
) -> None:
    """ Run all Plotly Express (px) graph-generating functions.

        climate_data (ClimateData):
            Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Generate a Plotly Express PPM bar graph
    plot_px_ppm_bar(
        climate_data=climate_data
    )

    # Generate a Plotly Express PPM line graph
    plot_px_ppm_line(
        climate_data=climate_data
    )

    # Generate a Plotly Express YOY bar graph
    plot_px_yoy_bar(
        climate_data=climate_data
    )

    # Generate a Plotly Express YOY line graph
    plot_px_yoy_line(
        climate_data=climate_data
    )

    return None


def go_graph_all(
    climate_data: ClimateData
) -> None:
    """ Run all Plotly Express (px) graph-generating functions.

        climate_data (ClimateData):
            Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Generate a Plotly Graph Object PPM bar graph
    plot_go_ppm_bar(
        climate_data=climate_data
    )

    # Generate a Plotly Graph Object PPM line graph
    plot_go_ppm_line(
        climate_data=climate_data
    )

    # Generate a Plotly Graph Object YOY bar graph
    plot_go_yoy_bar(
        climate_data=climate_data
    )

    # Generate a Plotly Graph Object YOY line graph
    plot_go_yoy_line(
        climate_data=climate_data
    )

    return None


def graph_all(
    climate_data: ClimateData
) -> None:
    """ Run all Plotly Express (px) graph-generating functions.

        climate_data (ClimateData):
            Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Graph all Plotly Express plots
    px_graph_all(
        climate_data=climate_data
    )

    # Graph all Plotly Graph Object plots
    go_graph_all(
        climate_data=climate_data
    )


def main() -> ClimateData:
    """ Main application.

        Args:
            None.

        Returns:
            cd (ClimateData):
                Instance of the ClimateData.ClimateData class.
    """

    # Create an instance of ClimateData
    climate_data = ClimateData()

    return climate_data


if __name__ == '__main__':
    climate_data = main()
