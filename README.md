# NBA Analytics


## Authors
- **Nicholas Cantalupa** - [ncantalupa](https://github.com/ncantalupa)
- **Sean Duffy** - [sean-r-duffy](https://github.com/sean-r-duffy)
- **Aditya Saxena** - [1adityasaxena](https://github.com/1adityasaxena)
- **Pazin Taransombat** - [tarasansombat-p](https://github.com/tarasansombat-p)


## Overview
Utilizing NBA and combine data to predict player/team performance and improve drafting


## Features
- Player style analysis
- Predictive modeling for game outcomes


## Table of Contents
- [Project Organization](#project-organization)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [License](#license)


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for nba_analytics
│                         and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── nba_analytics                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes nba_analytics a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```


## Installation
Follow these steps to set up the project locally:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/NBA-Analytics.git
    cd NBA-Analytics
    ```

2. (Optional) Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
   or
   ```sh
    conda create --name nba-analytics python=3.8
    conda activate nba-analytics
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
   or
   ```sh
    conda install --file requirements.txt
    ```

4. Set up any necessary environment variables or configuration files as specified in [Geting Started](./docs/docs/getting-started.md).


## Usage
To use this project, follow these steps:

1. Run the main script:
    ```sh
    python main.py
    ```

2. Access the analysis and visualizations:
    - Open `index.html` in your web browser to view the dashboard.
    - Use the command line interface to run specific analyses.

For detailed usage instructions, please refer to [Geting Started](./docs/docs/getting-started.md).


## Data Sources
- https://stathead.com/basketball/
- https://github.com/swar/nba_api

## License
This project is licensed under the terms of the [MIT License](./LICENSE).

--------
