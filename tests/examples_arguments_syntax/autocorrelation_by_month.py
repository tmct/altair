"""
Autocorrelation Decay by Month
==============================
This example uses the correlation transform to compute the autocorrelation
of Seattle daily maximum temperature at lags of 1, 3, and 6 days, broken
out by month. Day-to-day temperature persistence is positive year-round
but decays with lag, more steeply in summer than winter.
"""
# category: uncertainties and trends

import altair as alt
from altair.datasets import data

source = data.seattle_weather()

alt.Chart(source, title="Autocorrelation of daily max temperature").transform_window(
    window=[
        alt.WindowFieldDef(op="lag", field="temp_max", param=1, **{"as": "temp_lag_1d"}),
        alt.WindowFieldDef(op="lag", field="temp_max", param=3, **{"as": "temp_lag_3d"}),
        alt.WindowFieldDef(op="lag", field="temp_max", param=6, **{"as": "temp_lag_6d"}),
    ],
    sort=[alt.SortField("date")],
).transform_filter(
    "datum.temp_lag_1d != null && datum.temp_lag_3d != null && datum.temp_lag_6d != null",
).transform_calculate(
    month="month(datum.date) + 1",
).transform_fold(
    fold=["temp_lag_1d", "temp_lag_3d", "temp_lag_6d"],
    as_=["lag", "temp_lagged"],
).transform_correlation(
    correlation="temp_max",
    on="temp_lagged",
    groupby=["month", "lag"],
    as_=["corr"],
).mark_line(point=True).encode(
    x=alt.X(
        "month:O",
        title="Month",
        axis=alt.Axis(
            labelExpr=(
                "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']"
                "[datum.value - 1]"
            ),
        ),
    ),
    y=alt.Y(
        "corr:Q",
        title="Autocorrelation of temp_max",
        scale=alt.Scale(domain=[0, 1]),
    ),
    color=alt.Color(
        "lag:N",
        title="Lag",
        sort=["temp_lag_1d", "temp_lag_3d", "temp_lag_6d"],
        legend=alt.Legend(
            labelExpr=(
                "{'temp_lag_1d':'1 day','temp_lag_3d':'3 days','temp_lag_6d':'6 days'}"
                "[datum.value]"
            ),
        ),
    ),
)
