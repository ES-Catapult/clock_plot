import warnings
from typing import Union
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy


def create_datetime_vars(data_in: pd.DataFrame, datetime_col: str, bins_per_day: int = 24) -> pd.DataFrame:
    """Create all the datetime-related columns that might be used for analysis/plotting
        columns and their possible values are:
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

    Args:
        data (pandas.DataFrame): The DataFrame involved
        datetime_col (str): The column containing the datetime
        bins_per_day (int): The number of bins into which data will be aggregated (over a day).
                This is useful when you have unequally spaced datetimes datatimes. (Defaults to 24)

    Returns:
        pandas.DataFrame: Copy of the input DataFrame with datetime-related columns added
    """
    data = data_in.copy()
    data[datetime_col] = pd.to_datetime(data[datetime_col])

    data["year"] = data[datetime_col].dt.year
    data["month"] = data[datetime_col].dt.strftime("%B")
    data["year_month"] = data[datetime_col].dt.strftime("%Y%m").astype(int)
    data["day"] = data[datetime_col].dt.day
    data["date"] = data[datetime_col].dt.strftime("%Y-%m-%d")
    data["week"] = data[datetime_col].dt.isocalendar().week
    data["dayofweek"] = data[datetime_col].dt.strftime("%a")
    data["weekend"] = "Weekday"
    data.loc[(data["dayofweek"] == "Sat") | (data["dayofweek"] == "Sun"), "weekend"] = "Weekend"
    data["hour"] = data[datetime_col].dt.hour
    data["minute"] = data[datetime_col].dt.minute
    data["degrees"] = 360 * data["hour"] / 24
    # Temporarily keep this methodology, in the long-term this needs fixing to use the binning method for all
    # circumstances
    if bins_per_day != 24:
        data["degrees"] = data["degrees"] + (360 * data["minute"] / (60 * 24))
        data["degree_bins"] = pd.cut(data["degrees"], bins=bins_per_day)
        data["degrees"] = data["degree_bins"].map(lambda x: x.mid).astype(int)

    data["season"] = data["month"].map(
        {
            "December": "Winter",
            "January": "Winter",
            "February": "Winter",
            "March": "Spring",
            "April": "Spring",
            "May": "Spring",
            "June": "Summer",
            "July": "Summer",
            "August": "Summer",
            "September": "Autumn",
            "October": "Autumn",
            "November": "Autumn",
        }
    )

    return data


def default_category_orders() -> dict:
    """Returns the default dictionary of category orders"""
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekend_order = ["Weekday", "Weekend"]
    season_order = ["Spring", "Summer", "Autumn", "Winter"]
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    category_orders = {
        "dayofweek": day_order,
        "weekend": weekend_order,
        "season": season_order,
        "month": month_order,
    }

    return category_orders


def create_title(title_start: str, filters: dict, line_group: str):
    """Automatically generates chart titles for the given filters and line groupings

    Args:
        title_start (str): The start of the title
        filters (dict): The filters applied to the data
        line_group (str): The lowest level of grouping applied to the data

    Returns:
        str: The title string
    """
    # Try to tidy up the list of filter values ready for printing in the chart title. This will work
    # for straightforward cases (single values, non-nested lists) but will fail for nested lists, in
    # which case just give up and don't bother to include it in the title
    if filters:
        try:
            tidied_filter_vals = ""
            keys = list(filters.keys())
            values = []
            for key in keys:
                values.append(filters[key])

            tidied_filter_vals = tidied_filter_vals + " & ".join([str(x) for x in values if type(x) is not list])
            if any(isinstance(val, list) for val in values) & any(not isinstance(val, list) for val in values):
                tidied_filter_vals = tidied_filter_vals + " & "
            tidied_filter_vals = tidied_filter_vals + " & ".join(
                [str(y) for x in values if type(x) is list for y in x]
            )
        except Exception:
            tidied_filter_vals = ""

    title = "by Hour of Day"
    if title_start != "":
        title = f"{title_start} {title}"
    if filters:
        title = title + f" for {tidied_filter_vals}"
    if line_group is not None:
        title = title + f"<br>(each line represents a single {line_group})"

    return title


