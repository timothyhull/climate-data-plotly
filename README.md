# climate-data-plotly Repository

## Build & Quality Status

[![BCH compliance](https://bettercodehub.com/edge/badge/timothyhull/climate-data-plotly?branch=main)](https://bettercodehub.com/results/timothyhull/climate-data-plotly)

![[Linting and Static Code Analysis](https://github.com/timothyhull/climate-data-plotly/actions/workflows/lint-files.yml)](https://img.shields.io/github/workflow/status/timothyhull/climate-data-plotly/Linting%20and%20Static%20Code%20Analysis?label=Linting%20and%20Static%20Code%20Analysis)

![[GitHub Workflow Status](https://github.com/timothyhull/climate-data-plotly/actions/workflows/pytest.yml)](https://img.shields.io/github/workflow/status/timothyhull/climate-data-plotly/pytest%20Testing?label=pytest)

## Application Framework

<!-- Application diagram -->
```mermaid
```

```text
|->| app  # Application folder
|->|->| climate_data.py  # Runtime file with `main` function
|->|->| ClimateData.py  # ClimateData class
|->| tests  # Pytest folder
|->|->| test_files.py  # Pytest files
|->|->|->| test_ClimateData.py
|->| web  # Flask application folder
|->|->| flask_app.py  # Flask app file
|->|->| templates  # Flask templates folder
|->|->|->| index.html  # Jinja template for `index.html`
```

## Sources

Climate data sourced from the [IMF[^1] Climate Change Indicators Dashboard](https://climatedata.imf.org "IMF Climate Change Indicators Dashboard")

[^1]: International Monetary Fund
