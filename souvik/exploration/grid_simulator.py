from Data import Data
from tqdm import tqdm
import pandas as pd

class GridSimulator:

    def __init__(
            self,
            name: str,
            df: pd.DataFrame,
            instruments: str,
            ticker: str,
            init_bal: float,
            init_trade_size: int,
            grid_pips: int,
            sl_grid_count: int,
            stop_loss_type: str,
            margin_sl_percent: float,
            sizing: str,
            cash_out_factor: float):
        
        self.name = name
        self.tp_pips = grid_pips
        self.sl_pips = grid_pips * sl_grid_count
        self.sizing_ratio = init_trade_size / init_bal
        self.stop_loss_type = stop_loss_type
        self.margin_sl_percent = margin_sl_percent
        self.sizing = sizing
        self.cash_out_factor = cash_out_factor

        self.d = Data(
            source=df.copy(),
            ticker=ticker,
            cols=['time', 'mid_c', 'bid_c', 'ask_c'],
            instruments=instruments
        )

        add_cols = dict(
            open_longs=object,
            open_shorts=object,
            closed_longs=object,
            closed_shorts=object,
            trade_type=int, # (1 = ENTRY or TP, 0 = SL, -1 = MC (Margin Call) (MC & SL takes precedence over ENTRY or TP)
            cum_long_position=int,
            cum_short_position=int,
            unrealised_pnl=float,
            realised_pnl=float,
            ac_bal=float,
            margin_used=float,
            margin_closeout=float,
            cash_bal=float
        )

        self.d.prepare_fast_data(name=name, start=0, end=self.d.datalen, add_cols=add_cols)

    def run_sim(self):
        for i in tqdm(range(self.d.fdatalen), desc=" Simulating... "):
            print(self.name, i)

        return self.d.df[self.name].copy()
