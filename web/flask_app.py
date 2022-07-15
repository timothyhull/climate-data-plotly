#!/usr/bin/env python3
""" Climate Data App Web Application. """

# Imports - Python Standard Library

# Imports - Third-Party
from flask import Flask

# Imports - Local
from app.ClimateData import ClimateData

# Create Flask object
app = Flask(__name__)


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

    html_data = cd.atmospheric_co2_data[0]

    return html_data


if __name__ == '__main__':
    # Run the Flask application
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
