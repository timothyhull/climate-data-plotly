#!/usr/bin/env python3
""" Climate Data App Web Application. """

# Imports - Python Standard Library

# Imports - Third-Party
from flask import Flask

# Imports - Local
from app.ClimateData import ClimateData

# Create Flask object
app = Flask(__name__)

# Constants
FLASK_HOST = 'localhost'
FLASK_PORT = 8088
FLASK_DEBUG = False


@app.route(
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

    # Create an instance of ClimateData
    cd = ClimateData()

    # Set the html_data variable
    html_data = cd.atmospheric_co2_data[0]

    return html_data


if __name__ == '__main__':
    # Run the Flask application
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
