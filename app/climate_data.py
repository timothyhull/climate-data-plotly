#!/usr/bin/env python3
""" Climate Data App Main Application. """

# Imports - Python Standard Library

# Imports - Third-Party

# Imports - Local
from ClimateData import ClimateData, PlotProperties, TransposedData

# Constants
FILE_SUFFIX = '.html'
# Plotly Express (px) file names
PX_BAR_PPM_FILE_NAME = 'px_ppm_bar_plot_1a'
PX_LINE_PPM_FILE_NAME = 'px_ppm_line_plot_1a'
PX_BAR_YOY_FILE_NAME = 'px_yoy_bar_plot_1a'
PX_LINE_YOY_FILE_NAME = 'px_yoy_line_plot_1a'
# Plotly Graph Objects (go) file names
GO_BAR_PPM_FILE_NAME = 'go_ppm_bar_plot_1a'
GO_LINE_PPM_FILE_NAME = 'go_ppm_line_plot_1a'
GO_BAR_YOY_FILE_NAME = 'go_yoy_bar_plot_1a'
GO_LINE_YOY_FILE_NAME = 'go_yoy_line_plot_1a'
PPM_BAR_PLOT_PROPERTIES = dict(
    compress_y_axis=True,
    date_label='Dates',
    line_graph=False,
    title='Monthly Atmospheric Co2 PPM Levels History',
    value_label='Atmospheric Co2 PPM',
)
PPM_LINE_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    date_label='Dates',
    line_graph=True,
    title='Monthly Atmospheric Co2 PPM Levels History',
    value_label='Atmospheric Co2 PPM',
)
YOY_BAR_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    date_label='Dates',
    line_graph=False,
    title='YoY Monthly Atmospheric Co2 Delta % History',
    value_label='YoY PPM Delta %',
)
YOY_LINE_PLOT_PROPERTIES = dict(
    compress_y_axis=False,
    date_label='Dates',
    line_graph=True,
    title='YoY Monthly Atmospheric Co2 Delta % History',
    value_label='YoY PPM Delta %',
)


# Plotly Express (px) function
def px_plot(
    transposed_data: TransposedData,
    properties: dict
) -> None:
    """ Generate a line or bar graph HTML file of atmospheric Co2 data.

        Plot data using Plotly Express (px).

        Args:
            transposed_data (TransposedData):
                Instance of the ClimateData.ClimateData.TransposedData
                class with data transposed for graphing.

            properties (dict):
                Dictionary object with plot-specific properties.
                Use one of PPM_BAR_PLOT_PROPERTIES, PPM_LINE_PLOT_PROPERTIES,
                YOY_BAR_PLOT_PROPERTIES, or YOY_LINE_PLOT_PROPERTIES
                constants.

        Returns:
            None.
    """

    # Set a file name argument with a value from the properties argument
    file_name = properties.get('file_name', 'name_unknown')

    # Remove the file_name key from the properties dictionary
    del properties['file_name']

    # Convert properties argument values to a PlotProperties object
    plot_properties = PlotProperties(**properties)

    # Call the climate_data.plot_atmospheric_co2_data_px method
    px_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=transposed_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=file_name,
        file_content=px_plot_data
    )

    return None


# Plotly Graph Object (go) function
def go_plot(
    transposed_data: TransposedData,
    properties: dict
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Plot data using Plotly Graph Objects (go).

        Args:
            transposed_data (TransposedData):
                Instance of the ClimateData.ClimateData.TransposedData
                class with data transposed for graphing.

            properties (dict):
                Dictionary object with plot-specific properties.
                Use one of PPM_BAR_PLOT_PROPERTIES, PPM_LINE_PLOT_PROPERTIES,
                YOY_BAR_PLOT_PROPERTIES, or YOY_LINE_PLOT_PROPERTIES
                constants.

        Returns:
            None.
    """

    # Set a file name argument with a value from the properties argument
    file_name = properties.get('file_name', 'name_unknown')

    # Remove the file_name key from the properties dictionary
    del properties['file_name']

    # Convert properties argument values to a PlotProperties object
    plot_properties = PlotProperties(**properties)

    # Call the climate_data.plot_atmospheric_co2_data_px method
    go_plot_data = climate_data.plot_atmospheric_co2_data_go(
        transposed_data=transposed_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=file_name,
        file_content=go_plot_data
    )

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

    # Setup properties object with a plot-specific file name
    properties = PPM_BAR_PLOT_PROPERTIES
    properties.update(dict(file_name=PX_BAR_PPM_FILE_NAME))

    # Generate a PPM bar graph
    px_plot(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {PX_BAR_PPM_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = PPM_LINE_PLOT_PROPERTIES
    properties.update(dict(file_name=PX_LINE_PPM_FILE_NAME))

    # Generate a PPM bar graph
    px_plot(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {PX_LINE_PPM_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = YOY_BAR_PLOT_PROPERTIES
    properties.update(dict(file_name=PX_BAR_YOY_FILE_NAME))

    # Generate a PPM bar graph
    px_plot(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {PX_BAR_YOY_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = YOY_LINE_PLOT_PROPERTIES
    properties.update(dict(file_name=PX_LINE_YOY_FILE_NAME))

    # Generate a PPM bar graph
    px_plot(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {PX_LINE_YOY_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = PPM_BAR_PLOT_PROPERTIES
    properties.update(dict(file_name=GO_BAR_PPM_FILE_NAME))

    # Generate a PPM bar graph
    go_plot(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {GO_BAR_PPM_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = PPM_LINE_PLOT_PROPERTIES
    properties.update(file_name=GO_LINE_PPM_FILE_NAME)

    # Generate a PPM bar graph
    go_plot(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {GO_LINE_PPM_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = YOY_BAR_PLOT_PROPERTIES
    properties.update(file_name=GO_BAR_YOY_FILE_NAME)

    # Generate a PPM bar graph
    go_plot(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {GO_BAR_YOY_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
    properties = YOY_LINE_PLOT_PROPERTIES
    properties.update(file_name=GO_LINE_YOY_FILE_NAME)

    # Generate a PPM bar graph
    go_plot(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        properties=properties
    )

    # Display a success message
    print(
        f'\nGenerated the file {GO_LINE_PPM_FILE_NAME}{FILE_SUFFIX}\n'
    )


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
