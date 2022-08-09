#!/usr/bin/env python3
""" Climate Data App Main Application. """

# Imports - Python Standard Library

# Imports - Third-Party

# Imports - Local
from ClimateData import ClimateData

# Constants
FILE_SUFFIX = '.html'
PPM_BAR_FILE_NAME = 'ppm_bar_plot_1a'
PPM_LINE_FILE_NAME = 'ppm_line_plot_1a'
YOY_BAR_FILE_NAME = 'yoy_bar_plot_1a'
YOY_LINE_FILE_NAME = 'yoy_line_plot_1a'
PPM_PLOT_LABELS = dict(
    date_label='Dates',
    compress_y_axis=True,
    title='Monthly Atmospheric Co2 PPM Levels Over Time',
    value_label='Atmospheric Co2 PPM'
)
YOY_PLOT_LABELS = dict(
    date_label='Dates',
    compress_y_axis=False,
    title='Monthly Atmospheric Co2 PPM Levels Over Time',
    value_label='Atmospheric Co2 PPM'
)


def ppm_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    plot_data = climate_data.plot_atmospheric_co2_data(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        line_graph=False,
        **PPM_PLOT_LABELS
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        PPM_BAR_FILE_NAME, plot_data)

    return None


def ppm_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level in PPM.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    plot_data = climate_data.plot_atmospheric_co2_data(
        transposed_data=climate_data.transposed_co2_ppm_date_data,
        line_graph=True,
        **PPM_PLOT_LABELS
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        PPM_LINE_FILE_NAME, plot_data)

    return None


def yoy_bar(
    climate_data: ClimateData
) -> None:
    """ Generate a bar graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    plot_data = climate_data.plot_atmospheric_co2_data(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        line_graph=False,
        **YOY_PLOT_LABELS
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        YOY_BAR_FILE_NAME, plot_data)

    return None


def yoy_line(
    climate_data: ClimateData
) -> None:
    """ Generate a line graph HTML file of atmospheric Co2 data.

        Monthly Co2 level year over year change.

        Args:
            climate_data (ClimateData):
                Instance of the ClimateData.ClimateData class.

        Returns:
            None.
    """

    plot_data = climate_data.plot_atmospheric_co2_data(
        transposed_data=climate_data.transposed_co2_yoy_change_data,
        line_graph=True,
        **YOY_PLOT_LABELS
    )

    # Write climate data to a file
    climate_data.write_plot_html_file(
        YOY_LINE_FILE_NAME, plot_data)

    return None


def graph_all() -> None:
    """ Run all graph-generating functions.

        Args:
            None.

        Returns:
            None.
    """

    # Generate a PPM bar graph
    ppm_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PPM_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a PPM line graph
    ppm_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {PPM_LINE_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY bar graph
    yoy_bar(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {YOY_BAR_FILE_NAME}{FILE_SUFFIX}\n'
    )

    # Generate a YOY line graph
    yoy_line(
        climate_data=climate_data
    )
    print(
        f'\nGenerated the file {YOY_LINE_FILE_NAME}{FILE_SUFFIX}\n'
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