def filter_and_group_data(
    data: pd.DataFrame,
    datetime_col: str,
    value_col: str,
    filters: dict = {},
    aggregate: dict = {None: "mean"},
    line_group: str = None,
    color: str = None,
    line_dash: str = None,
    bins_per_day: int = None,
) -> Union[pd.DataFrame, pd.DataFrame]:
    """Filter and then group the data based on given parameters

    Args:
        data (pd.DataFrame): The data to filter and group
        datetime_col (str): The datetime column name
        value_col (str): The name of the column containing the values to be grouped
        filters (dict, optional): Dictionary fiters, key-value pairs are column names and values to keep respectively.
                                  Defaults to {}.
        aggregate (_type_, optional): Dictionary containing a single key-value pair used to specify an additional
                                      level of aggregation line.
                Key gives column name to aggregate and value gives the aggregation method. Defaults to {None: "mean"}.
        line_group (str, optional): Name of column to use a the lowest level of grouping when plotting.
                                    Defaults to None.
        color (str, optional): Name of column to use to group by color. Defaults to None.
        line_dash (str, optional): Name of column to use to group by line dash. Defaults to None.
        bins_per_day (int, optional): Number of bins to group data into for each hour. Defaults to None.

    Raises:
        Exception: When an expected column is not present in the given DataFrame
        Exception: When the given filters leave 0 rows of data remaining

    Returns:
        Union[pd.DataFrame, pd.DataFrame]: The filtered and grouped data
    """
    agg_col = list(aggregate.keys())[0]
    agg_fn = list(aggregate.values())[0]
    relevant_cols = [col for col in [line_group, color, line_dash, "degrees", agg_col] + list(filters.keys()) if col]

    # If columns have been specified that don't exist (or bins_per_day is manually specified) then
    # generate the datatime vars to see if that helps
    if not set(relevant_cols).issubset(data.columns) or bins_per_day or len(relevant_cols) == 0:
        data = create_datetime_vars(data, datetime_col, bins_per_day)
    # If there are still missing columns raise an Exception
    if not set(relevant_cols).issubset(data.columns):
        missing_cols = [col for col in relevant_cols if col not in data.columns]
        raise KeyError(f"The following columns are missing from the supplied dataset: {missing_cols}")

    filtered_data = data
    if len(filters) > 0:
        # Apply all the specified filters
        for col, val in filters.items():
            # Note that the check that col is in filtered_data.columns has already been done above
            if col is not None:
                if type(val) is list:
                    filtered_data = filtered_data[filtered_data[col].isin(val)]
                else:
                    filtered_data = filtered_data[filtered_data[col] == val]

        if len(filtered_data) == 0:
            raise Exception("Filtering data leaves 0 rows remaining. Check the filters that have been specified")

    # Group by the required columns (using the list comprehension to remove columns that are None)
    grouped_data = (
        filtered_data.groupby([col for col in [line_group, color, line_dash, "degrees"] if col])[value_col]
        .agg(agg_fn)
        .reset_index()
    )

    if (grouped_data[value_col] < 0).any():
        warnings.warn(
            "Data contains negative values. A plot will be produced but they are often difficult to" " interpret"
        )

    return filtered_data, grouped_data


def spline_interp(grouped_data: pd.DataFrame, value_col: str, groups: list, grouped_columns: list) -> pd.DataFrame:
    """Perform spline interpolation on the given data

    Args:
        grouped_data (pd.DataFrame): The data to interpolate
        value_col (str): The column name holding the values to be interpolated
        groups (list): The groups of values on which the data will be separated for interpolartion
        grouped_columns (list): The column names that were used for grouping the data

    Returns:
        pd.DataFrame: The interpolated data
    """
    interp_data = pd.DataFrame()
    for values in groups:
        filt = (grouped_data[grouped_columns] == values).all(axis=1)
        df = grouped_data[filt].copy()
        # It only makes sense to interpolate if we have enough data, here we choose 8 points (i.e. 3 hour intervals)
        if len(df) >= 8:
            # Want to put first values at end and last values at start to use for interpolation
            # We use 3 values as we are doing a cublic spline. This is the minimum needed for good interpolation
            # around 0-360 deg.
            start = range(0, 3)
            end = range(-3, 0)
            df = pd.concat([pd.DataFrame(df.iloc[end, :]), df, pd.DataFrame(df.iloc[start, :])], axis=0)
            df.iloc[end, df.columns == "degrees"] = df.iloc[end]["degrees"] + 360
            df.iloc[start, df.columns == "degrees"] = df.iloc[start]["degrees"] - 360
            # Reindex so we have rows for every degree value (plus the original rows)
            new_index = np.linspace(0, 360, 361)
            df = df.set_index("degrees")
            df = df.reindex(df.index.union(new_index))
            df[grouped_columns] = values
            df[value_col] = df[value_col].astype(float).interpolate(method="cubicspline")
            df.reset_index(inplace=True)
            df = df.loc[(df["degrees"] >= 0) & (df["degrees"] < 360)]
            interp_data = pd.concat([interp_data, df])

    return interp_data


