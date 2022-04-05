## clock_plot

clock_plot provides a simple way to visualize timeseries data mapping 24 hours onto the 360 degrees of a polar plot. 
For usage, please see the [examples.ipynb](examples.ipynb) Jupyter notebook

![seasonal gas usage clock plot](/data/seasonal_gas_usage.png)

## Installation
To install this package run:
`pip install clock_plot`

## Available features
Time features are automatically generated for your timeseries. These features include:
| Feature    | Type | Description                                                           | Example Values                                                                             |
| ---------- | ---- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| year       | int  | Calendar year                                                         | 2022                                                                                       |
| month      | str  | Calendar month                                                        | "January"                                                                                  |
| year_month | int  | Calendar year and month in the format YYYYMM                          | 202201                                                                                     |
| day        | int  | Day of calendar year                                                  | 25                                                                                         |
| date       | str  | Expressed in the format YYYY-MM-DD                                    | "2022-01-25"                                                                               |
| week       | int  | ISO week of the calendar year                                         | 5                                                                                          |
| dayofweek  | str  | Short version of day of week                                          | "Tue"                                                                                      |
| weekend    | str  | Either "weekday" or "weekend", where "weekend" is Saturday and Sunday | "weekend" (Sat/Sun) <br> "weekday" (Mon-Fri)                                               |
| hour       | int  | Hour of the day in 24 clock                                           | 14                                                                                         |
| minute     | int  | Minute of the hour                                                    | 42                                                                                         |
| degrees    | int  | Angle around 24 hour clock-face measured in degrees                   | 341                                                                                        |
| season     | str  | Season of the year defined based on month, with Winter being Dec-Feb  | "Winter" (Dec-Feb) <br> "Spring" (Mar-May) <br> "Summer" (Jun-Aug) <br> "Autumn" (Sep-Nov) |

These can be used to filter your data and format your plot.

For example you could filter for a particular year, plot seasons with different colors and weekday vs weekend days with different line dashes.
Examples of this are given in examples.ipynb
