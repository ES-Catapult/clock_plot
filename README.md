## clock_plot

clock_plot provides a simple way to visualize timeseries data mapping 24 hours onto the 360 degrees of a polar plot. 
For usage, please see the examples.ipynb Jupyter notebook

Time features are automatically generated for your timeseries
These features include:
year (int): Calendar year e.g. 2022
month (str): Calendar month e.g. "January"
year_month (int): Calendar year and month in the format YYYYMM e.g. 202201
day (int): Day of calendar year e.g. 25
date (str): Expressed in the format YYYY-MM-DD e.g. 2022-01-25
week (int): Week of the calendar year e.g. 5
dayofweek (str): Short version of day of week e.g. Tue
weekend (str): Either "weekday" or "weekend" where weekends are where dayofweek is either "Sat" or "Sun"
hour (int): Hour of the day in 24 clock e.g. 14
minute (int): Minute of the hour e.g. 42
degrees (int): Angle around 24 hour clock-face measured in degrees, calculated using hours and minutes
season (str): Season of the year defined as:
                "Winter" where month is either "December", "January" or "February"
                "Spring" where month is either "March", "April" or "May"
                "Summer" where month is either "June", "July" or "August"
                "Autumn" where month is either "September", "October" or "November"
Using these it is then simple to filter your data and format your plot.
For example you could filter for a particular year, plot seasons with different colors and weekday vs weekend days with different line dashes.
Examples of this are given in examples.ipynb

## Installation
To install this package run:
pip install /path/to/clock_plot

or to install in editable mode, use:
pip install -editable /path/to/clock_plot

