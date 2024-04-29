from grid_optimizer import GridOptimizer

data_path = '../data/'
out_path = 'D:/Trading/ml4t-data/grid/'
instruments = "../data/instruments.json"

# dummyrun = False
# checkpoint=1359
# counter=1126
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[20, 30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30, 50]
# stop_loss_type=['grid_count']
# margin_sl_percent=[0.90]
# sizing=['dynamic', 'static']
# cash_out_factor=[None, 1.1, 1.25, 1.5, 2.0, 3.0]
# inputs_file='inputs.1b.csv'

# dummyrun = False
# checkpoint=2305
# counter=2126
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[1.1]
# inputs_file='inputs.2d.csv'

# dummyrun = False
# checkpoint=3305
# counter=3126
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[1.25]
# inputs_file='inputs.3d.csv'

# dummyrun = False
# checkpoint=4305
# counter=4126
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[1.5]
# inputs_file='inputs.4d.csv'

# dummyrun = False
# checkpoint=5026
# counter=5000
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[10, 20, 30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[1.75]
# inputs_file='inputs.5a.csv'

# dummyrun = False
# checkpoint=6025
# counter=6000
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[10, 20, 30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[2.0]
# inputs_file='inputs.6a.csv'

# dummyrun = False
# checkpoint=7024
# counter=7000
# start=None
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[10, 20, 30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[3.0]
# inputs_file='inputs.7a.csv'

# dummyrun = False
# checkpoint=8247
# counter=8000
# start=None  
# end=None
# records=['events']
# tickers=['EUR_USD']
# frequency=['M5']
# init_bal=[1000]
# init_trade_size=[1000]
# grid_pips=[10, 20, 30, 40, 60]
# sl_grid_count=[5, 10, 15, 20, 30]
# stop_loss_type=['grid_count_on_margin', 'oldest_on_margin']
# margin_sl_percent=[0.90, 0.80, 0.70]
# sizing=['dynamic', 'static']
# cash_out_factor=[None]
# inputs_file='inputs.8b.csv'

dummyrun = False
checkpoint=0
counter=10000
start=0  
end=10000
records=['events']
tickers=['EUR_USD']
frequency=['M5']
init_bal=[1000]
init_trade_size=[1000]
grid_pips=[10, 20]
sl_grid_count=[5, 10]
stop_loss_type=['grid_count', 'grid_count_on_margin', 'oldest_on_margin']
margin_sl_percent=[0.90]
sizing=['dynamic', 'static']
cash_out_factor=[None]
cover_stopped_loss = [True]
inputs_file='inputs.10.csv'


if __name__ == '__main__':
    optim = GridOptimizer(
        checkpoint=checkpoint,
        counter=counter,
        start=start,
        end=end,
        records=records,
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
        cover_stopped_loss=cover_stopped_loss,
        data_path=data_path,
        instruments=instruments,
        out_path=out_path,
        inputs_file=inputs_file,
        dummyrun=dummyrun
    )

    print(optim)

    optim.run_optimizer()