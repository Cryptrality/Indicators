__author__ = "Spacecarl#0439 / https://github.com/SpaceCarl" 

vwapPeriod = range(1, 10+1)
    vwapIndex = []
    volumeIndex = []
    vwapSum = 0
    volumeSum = 0


    for i in vwapPeriod:
        price = ((data['high'][i*-1] + data['low'][i*-1] + data['close'][i*-1]) / 3) * data['volume'][i*-1]
        vwapIndex.append(price)
        volume = data['volume'][i*-1]
        volumeIndex.append(volume)

    for i in range(0, len(vwapIndex)):
        vwapSum = vwapSum + vwapIndex[i];

    for i in range(0, len(volumeIndex)):
        volumeSum = volumeSum + volumeIndex[i];


    state.vwap = vwapSum / volumeSum

    with PlotScope.root(data.symbol):
        plot_line ("VWAP", state.vwap)
