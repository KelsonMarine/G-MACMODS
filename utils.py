import numpy as np
import pandas as pd


def offset_data_year(df, num_years):
    df.index += pd.DateOffset(years=num_years)
    return df

def interpolate_dataframe(df: pd.DataFrame, times: pd.DatetimeIndex):
    idx: pd.DatetimeIndex = df.index
    first_time = times[0]

    # if the last given time is before the first desired time, shift everything
    # forward by some years
    if idx[-1] < first_time:
        # shift so it at least overlaps
        num_years = times[0].year - idx[0].year
        df.index += pd.DateOffset(years=num_years)

    # if the first given time is greater than the last desired time, shift
    # everything backwards by some years
    if idx[0] > times[-1]:
        num_years = idx[-1].year - times[-1].year
        df.index -= pd.DateOffset(years=num_years)

    # Shift data backwards by one year and concatenate it with itself to create
    # cyclic data
    while df.index[0] > times[0]:
        back_shift = df.index - pd.DateOffset(years=1)
        mask = back_shift < df.index[0]
        extra_data = pd.Series(df[mask].values, back_shift[mask])
        df = pd.concat([extra_data, df])

    # Shift data forwards by one year and concatenate it with itself to create
    # cyclic data
    while df.index[-1] < times[-1]:
        forward_shift = df.index + pd.DateOffset(years=1)
        mask = forward_shift > df.index[-1]
        extra_data = pd.Series(df[mask].values, forward_shift[mask])
        df = pd.concat([df, extra_data])

    idx = df.index

    desired_times = times - first_time
    given_times = idx - first_time

    new_values = np.interp(desired_times.values.astype(np.float64), given_times.values.astype(np.float64), df.values)
    return new_values


def build_forcing(forcing_index, data):
    N = len(forcing_index)
    new_data = {}
    for key, value in data.items():

        if isinstance(value, (int, float)):
            new_data[key] = np.zeros(N) + value
        elif isinstance(value, pd.DataFrame):
            new_data[key] = interpolate_dataframe(value[value.columns[0]], forcing_index)
        elif isinstance(value, pd.Series):
            new_data[key] = interpolate_dataframe(value, forcing_index)
        else:
            new_data[key] = value

    return pd.DataFrame(new_data, index=forcing_index)