def make_candlestick(ohlc_data, width: int = None, height: int = 20) -> str:
    """
    Returns a multi-line candlestick chart (as a string) for a list of OHLC data.
    Handles dynamic width and height safely.
    
    Parameters:
        ohlc_data : list of [timestamp, open, high, low, close]
        width     : number of candles to display (auto-fallback if None)
        height    : number of rows for price levels
    """

    # fallback values
    width = width or 90
    height = height or 20

    n_candles = len(ohlc_data)
    if n_candles == 0:
        return "[No OHLC data]"

    # if too many candles, sample them evenly
    if n_candles > width:
        step = max(1, n_candles // width)
        ohlc_data = ohlc_data[::step]
    else:
        width = n_candles  # fit to actual data if fewer points

    lows = [l for _, _, _, l, _ in ohlc_data]
    highs = [h for _, _, h, _, _ in ohlc_data]
    min_price = min(lows)
    max_price = max(highs)
    price_step = (max_price - min_price) / max(height - 1, 1)

    # create empty grid
    grid = [[" " for _ in range(len(ohlc_data))] for _ in range(height)]

    # draw each candle
    for col, (_, o, h, l, c) in enumerate(ohlc_data):
        def row_index(p): 
            return int((p - min_price) / price_step)

        low_row, high_row, open_row, close_row = row_index(l), row_index(h), row_index(o), row_index(c)

        # vertical line for high-low
        for r in range(low_row, high_row + 1):
            grid[height - 1 - r][col] = "│"

        # body of candle
        top = max(open_row, close_row)
        bottom = min(open_row, close_row)
        for r in range(bottom, top + 1):
            grid[height - 1 - r][col] = "█" if c >= o else "░"

    # add price labels
    chart_lines = []
    for i, row in enumerate(grid):
        price_label = f"{min_price + price_step * (height - 1 - i):8.2f} | "
        chart_lines.append(price_label + "".join(row))

    # bottom axis
    chart_lines.append(" " * 10 + "-" * len(ohlc_data))
    chart_lines.append(" " * 10 + "".join(f"{i%10}" for i in range(len(ohlc_data))))

    return "\n".join(chart_lines)