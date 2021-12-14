'''
Implementation of the super trend indicator
https://bonfida.medium.com/introduction-of-super-trend-strategy-3b8c420abbd0

The indicator changes state when a closing price crosses a price threshold
The price threshold is set using the ATR and multipler.
The treshold moves only in the direction of the trend unless it is broken.
'''

ATR_PERIOD = 24
ATR_MULTIPLIER = 3.0

def initialize(state):
    state.super_trend = 0   # current trend direction
    state.limit = 0         # current threshold price

''' The update function for the super trend indicator '''
def super_trend(state, price, atr, multipler) :

    # calculate the new trend reversal price
    limit = -state.super_trend * multipler * atr + price

    # set the state the first time that the bot is run
    if state.super_trend == 0:
        state.limit = limit

    # check if the trend has changed
    if price >= state.limit and state.super_trend != 1:
        state.super_trend = 1
        # reset reversal price
        state.limit = -state.super_trend * multipler * atr + price
    elif price < state.limit and state.super_trend != -1:
        state.super_trend = -1
        # reset reversal price
        state.limit = -state.super_trend * multipler * atr + price
    else:
        # only ratchet limit price if its going in the trends direction
        if state.super_trend == +1:
            state.limit = max(state.limit, limit)
        elif state.super_trend == -1:
            state.limit = min(state.limit, limit)

    # return the current trend reversal price and the trenc direction
    return state.limit, state.super_trend


@schedule(interval="1h", symbol="BTCUSDT")
def handler(state, data):
    
    # initalize super trend indicator with historic data the first time the bot is run
    if state.super_trend == 0:
         atr = data.atr(ATR_PERIOD)
         for p, v in zip(data.select("close"), atr):
             super_trend(state, p, v, ATR_MULTIPLIER)

    # update super trend indicator
    level, direction = super_trend(state, data.close_last, data.atr(ATR_PERIOD)[-1], ATR_MULTIPLIER)

    with PlotScope.root(data.symbol):
        plot_line("level", level)
    plot_line("direction", direction, data.symbol)
