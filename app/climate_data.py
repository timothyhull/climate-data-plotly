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
    climate_data.write_plot_html_file(
        file_name=plot_properties.file_name,
        file_content=plot_data
    )

    # Display a success message
    if plot_properties.line_graph is True:
        graph_type = 'line'
    elif plot_properties.line_graph is False:
        graph_type = 'bar'
    else:
        graph_type = 'unknown type'

    print(
        f'\nPlotted the {graph_type} graph '
        f'"{plot_properties.title}"\n'
    )

    return True


def plot_graph(
    climate_data: ClimateData,
    plot_properties: PlotProperties
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

    # Display a success message
    print(
        '\nGenerated the file '
        f'{plot_properties.get("file_name", "unknown")}{FILE_SUFFIX}\n'
    )

    return plot_status


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

    # Setup properties object with a plot-specific file name
    plot_properties = PPM_BAR_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{PX_PREFIX}{BAR_PPM_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_ppm_date_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = PPM_LINE_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{PX_PREFIX}{LINE_PPM_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_ppm_date_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = YOY_BAR_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{PX_PREFIX}{BAR_YOY_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_yoy_change_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = YOY_LINE_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{PX_PREFIX}{LINE_YOY_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_yoy_change_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = PPM_BAR_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{GO_PREFIX}{BAR_PPM_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_ppm_date_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = PPM_LINE_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{GO_PREFIX}{LINE_PPM_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_ppm_date_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = YOY_BAR_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{GO_PREFIX}{BAR_YOY_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_yoy_change_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

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

    # Setup properties object with a plot-specific file name
    plot_properties = YOY_LINE_PLOT_PROPERTIES
    plot_properties.update(
        dict(
            file_name=f'{GO_PREFIX}{LINE_YOY_FILE_NAME}',
            transposed_data=climate_data.transposed_co2_yoy_change_data
        )
    )

    # Call the _plot_graph function
    plot_graph(
        climate_data=climate_data,
        plot_properties=plot_properties
    )

    return None


def px_graph_all() -> None:
    """ Run all Plotly Express (px) graph-generating functions.

        Args:
            None.

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


def go_graph_all() -> None:
    """ Run all Plotly Graph Object (go) graph-generating functions.

        Args:
            None.

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
