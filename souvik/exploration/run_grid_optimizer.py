from grid_optimizer import GridOptimizer

data_path = '../data/'
out_path = 'D:/Trading/ml4t-data/grid/'
instruments = '../data/instruments.json'

checkpoint=0
counter=8001
start=0
end=5000
tickers=['EUR_USD']
frequency=['M5']
init_bal=[1000]
init_trade_size=[1000]
grid_pips=[10]
sl_grid_count=[50]
stop_loss_type=['margin_grid_count']
margin_sl_percent=[0.90]
sizing=['dynamic']
cash_out_factor=[1.1, 1.9]
inputs_file='inputs.8.csv'


if __name__ == '__main__':
    optim = GridOptimizer(
        checkpoint=checkpoint,
        counter=counter,
        start=start,
        end=end,
        tickers=tickers,
        frequency=frequency,
        init_bal=init_bal,      
        init_trade_size=init_trade_size,
        grid_pips=grid_pips,
        sl_grid_count=sl_grid_count,
        stop_loss_type=stop_loss_type,
        margin_sl_percent=margin_sl_percent,
        sizing=sizing,
        cash_out_factor=cash_out_factor,
        data_path=data_path,
        instruments=instruments,
        out_path=out_path,
        inputs_file=inputs_file
    )

    optim.run_optimizer()