def plot_averages(
    fig: go.Figure,
    data: pd.DataFrame,
    value_col: str,
    aggregate: dict,
    color: str,
    line_shape: str = "spline",
    color_discrete_sequence: list = px.colors.qualitative.G10,
    category_orders: dict = default_category_orders(),
    mode: str = "polar",
):
    """Add traces for the aggregated data

    Args:
        fig (go.Figure): The existing figure to which the traces will be added
        data (pd.DataFrame): The data to aggregate
        value_col (str): Name of the column containing the value to aggregate
        aggregate (dict): Dictionary containing a single key-value pair.
                Key gives column name to aggregate and value gives the aggregation method.
        color (str): Name of column to use to group by color.
        line_shape (str, optional): Whether to smooth the lines, one of either 'linear' or 'spline'.
                                    Defaults to 'spline'
        color_discrete_sequence (list, optional): List of colors to use for the chart.
                                                    Defaults to px.colors.qualitative.G10
        category_orders (dict, optional): Dictionary where the key-value pairs are column names and a list of values
                                          in the desired order. This is used to set relative ordering of categories
                                          and is important for fixing line colors and legend orders.
                                          Defaults to default_category_orders()
        mode (str, optional): Whether to plot "polar" or "flat" (cartesian). Defaults to "polar".

    Returns:
        go.Figure: The figure with added traces for aggregated data
    """
    agg_col = list(aggregate.keys())[0]
    agg_fn = list(aggregate.values())[0]
    agg_data = data.groupby([agg_col, "degrees"])[value_col].agg(agg_fn).reset_index()
    # Want to change the data labels to reflect that it is aggregated ( This appears in the legend )
    agg_data[agg_col] = agg_data[agg_col].map(("{} (" + agg_fn + ")").format)
    # Also need to add these categories to the category_orders dict ( So the color and legend order are consistent)
    if agg_col in category_orders:
        category_orders[agg_col] = category_orders[agg_col] + [
            f"{value} ({agg_fn})" for value in category_orders[agg_col]
        ]

    if mode == "polar":
        agg_fig = px.line_polar(
            agg_data,
            theta="degrees",
            r=value_col,
            color=color,
            line_close=True,
            line_shape=line_shape,
            category_orders=category_orders,
            color_discrete_sequence=color_discrete_sequence,
        )
    else:
        agg_fig = px.line(
            agg_data,
            x="degrees",
            y=value_col,
            color=color,
            line_shape=line_shape,
            category_orders=category_orders,
            color_discrete_sequence=color_discrete_sequence,
        )
    agg_fig.update_traces(line_width=6)
    fig.add_traces(list(agg_fig.select_traces()))

    return fig


