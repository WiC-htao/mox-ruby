def get_clean_factor_and_forward_returns(
    factor,
    prices,
    groupby=None,
    binning_by_group=False,
    quantiles=5,
    bins=None,
    periods=(1, 5, 10),
    filter_zscore=20,
    groupby_labels=None,
    max_loss=0.35,
    zero_aware=False,
    cumulative_returns=True,
):
    """
    Formats the factor data, pricing data, and group mappings into a DataFrame
    that contains aligned MultiIndex indices of timestamp and asset. The
    returned data will be formatted to be suitable for Alphalens functions.

    It is safe to skip a call to this function and still make use of Alphalens
    functionalities as long as the factor data conforms to the format returned
    from get_clean_factor_and_forward_returns and documented here

    Parameters
    ----------
    factor : pd.Series - MultiIndex
        A MultiIndex Series indexed by timestamp (level 0) and asset
        (level 1), containing the values for a single alpha factor.
        ::
            -----------------------------------
                date    |    asset   |
            -----------------------------------
                        |   AAPL     |   0.5
                        -----------------------
                        |   BA       |  -1.1
                        -----------------------
            2014-01-01  |   CMG      |   1.7
                        -----------------------
                        |   DAL      |  -0.1
                        -----------------------
                        |   LULU     |   2.7
                        -----------------------

    prices : pd.DataFrame
        A wide form Pandas DataFrame indexed by timestamp with assets
        in the columns.
        Pricing data must span the factor analysis time period plus an
        additional buffer window that is greater than the maximum number
        of expected periods in the forward returns calculations.
        It is important to pass the correct pricing data in depending on
        what time of period your signal was generated so to avoid lookahead
        bias, or  delayed calculations.
        'Prices' must contain at least an entry for each timestamp/asset
        combination in 'factor'. This entry should reflect the buy price
        for the assets and usually it is the next available price after the
        factor is computed but it can also be a later price if the factor is
        meant to be traded later (e.g. if the factor is computed at market
        open but traded 1 hour after market open the price information should
        be 1 hour after market open).
        'Prices' must also contain entries for timestamps following each
        timestamp/asset combination in 'factor', as many more timestamps
        as the maximum value in 'periods'. The asset price after 'period'
        timestamps will be considered the sell price for that asset when
        computing 'period' forward returns.
        ::
            ----------------------------------------------------
                        | AAPL |  BA  |  CMG  |  DAL  |  LULU  |
            ----------------------------------------------------
               Date     |      |      |       |       |        |
            ----------------------------------------------------
            2014-01-01  |605.12| 24.58|  11.72| 54.43 |  37.14 |
            ----------------------------------------------------
            2014-01-02  |604.35| 22.23|  12.21| 52.78 |  33.63 |
            ----------------------------------------------------
            2014-01-03  |607.94| 21.68|  14.36| 53.94 |  29.37 |
            ----------------------------------------------------

    groupby : pd.Series - MultiIndex or dict
        Either A MultiIndex Series indexed by date and asset,
        containing the period wise group codes for each asset, or
        a dict of asset to group mappings. If a dict is passed,
        it is assumed that group mappings are unchanged for the
        entire time period of the passed factor data.
    binning_by_group : bool
        If True, compute quantile buckets separately for each group.
        This is useful when the factor values range vary considerably
        across gorups so that it is wise to make the binning group relative.
        You should probably enable this if the factor is intended
        to be analyzed for a group neutral portfolio
    quantiles : int or sequence[float]
        Number of equal-sized quantile buckets to use in factor bucketing.
        Alternately sequence of quantiles, allowing non-equal-sized buckets
        e.g. [0, .10, .5, .90, 1.] or [.05, .5, .95]
        Only one of 'quantiles' or 'bins' can be not-None
    bins : int or sequence[float]
        Number of equal-width (valuewise) bins to use in factor bucketing.
        Alternately sequence of bin edges allowing for non-uniform bin width
        e.g. [-4, -2, -0.5, 0, 10]
        Chooses the buckets to be evenly spaced according to the values
        themselves. Useful when the factor contains discrete values.
        Only one of 'quantiles' or 'bins' can be not-None
    periods : sequence[int]
        periods to compute forward returns on.
    filter_zscore : int or float, optional
        Sets forward returns greater than X standard deviations
        from the the mean to nan. Set it to 'None' to avoid filtering.
        Caution: this outlier filtering incorporates lookahead bias.
    groupby_labels : dict
        A dictionary keyed by group code with values corresponding
        to the display name for each group.
    max_loss : float, optional
        Maximum percentage (0.00 to 1.00) of factor data dropping allowed,
        computed comparing the number of items in the input factor index and
        the number of items in the output DataFrame index.
        Factor data can be partially dropped due to being flawed itself
        (e.g. NaNs), not having provided enough price data to compute
        forward returns for all factor values, or because it is not possible
        to perform binning.
        Set max_loss=0 to avoid Exceptions suppression.
    zero_aware : bool, optional
        If True, compute quantile buckets separately for positive and negative
        signal values. This is useful if your signal is centered and zero is
        the separation between long and short signals, respectively.
    cumulative_returns : bool, optional
        If True, forward returns columns will contain cumulative returns.
        Setting this to False is useful if you want to analyze how predictive
        a factor is for a single forward day.

    Returns
    -------
    merged_data : pd.DataFrame - MultiIndex
        A MultiIndex Series indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - forward returns column names follow  the format accepted by
          pd.Timedelta (e.g. '1D', '30m', '3h15m', '1D1h', etc)
        - 'date' index freq property (merged_data.index.levels[0].freq) will be
          set to a trading calendar (pandas DateOffset) inferred from the input
          data (see infer_trading_calendar for more details). This is currently
          used only in cumulative returns computation
        ::
           -------------------------------------------------------------------
                      |       | 1D  | 5D  | 10D  |factor|group|factor_quantile
           -------------------------------------------------------------------
               date   | asset |     |     |      |      |     |
           -------------------------------------------------------------------
                      | AAPL  | 0.09|-0.01|-0.079|  0.5 |  G1 |      3
                      --------------------------------------------------------
                      | BA    | 0.02| 0.06| 0.020| -1.1 |  G2 |      5
                      --------------------------------------------------------
           2014-01-01 | CMG   | 0.03| 0.09| 0.036|  1.7 |  G2 |      1
                      --------------------------------------------------------
                      | DAL   |-0.02|-0.06|-0.029| -0.1 |  G3 |      5
                      --------------------------------------------------------
                      | LULU  |-0.03| 0.05|-0.009|  2.7 |  G1 |      2
                      --------------------------------------------------------

    See Also
    --------
    utils.get_clean_factor
        For use when forward returns are already available.
    """
    forward_returns = compute_forward_returns(
        factor,
        prices,
        periods,
        filter_zscore,
        cumulative_returns,
    )

    factor_data = get_clean_factor(
        factor,
        forward_returns,
        groupby=groupby,
        groupby_labels=groupby_labels,
        quantiles=quantiles,
        bins=bins,
        binning_by_group=binning_by_group,
        max_loss=max_loss,
        zero_aware=zero_aware,
    )

    return factor_data


