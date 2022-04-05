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

## When should you use these plots?
Radar/polar plots (of which clock plots are a special case) are [much maligned by visualisation experts](https://www.data-to-viz.com/caveat/spider.html), and for good reason. Whilst some of the common limitations are overcome with clock plots, two key ones remain:
1. It is harder to read quantitative values than on a linear axis
2. Areas scale quadratically (with the square of the value) rather than linearly, which can lead to overestimation of differences

Clock plots are therefore most suited for cases where understanding absolute values is less important and one or more of the following is true:
- behaviour around midnight is particularly important
- there are a 2-3 daily peaks and understanding at a glance when those are occurring is more important than their exact magnitude
- you want a distinctive, eye-catching graphic to engage people with your work

Note that they are particularly poorly suited to:
- timeseries with negative values (the radial axis becomes very unintuitive)
- timeseries with little within day variation (you just get circles!)

If you're not sure which is best for a particular use case, you can quickly toggle between a clock plot and a linear plot by adding `mode="line"` to your clock_plot call.