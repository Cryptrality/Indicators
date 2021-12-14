'''
This script is a demonstration of different types of volatility calculation
And how they can be used to determine relative value.
'''

import numpy as np

def rogers_satchell_volatility(data, periods):
    '''Rogers-Satchell is an estimator for measuring the volatility of securities
    with an average return not equal to zero.'''

    opens = data.select("open")[-periods:]
    highs = data.select("high")[-periods:]
    lows = data.select("low")[-periods:]
    closes = data.select("close")[-periods:]

    v1 = np.log(np.divide(highs, closes))
    v2 = np.log(np.divide(highs, opens))
    v3 = np.log(np.divide(lows, closes))
    v4 = np.log(np.divide(lows, closes))

    return  np.sqrt(np.sum(np.add(np.multiply(v1,v2),np.multiply(v3,v4))) / periods)

def parkinson_volatility(data, periods):
    '''Parkinson volatility is a volatility measure that uses the high and low price of the day. '''
    highs = data.select("high")[-periods:]
    lows = data.select("low")[-periods:]

    total = np.sum(np.square(np.log(np.divide(highs, lows))))
    scale = 1.0/(4*periods*np.log(2))

    return np.sqrt(scale * total)

def garman_klass_volatility(data, periods):
    ''' Garman Klass is a volatility estimator that incorporates open, low, high, and close prices of a security '''

    opens = data.select("open")[-periods:]
    highs = data.select("high")[-periods:]
    lows = data.select("low")[-periods:]
    closes = data.select("close")[-periods:]

    v1 = np.square(np.log(np.divide(highs, lows)))
    v2 = np.square(np.log(np.divide(closes, opens)))

    f1 = ((2*np.log(2))-1.0)/periods
    f2 = 1.0/(2*periods)

    return np.sqrt(f2 * np.sum(np.subtract(v1, f1*v2)))


def initialize(state):
    pass

PERIOD = 24
MULTIPLIER = 2.0

@schedule(interval="1h", symbol="BTCUSDT")
def handler(state, data):

    stddev = data.stddev(PERIOD)
    atr = data.atr(PERIOD)

    plot_line("atr_perc", atr[-1]/data.close_last, data.symbol)

    rs_vol = rogers_satchell_volatility(data, PERIOD)
    plot_line("rs", rs_vol, data.symbol)

    p_vol = parkinson_volatility(data, PERIOD)
    plot_line("pv", p_vol, data.symbol)

    gk_vol = garman_klass_volatility(data, PERIOD)
    plot_line("gkv", gk_vol, data.symbol)

    ema_price= data.ema(PERIOD).last
    with PlotScope.root(data.symbol):
        # bollinger bands stdev
        plot_line("bollinger_up", ema_price+stddev[-1]*MULTIPLIER)
        plot_line("bollinger_dn", ema_price-stddev[-1]*MULTIPLIER)

        # keltner channels with ATR
        plot_line("keltner_up", ema_price+atr[-1]*MULTIPLIER)
        plot_line("keltner_dn", ema_price-atr[-1]*MULTIPLIER)

        # parkinson volatility bands
        plot_line("p_up", ema_price*(1+p_vol*MULTIPLIER))
        plot_line("p_dn", ema_price*(1-p_vol*MULTIPLIER))

        # rogers satchell volatility bands
        plot_line("rs_up", ema_price*(1+rs_vol*MULTIPLIER))
        plot_line("rs_dn", ema_price*(1-rs_vol*MULTIPLIER))

        # garman klass volatility bands
        plot_line("gk_up", ema_price*(1+gk_vol*MULTIPLIER))
        plot_line("gk_dn", ema_price*(1-gk_vol*MULTIPLIER))