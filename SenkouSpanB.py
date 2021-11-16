def initialize(state):
    state.data5run = 0
    state.spanindex = []
    state.highhigh = {}
    state.lowlow = {}   
    state.spanbcur = {}

@schedule(interval="5m", symbol="XDGUSD", window_size=200)
def data5handler(state, data):

    spanbPeriod = range(1, 52+1)
    spanIndex = state.spanindex

    state.highhigh = data.high_last
    state.lowlow = data.low_last

###Calculate Span B
    for i in spanbPeriod:
        high = data['high'][i *-1]
        if (high > state.highhigh):
            state.highhigh = high;

    for i in spanbPeriod:    
        low = data['low'][i *-1]
        if (low < state.lowlow):
            state.lowlow = low;
    
    else:
        spanb = (state.lowlow + state.highhigh) / 2

    spanIndex.append(spanb)
 ###Plot Span B 
    if state.data5run > 26:
        spanIndex0 = spanIndex[0]
        del spanIndex[0];
        with PlotScope.root(data.symbol):
            plot_line ("spanB", spanIndex0)

    if state.data5run <= 200:
        state.data5run += 1

    state.spanindex = spanIndex
    state.spanbcur = spanIndex[0]