def clock_plot(
    data: pd.DataFrame,
    datetime_col: str,
    value_col: str,
    filters: dict = {},
    aggregate: dict = {None: "mean"},
    line_group: str = None,
    color: str = None,
    line_dash: str = None,
    line_shape: str = "spline",
    title_start: str = "",
    title: str = None,
    bins_per_day: int = 24,
    show: bool = True,
    color_discrete_sequence: list = None,
    category_orders: dict = {},
    text_noon: bool = True,
    mode: str = "polar",
    **kwargs,
):
    """Plot a polar chart showing value by hour of day

    Args:
        data (pandas.DataFrame): DataFrame containing the values to plot as a timeseries
        datetime_col (str): Name of the column containing the datetime
        value_col (str): Name of the column containing the value to plot
        filters (dict, optional): Dictionary filters, key-value pairs are column names and values to keep respectively.
                                  Defaults to {}.
        aggregate (_type_, optional): Dictionary containing a single key-value pair.
                                      Key gives column name to aggregate and value gives the aggregation method.
                                      Defaults to {None: "mean"}.
        line_group (str, optional): Name of column to use a the lowest level of grouping when plotting.
                                    Defaults to None.
        color (str, optional): Name of column to use to group by color. Defaults to None.
        line_dash (str, optional): Name of column to use to group by line dash. Defaults to None.
        line_shape (str, optional): Whether to smooth the lines, one of either 'linear' or 'spline'.
                                    Defaults to "spline".
        title_start (str, optional): A string to prefix to the automated chart title. Defaults to "".
        title (str, optional): Overrides the automated chart title. Defaults to None.
        bins_per_day (int, optional): Number of bins to group data into over a day. This is useful when using
                                      irregularly spaced datetimes. Defaults to 24.
        show (bool, optional): Whether to display the chart after it is generated. Defaults to True.
        color_discrete_sequence (list, optional): List of colors to use for the chart. Defaults to None.
        category_orders (dict, optional): Dictionary where the key-value pairs are column names and a list of values
                                          in the desired order. This is used to set relative ordering of categories
                                          and is important for fixing line colors and legend orders. Defaults to {}.
        text_noon (bool, optional): Whether to replace hours 0 and 12 with "Midnight" and "Noon" respectively.
                                    Defaults to True.
        mode (str, optional): Whether to plot "polar" or "line" (cartesian). Defaults to "polar".
        **kwargs: Accepts and passes on any arguments accepted by plotly express line_polar()

    Returns:
        (plotly.graph_objects.Figure): The generated plotly figure object containing the polar charts.
    """
    filtered_data, grouped_data = filter_and_group_data(
        data,
        datetime_col,
        value_col,
        filters,
        aggregate,
        line_group,
        color,
        line_dash,
        bins_per_day,
    )

    # The order in which categories are plotted determins their colour which we want to be consistent and correct
    def_category_orders = default_category_orders()
    def_category_orders.update(category_orders)
    category_orders = def_category_orders

    # Specify the color sequence to use (we use a custom one for season so that the colours are intuitive)
    # TODO: Allow continuous colour sequences to be passed
    if color_discrete_sequence is None:
        if color is not None and "season" in color:
            color_discrete_sequence = ["green", "red", "orange", "blue"]
        elif list(aggregate.keys())[0] is not None and "season" in list(aggregate.keys()):
            color_discrete_sequence = ["green", "red", "orange", "blue"]
        else:
            color_discrete_sequence = px.colors.qualitative.G10

    if title is None:
        title = create_title(title_start, filters, line_group)

    # Plotly struggles to do splines for more than 20 or so curves, so revert to line_shape = linear and do
    # interpolation before hand
    orig_line_shape = line_shape
    columns = [col for col in [color, line_group, line_dash] if col]
    if len(columns) > 0:
        groups = list(filtered_data.groupby(columns).groups.keys())
    else:
        groups = []
    grp_length = len(groups)
    if grp_length > 20 and line_shape == "spline":
        line_shape = "linear"
        grouped_data = spline_interp(grouped_data, value_col, groups, columns)

    tick_text = list(range(0, 24))
    if text_noon:
        tick_text[0] = "Midnight"
        tick_text[12] = "Noon"

    if mode == "polar":
        # Default to 800x800 unless size is manually specified
        if "width" not in kwargs.keys() and "height" not in kwargs.keys():
            kwargs["width"] = 800
            kwargs["height"] = 800

        fig = px.line_polar(
            grouped_data,
            theta="degrees",
            r=value_col,
            line_group=line_group,
            color=color,
            line_dash=line_dash,
            line_close=True,
            line_shape=line_shape,
            category_orders=category_orders,
            title=title,
            color_discrete_sequence=color_discrete_sequence,
            **kwargs,
        )
        # Calculate the tickmarks for 24 hour clock
        fig.update_polars(
            angularaxis_tickvals=np.array(range(0, 360, int(360 / 24))),
            angularaxis_ticktext=tick_text,
        )
    else:
        # Default to 800x600 unless size is manually specified
        if "width" not in kwargs.keys() and "height" not in kwargs.keys():
            kwargs["width"] = 800
            kwargs["height"] = 600
        fig = px.line(
            grouped_data,
            x="degrees",
            y=value_col,
            line_group=line_group,
            color=color,
            line_dash=line_dash,
            line_shape=line_shape,
            category_orders=category_orders,
            title=title,
            color_discrete_sequence=color_discrete_sequence,
            **kwargs,
        )
        # Calculate the tickmarks for 24 hour clock
        fig.update_layout(
            xaxis_tickvals=np.array(range(0, 360, int(360 / 24))),
            xaxis_ticktext=tick_text,
        )

    # If there are a lot of lines, make them smaller and slightly transparent
    if grp_length > 12:
        fig.update_traces(line_width=0.5)
        fig.update_traces(opacity=0.7)
    elif grp_length <= 8:
        fig.update_traces(line_width=3)

    # Plot the averages (if required)
    if list(aggregate.keys())[0] is not None:
        fig = plot_averages(
            fig,
            filtered_data,
            value_col,
            aggregate,
            color,
            orig_line_shape,
            color_discrete_sequence,
            category_orders,
            mode,
        )

    if show:
        fig.show()
    return fig
