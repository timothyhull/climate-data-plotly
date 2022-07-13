#!/usr/bin/env python3
""" Climate Data App Main Application. """

# Imports - Python Standard Library

# Imports - Third-Party

# Imports - Local
from ClimateData import ClimateData


def main() -> None:
    """ Main application:

            Args:
                None.

            Returns:
                None.
        """

    # Create an instance of ClimateData
    cd = ClimateData()
    print(len(cd.atmospheric_co2_data))

    return None


if __name__ == '__main__':
    main()
