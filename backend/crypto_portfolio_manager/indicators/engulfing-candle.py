class EngulfingIndicator():
    """ 
    Checks for an engulfing candle for added confluence 
    """
    def __init__(self, data):
        self.position = None

    def on_data(self, data):
        if len(data) < 2:
            return "Hold"

        prev_open = data['open'].iloc[-2]
        prev_close = data['close'].iloc[-2]
        curr_open = data['open'].iloc[-1]
        curr_close = data['close'].iloc[-1]

        # Bullish Engulfing
        if prev_close < prev_open and curr_close > curr_open and curr_close > prev_open and curr_open < prev_close and self.position is None:
            return "Long"
        # Bearish Engulfing
        elif prev_close > prev_open and curr_close < curr_open and curr_close < prev_open and curr_open > prev_close and self.position is None:
            return "Short"
        else:
            return "Hold"