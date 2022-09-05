#!/usr/bin/env python3
""" Climate Data App Web Application. """

# Imports - Python Standard Library

# Imports - Third-Party
from flask import Flask  # , render_template

# Imports - Local
# from app.ClimateData import AtmosphericCo2PPM, PlotProperties
from app.ClimateData import AtmosphericCo2PPM as ppm

# Create Flask object
flask_app = Flask(__name__)

# Constants
FLASK_HOST = 'localhost'
FLASK_PORT = 8088
FLASK_DEBUG = False


@flask_app.route(
    rule='/'
)
def index() -> str:
    """ Default URI rule for main/index page.

            Args:
                None.

            Returns:
                html_data (str):
                    HTML data for web browser consumption.
        """

    # Create PlotProperties object
    plot_properties = ppm.PlotProperties(
        compress_y_axis=True,
        line_graph=False,
        date_label='Dates',
        value_label='Atmospheric Co2 PPM',
        title='Monthly Atmospheric Co2 PPM Levels History',
        px_plot=False
    )

    # Create an instance of AtmosphericCo2PPM
    # cd = AtmosphericCo2PPM()
    cd = ppm()

    html_data = cd.plot_atmospheric_co2_data(
        plot_properties=plot_properties,
        transposed_data=cd.transposed_co2_ppm_date_data
    )

    # Render HTML from the index template
    # html_data = render_template(
    #     template_name_or_list='index.html',
    #     atmospheric_co2_data=cd.atmospheric_co2_data[:10]
    # )

    return html_data


if __name__ == '__main__':
    # Run the Flask application
    flask_app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
