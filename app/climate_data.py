#!/usr/bin/env python3
""" Climate Data App Main Application. """

# Imports - Python Standard Library

# Imports - Third-Party

# Imports - Local
from ClimateData import ClimateData, PlotProperties

# Constants
FILE_SUFFIX = '.html'
# Plotly Express (px) file names
PX_PPM_BAR_FILE_NAME = 'px_ppm_bar_plot_1a'
PX_PPM_LINE_FILE_NAME = 'px_ppm_line_plot_1a'
PX_YOY_BAR_FILE_NAME = 'px_yoy_bar_plot_1a'
PX_YOY_LINE_FILE_NAME = 'px_yoy_line_plot_1a'
# Plotly Graph Objects (go) file names
GO_PPM_BAR_FILE_NAME = 'go_ppm_bar_plot_1a'
GO_PPM_LINE_FILE_NAME = 'go_ppm_line_plot_1a'
GO_YOY_BAR_FILE_NAME = 'go_yoy_bar_plot_1a'
GO_YOY_LINE_FILE_NAME = 'go_yoy_line_plot_1a'
PPM_PLOT_PROPERTIES = dict(
    date_label='Dates',
    value_label='Atmospheric Co2 PPM',
    title='Monthly Atmospheric Co2 PPM Levels History',
    compress_y_axis=True
)
YOY_PLOT_PROPERTIES = dict(
    date_label='Dates',
    value_label='YoY PPM Delta %',
    title='YoY Monthly Atmospheric Co2 Delta % History',
    compress_y_axis=False
)


# Plotly Express (px) functions
def px_ppm_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM using Plotly Express (px).

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **PPM_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    px_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=PX_PPM_BAR_FILE_NAME,
        file_content=px_plot_data
    )

    return None


def px_ppm_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM using Plotly Express (px).

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **PPM_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    px_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        PX_PPM_LINE_FILE_NAME, px_plot_data)

    return None


def px_yoy_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change using Plotly Express (px).

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **PPM_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    px_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=PX_YOY_BAR_FILE_NAME,
        file_content=px_plot_data
    )

    return None


def px_yoy_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change using Plotly Express (px).

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **PPM_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    px_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=PX_YOY_LINE_FILE_NAME,
        file_content=px_plot_data
    )

    return None


# Plotly Express (px) functions
def go_ppm_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM using Plotly Graph Objects.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **YOY_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    go_plot_data = climate_data.plot_atmospheric_co2_data_px(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=GO_PPM_BAR_FILE_NAME,
        file_content=go_plot_data
    )

    return None


def go_ppm_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM  using Plotly Graph Objects.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **YOY_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    go_plot_data = climate_data.plot_atmospheric_co2_data_go(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        GO_PPM_LINE_FILE_NAME, go_plot_data)

    return None


def go_yoy_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change using Plotly Graph Objects.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **YOY_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    go_plot_data = climate_data.plot_atmospheric_co2_data_go(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        line_graph=False,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=GO_YOY_BAR_FILE_NAME,
        file_content=go_plot_data
    )

    return None


def go_yoy_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change  using Plotly Graph Objects.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    # Create a PlotProperties object with a graph type
    plot_properties = PlotProperties(
        line_graph=False,
        **YOY_PLOT_PROPERTIES
    )

    # Call the climate_data.plot_atmospheric_co2_data_px method
    go_plot_data = climate_data.plot_atmospheric_co2_data_go(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        line_graph=True,
        plot_properties=plot_properties
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        file_name=GO_YOY_LINE_FILE_NAME,
        file_content=go_plot_data
    )

    return None


def px_graph_all() -> None:
    """ Run all Plotly Express (px) graph-generating functions.

        Args:
            None.

        Returns:
            None.
    """

    # Generate a PPM bar graph
    px_ppm_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PX_PPM_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a PPM line graph
    px_ppm_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PX_PPM_LINE_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY bar graph
    px_yoy_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PX_YOY_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY line graph
    px_yoy_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PX_YOY_LINE_FILE_NAME}{FILE_SUFFIX}\n'
    )

    return None


def go_graph_all() -> None:
    """ Run all Plotly Graph Object (go) graph-generating functions.

        Args:
            None.

        Returns:
            None.
    """

    # Generate a PPM bar graph
    go_ppm_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {GO_PPM_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a PPM line graph
    go_ppm_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {GO_PPM_LINE_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY bar graph
    go_yoy_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {GO_YOY_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY line graph
    go_yoy_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {GO_YOY_LINE_FILE_NAME}{FILE_SUFFIX}\n'
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
