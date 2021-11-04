from trality.indicator import rsi, crossover
import numpy as np 

@schedule(interval="1h", symbol="BTCUSDT")
def handler(state, data):
    rsi_open = rsi(data.select("open"), period=14)
    rsi_close = rsi(data.select("close"), period=14)
    rsi_open_close = np.concatenate((rsi_open,rsi_close), axis=0)
    rsi_cross = crossover(rsi_open_close)[0,:]
