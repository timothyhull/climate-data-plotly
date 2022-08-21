# climate-data-plotly Repository

Days 83 + 84 assignment for TalkPython #100DaysOfCode.

## Build & Quality Status

[![BCH compliance](https://bettercodehub.com/edge/badge/timothyhull/climate-data-plotly?branch=main)](https://bettercodehub.com/results/timothyhull/climate-data-plotly)

![[Linting and Static Code Analysis](https://github.com/timothyhull/climate-data-plotly/actions/workflows/lint-files.yml)](https://img.shields.io/github/workflow/status/timothyhull/climate-data-plotly/Linting%20and%20Static%20Code%20Analysis?label=Linting%20and%20Static%20Code%20Analysis)

![[GitHub Workflow Status](https://github.com/timothyhull/climate-data-plotly/actions/workflows/pytest.yml)](https://img.shields.io/github/workflow/status/timothyhull/climate-data-plotly/pytest%20Testing?label=pytest)

## Application Framework

<!-- Application diagram -->
```mermaid
classDiagram
    repo_root <|-- app
    repo_root <|-- tests
    repo_root <|-- web
    app <|-- plot_files
    web <|-- templates
    class repo_root{
        # Repository root folder
        - repo_root/
    }
    class app{
        # Application folder
        - repo_root/app/
        ---
        # Runtime file with `main` function
        -climate_data.py
        ---
        # ClimateData class
        -ClimateData.py
    }
    class plot_files{
        # HTML plot file folder
        - repo_root/app/plot_files/
        ---
        # HTML plot files
        - climate_data_1.html
        - climate_data_2.html
        - climate_data_3.html
    }
    class tests{
         # Pytest folder
         - repo_root/tests/
         ---
         # Tests for ../app/ClimateData.py
         - file test_ClimateData.py
    }
    class web{
        # Flask application folder
        - repo_root/web/
        ---
        # Main Flask app file
        - flask_app.py
    }
    class templates{
        # Flask templates folder
        - repo_root/web/templates/
        ---
        # Main Flask app file
        - index.html
    }
```

## Sources

Climate data sourced from the [IMF[^1] Climate Change Indicators Dashboard](https://climatedata.imf.org "IMF Climate Change Indicators Dashboard")

[^1]: International Monetary Fund
