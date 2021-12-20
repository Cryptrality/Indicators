def rvi(data, state, period):

    numerator_list = []
    denominator_list = []
    period = (period * -1) + -1
    period_range = list(range(-1, period , -1))

    for i in period_range:
        a = data.close[-1 * i] - data.open[-1 * i] 
        b = data.close[-2 * i] - data.open[-2 * i]
        c = data.close[-3 * i] - data.open[-3 * i]
        d = data.close[-4 * i] - data.open[-4 * i]
        numerator_list.append((a + (2*b) + (2*c) + d) / 6)
        e = data.high[-1 * i] - data.low[-1 * i]
        f = data.high[-2 * i] - data.low[-2 * i]
        g = data.high[-3 * i] - data.low[-3 * i]
        h = data.high[-4 * i] - data.low[-4 * i]
        denominator_list.append((e + (2*f) + (2*g) + h) / 6)
    numeraator_sma = sum(numerator_list) / len(numerator_list)
    denominator_sma = sum(denominator_list) / len(denominator_list)
    rvi_line = numeraator_sma / denominator_sma
    state.rvi_sig.insert(0, rvi_line)

    if len(state.rvi_sig) > 4:
        del state.rvi_sig[-1]
        rvi_sig = sum(state.rvi_sig) / len(state.rvi_sig)
        with PlotScope.group("RVI", data.symbol):
            plot_line("RVI Signal", rvi_sig)
    
    with PlotScope.group("RVI", data.symbol):
        plot_line("RVI Line", rvi_line)

    return rvi_line, rvi_sig