def infer_trading_calendar(factor_idx, prices_idx):
    """
    Infer the trading calendar from factor and price information.

    Parameters
    ----------
    factor_idx : pd.DatetimeIndex
        The factor datetimes for which we are computing the forward returns
    prices_idx : pd.DatetimeIndex
        The prices datetimes associated withthe factor data

    Returns
    -------
    calendar : pd.DateOffset
    """
    full_idx = factor_idx.union(prices_idx)

    traded_weekdays = []
    holidays = []

    days_of_the_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day, day_str in enumerate(days_of_the_week):

        weekday_mask = full_idx.dayofweek == day

        # drop days of the week that are not traded at all
        if not weekday_mask.any():
            continue
        traded_weekdays.append(day_str)

        # look for holidays
        used_weekdays = full_idx[weekday_mask].normalize()
        all_weekdays = pd.date_range(
            full_idx.min(), full_idx.max(), freq=CustomBusinessDay(weekmask=day_str)
        ).normalize()
        _holidays = all_weekdays.difference(used_weekdays)
        _holidays = [timestamp.date() for timestamp in _holidays]
        holidays.extend(_holidays)

    traded_weekdays = " ".join(traded_weekdays)
    return CustomBusinessDay(weekmask=traded_weekdays, holidays=holidays)


def compute_forward_returns(
    factor, prices, periods=(1, 5, 10), filter_zscore=None, cumulative_returns=True
):
    """
    Finds the N period forward returns (as percent change) for each asset
    provided.

    Parameters
    ----------
    factor : pd.Series - MultiIndex
        A MultiIndex Series indexed by timestamp (level 0) and asset
        (level 1), containing the values for a single alpha factor.

        - See full explanation in utils.get_clean_factor_and_forward_returns

    prices : pd.DataFrame
        Pricing data to use in forward price calculation.
        Assets as columns, dates as index. Pricing data must
        span the factor analysis time period plus an additional buffer window
        that is greater than the maximum number of expected periods
        in the forward returns calculations.
    periods : sequence[int]
        periods to compute forward returns on.
    filter_zscore : int or float, optional
        Sets forward returns greater than X standard deviations
        from the the mean to nan. Set it to 'None' to avoid filtering.
        Caution: this outlier filtering incorporates lookahead bias.
    cumulative_returns : bool, optional
        If True, forward returns columns will contain cumulative returns.
        Setting this to False is useful if you want to analyze how predictive
        a factor is for a single forward day.

    Returns
    -------
    forward_returns : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by timestamp (level 0) and asset
        (level 1), containing the forward returns for assets.
        Forward returns column names follow the format accepted by
        pd.Timedelta (e.g. '1D', '30m', '3h15m', '1D1h', etc).
        'date' index freq property (forward_returns.index.levels[0].freq)
        will be set to a trading calendar (pandas DateOffset) inferred
        from the input data (see infer_trading_calendar for more details).
    """

    factor_dateindex = factor.index.levels[0]

    freq = infer_trading_calendar(factor_dateindex, prices.index)

    factor_dateindex = factor_dateindex.intersection(prices.index)

    if len(factor_dateindex) == 0:
        raise ValueError(
            "Factor and prices indices don't match: make sure "
            "they have the same convention in terms of datetimes "
            "and symbol-names"
        )

    # chop prices down to only the assets we care about (= unique assets in
    # `factor`).  we could modify `prices` in place, but that might confuse
    # the caller.
    prices = prices.filter(items=factor.index.levels[1])

    raw_values_dict = {}
    column_list = []

    for period in sorted(periods):
        if cumulative_returns:
            returns = prices.pct_change(period)
        else:
            returns = prices.pct_change()

        forward_returns = returns.shift(-period).reindex(factor_dateindex)

        if filter_zscore is not None:
            mask = abs(forward_returns - forward_returns.mean()) > (
                filter_zscore * forward_returns.std()
            )
            forward_returns[mask] = np.nan

        #
        # Find the period length, which will be the column name. We'll test
        # several entries in order to find out the most likely period length
        # (in case the user passed inconsinstent data)
        #
        days_diffs = []
        for i in range(30):
            if i >= len(forward_returns.index):
                break
            p_idx = prices.index.get_loc(forward_returns.index[i])
            if p_idx is None or p_idx < 0 or (p_idx + period) >= len(prices.index):
                continue
            start = prices.index[p_idx]
            end = prices.index[p_idx + period]
            period_len = diff_custom_calendar_timedeltas(start, end, freq)
            days_diffs.append(period_len.components.days)

        delta_days = period_len.components.days - mode(days_diffs).mode[0]
        period_len -= pd.Timedelta(days=delta_days)
        label = timedelta_to_string(period_len)

        column_list.append(label)

        raw_values_dict[label] = np.concatenate(forward_returns.values)

    df = pd.DataFrame.from_dict(raw_values_dict)
    df.set_index(
        pd.MultiIndex.from_product(
            [factor_dateindex, prices.columns], names=["date", "asset"]
        ),
        inplace=True,
    )
    df = df.reindex(factor.index)

    # now set the columns correctly
    df = df[column_list]

    df.index.levels[0].freq = freq
    df.index.set_names(["date", "asset"], inplace=True)

    return df
