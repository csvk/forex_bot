from data import Data
from tqdm import tqdm
import pandas as pd


class GridSimulator:

    EVENT_TP, EVENT_SL, EVENT_MC, EVENT_ENTRY = 'TP', 'SL', 'MC', 'ENT'
    EVENT_CASH_IN, EVENT_CASH_OUT =  'CI', 'CO'
    SIZE, ENTRY, TP, SL = 0, 1, 2, 3
    EXIT, PIPS = 2, 3
    MC_PERCENT = 0.50

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
        self.init_bal = init_bal
        self.init_trade_size = init_trade_size
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
            events=object,
            cum_long_position=int,
            cum_short_position=int,
            unrealised_pnl=float,
            realised_pnl=float,
            ac_bal=float,
            net_bal=float,
            margin_used=float,
            cash_bal=float
        )

        self.d.prepare_fast_data(name=name, start=0, end=self.d.datalen, add_cols=add_cols)

    def cum_long_position(self):
        open_longs = self.d.fdata('open_longs', self.i).copy() if type(self.d.fdata('open_longs', self.i)) == dict else dict()
        cum_long_position = 0
        for _, trade in open_longs.items():
            cum_long_position = cum_long_position + trade[self.SIZE]
        return cum_long_position

    def cum_short_position(self):
        open_shorts = self.d.fdata('open_shorts', self.i).copy() if type(self.d.fdata('open_shorts', self.i)) == dict else dict()
        cum_short_position = 0
        for _, trade in open_shorts.items():
            cum_short_position = cum_short_position + trade[self.SIZE]
        return cum_short_position

    def unrealised_pnl(self):
        open_longs = self.d.fdata('open_longs', self.i).copy() if type(self.d.fdata('open_longs', self.i)) == dict else dict()
        open_shorts = self.d.fdata('open_shorts', self.i).copy() if type(self.d.fdata('open_shorts', self.i)) == dict else dict()
        pnl = 0
        for _, trade in open_longs.items():
            pnl = pnl + trade[self.SIZE] * (self.d.fdata('mid_c', self.i) - trade[self.ENTRY])
        for _, trade in open_shorts.items():
            pnl = pnl + trade[self.SIZE] * (trade[self.ENTRY] - self.d.fdata('mid_c', self.i))
        return round(pnl, 2)
    
    def realised_pnl(self):
        closed_longs = self.d.fdata('closed_longs', self.i).copy() if type(self.d.fdata('closed_longs', self.i)) == dict else dict()
        closed_shorts = self.d.fdata('closed_shorts', self.i).copy() if type(self.d.fdata('closed_shorts', self.i)) == dict else dict()
        pnl = 0
        for _, trade in closed_longs.items():
            pnl = pnl + trade[self.SIZE] * (trade[self.EXIT] - trade[self.ENTRY])
        for _, trade in closed_shorts.items():
            pnl = pnl + trade[self.SIZE] * (trade[self.ENTRY] - trade[self.EXIT])
        return round(pnl, 2)
    
    def cash_transfer(self):
        net_bal, _ = self.current_ac_values()
        if self.cash_out_factor is not None:
            self.d.update_fdata('cash_bal', self.i, self.d.fdata('ac_bal', self.i-1))
            cash_out_threshold = self.init_bal * self.cash_out_factor
            events = self.d.fdata('events', self.i) if type(self.d.fdata('events', self.i)) == list else list()
            stop_loss = self.EVENT_SL in events or self.EVENT_MC in events
            # Cash out / withdraw
            if net_bal > cash_out_threshold:
                cash_out = net_bal - cash_out_threshold
                self.d.update_fdata('ac_bal', self.i, round(self.d.fdata('ac_bal', self.i) - cash_out, 2))
                self.d.update_fdata('cash_bal', self.i, round(self.d.fdata('cash_bal', self.i) + cash_out, 2))
                self.update_temp_ac_values()
                self.update_events(self.EVENT_CASH_OUT)
                return cash_out
            # Deposit money into a/c when net_bal < cash_out_threshold
            elif stop_loss and net_bal < cash_out_threshold:
                cash_in = min(cash_out_threshold - net_bal, self.d.fdata('cash_bal', self.i-1))
                if cash_in > 0:
                    self.d.update_fdata('ac_bal', self.i, round(self.d.fdata('ac_bal', self.i) + cash_in, 2))
                    self.d.update_fdata('cash_bal', self.i, round(self.d.fdata('cash_bal', self.i) - cash_in, 2))
                    self.update_temp_ac_values()
                    self.update_events(self.EVENT_CASH_IN)    
                    return cash_in  

    def current_ac_values(self):
        ac_bal = self.d.fdata('ac_bal', self.i-1) + self.d.fdata('realised_pnl', self.i)
        margin_used = (self.d.fdata('cum_long_position', self.i) + 
                       self.d.fdata('cum_short_position', self.i)) * float(self.d.ticker['marginRate'])
        net_bal = ac_bal + self.d.fdata('unrealised_pnl', self.i)
        return net_bal, margin_used      

    def update_temp_ac_values(self, init: bool=False):
        if init:
            self.d.update_fdata('open_longs', self.i, self.d.fdata('open_longs', self.i-1))
            self.d.update_fdata('open_shorts', self.i, self.d.fdata('open_shorts', self.i-1))
            self.d.update_fdata('cum_long_position', self.i, self.d.fdata('cum_long_position', self.i-1))
            self.d.update_fdata('cum_short_position', self.i, self.d.fdata('cum_short_position', self.i-1))
        else:
            self.d.update_fdata('cum_long_position', self.i, self.cum_long_position())
            self.d.update_fdata('cum_short_position', self.i, self.cum_short_position())
        
        self.d.update_fdata('unrealised_pnl', self.i, self.unrealised_pnl())
        self.d.update_fdata('realised_pnl', self.i, self.realised_pnl())

    def update_ac_values(self):
        self.d.update_fdata('cum_long_position', self.i, self.cum_long_position())
        self.d.update_fdata('cum_short_position', self.i, self.cum_short_position())
        self.d.update_fdata('unrealised_pnl', self.i, self.unrealised_pnl())
        self.d.update_fdata('realised_pnl', self.i, self.realised_pnl())
        
        # First candle
        if self.i == 0:               
            self.d.update_fdata('ac_bal', self.i, self.init_bal)
        # Subsequent candles
        else:
            events = self.d.fdata('events', self.i) if type(self.d.fdata('events', self.i)) == list else list()
            cash_transfer = self.EVENT_CASH_IN in events or self.EVENT_CASH_OUT in events
            ac_bal = self.d.fdata('ac_bal', self.i) if cash_transfer else self.d.fdata('ac_bal', self.i-1)
            self.d.update_fdata('ac_bal', self.i, round(ac_bal + self.d.fdata('realised_pnl', self.i), 2))

        self.d.update_fdata('net_bal', self.i, round(self.d.fdata('ac_bal', self.i) + self.d.fdata('unrealised_pnl', self.i), 2))
        self.d.update_fdata('margin_used', self.i, \
                            round((self.d.fdata('cum_long_position', self.i) + 
                                   self.d.fdata('cum_short_position', self.i)) * float(self.d.ticker['marginRate']), 2))
    
    def dynamic_trade_size(self):
        net_bal, _ = self.current_ac_values()
        print(self.i, net_bal)
        return int(net_bal * self.sizing_ratio)   
    
    def update_events(self, event):
        events = self.d.fdata('events', self.i).copy() if type(self.d.fdata('events', self.i)) == list else list()
        events.append(event)
        self.d.update_fdata('events', self.i, events)

    def close_long(self, trade_no: int):
        # Remove from open longs
        open_longs = self.d.fdata('open_longs',  self.i).copy()
        closing_long = open_longs[trade_no]
        del open_longs[trade_no]
        self.d.update_fdata('open_longs', self.i, open_longs)

        # Append to closed longs
        pips = (self.d.fdata('ask_c',  self.i) - closing_long[self.ENTRY]) * pow(10, -self.d.ticker['pipLocation'])
        closed_longs = self.d.fdata('closed_longs',  self.i).copy() if type(self.d.fdata('closed_longs',  self.i)) == dict else dict()
        closed_longs[trade_no] = (closing_long[self.SIZE], closing_long[self.ENTRY], self.d.fdata('bid_c',  self.i), round(pips, 1)) # (SIZE, ENTRY, EXIT, PIPS)

        self.d.update_fdata('closed_longs', self.i, closed_longs)

    def close_short(self, trade_no: int):
        # Remove from open shorts
        open_shorts = self.d.fdata('open_shorts',  self.i).copy()
        closing_short = open_shorts[trade_no]
        del open_shorts[trade_no]
        self.d.update_fdata('open_shorts', self.i, open_shorts)

        # Append to closed shorts
        pips = (closing_short[self.ENTRY] - self.d.fdata('bid_c',  self.i)) * pow(10, -self.d.ticker['pipLocation'])
        closed_shorts = self.d.fdata('closed_shorts',  self.i).copy() if type(self.d.fdata('closed_shorts',  self.i)) == dict else dict()
        closed_shorts[trade_no] = (closing_short[self.SIZE], closing_short[self.ENTRY], self.d.fdata('ask_c',  self.i), round(pips, 1)) # (SIZE, ENTRY, EXIT, PIPS)

        self.d.update_fdata('closed_shorts', self.i, closed_shorts)
    
    def entry(self):
        if self.d.fdata('mid_c', self.i) >= self.next_up_grid or self.d.fdata('mid_c', self.i) <= self.next_down_grid:
            self.next_up_grid = self.d.fdata('mid_c', self.i) + self.tp_pips * pow(10, self.d.ticker['pipLocation'])
            self.next_down_grid = self.d.fdata('mid_c', self.i) - self.tp_pips * pow(10, self.d.ticker['pipLocation'])

            long_sl = self.d.fdata('mid_c', self.i) - self.sl_pips * pow(10, self.d.ticker['pipLocation'])
            short_sl = self.d.fdata('mid_c', self.i) + self.sl_pips * pow(10, self.d.ticker['pipLocation'])

            if self.i == 0:
                trade_size = self.init_trade_size
            else:
                trade_size = self.dynamic_trade_size() if self.sizing == 'dynamic' else self.init_trade_size

            open_longs = self.d.fdata('open_longs', self.i).copy() if type(self.d.fdata('open_longs', self.i)) == dict else dict()
            open_shorts = self.d.fdata('open_shorts', self.i).copy() if type(self.d.fdata('open_shorts', self.i)) == dict else dict()
            
            required_margin = round(trade_size * float(self.d.ticker['marginRate']) * 2, 2)
            net_bal, margin_used = self.current_ac_values()
            if self.i == 0 or (self.i > 0 and net_bal >= (required_margin + margin_used) * self.MC_PERCENT):
                self.trade_no = self.trade_no + 1
                open_longs[self.trade_no] = (trade_size, self.d.fdata('ask_c', self.i), self.next_up_grid, long_sl) # (SIZE, ENTRY, TP, SL)
                self.d.update_fdata('open_longs', self.i, open_longs)
                open_shorts[self.trade_no] = (trade_size, self.d.fdata('bid_c', self.i), self.next_down_grid, short_sl) # (SIZE, ENTRY, TP, SL)
                self.d.update_fdata('open_shorts', self.i, open_shorts)
                
                self.update_temp_ac_values()
                self.update_events(self.EVENT_ENTRY)
                # self.update_ac_values()

    def take_profit(self):     
        traded = False
        # Close long positions take profit
        open_longs = self.d.fdata('open_longs', self.i).copy() if type(self.d.fdata('open_longs', self.i)) == dict else dict()
        for trade_no, trade in open_longs.items():
            if self.d.fdata('mid_c', self.i) >= trade[self.TP]:
                self.close_long(trade_no)
                traded = True

        # Close short positions take profit
        open_shorts = self.d.fdata('open_shorts', self.i).copy() if type(self.d.fdata('open_shorts', self.i)) == dict else dict()
        for trade_no, trade in open_shorts.items():
            if self.d.fdata('mid_c', self.i) <= trade[self.TP]:
                self.close_short(trade_no)
                traded = True

        if traded:
            self.update_temp_ac_values()
            self.update_events(self.EVENT_TP)
            # self.update_ac_values()    

    def stop_loss_grid_count(self):
        traded = False
        # Close long positions stop loss
        open_longs = self.d.fdata('open_longs', self.i).copy()
        for trade_no, trade in open_longs.items():
            if self.d.fdata('mid_c', self.i) <= trade[self.SL]:
                self.close_long(trade_no)
                traded = True

        # Close short positions stop loss
        open_shorts = self.d.fdata('open_shorts', self.i).copy()
        for trade_no, trade in open_shorts.items():
            if self.d.fdata('mid_c', self.i) >= trade[self.SL]:
                self.close_short(trade_no)
                traded = True

        return traded

    def stop_loss_grid_count_on_margin(self, net_bal: float, margin_used: float):
        traded = False
        if net_bal < margin_used * self.margin_sl_percent:
            traded = self.stop_loss_grid_count()
        return traded

    def stop_loss_oldest_on_margin(self, net_bal: float, margin_used: float):
        traded = False
        if net_bal < margin_used * self.margin_sl_percent:
            longs = list(self.d.fdata('open_longs', self.i).keys())
            shorts = list(self.d.fdata('open_shorts', self.i).keys())
            oldest_long = longs[0] if len(longs) > 0 else None
            oldest_short = shorts[0] if len(shorts) > 0 else None
            if oldest_long == None and oldest_short == None:
                pass
            else:
                if oldest_long == None:
                    self.close_short()
                elif oldest_short == None:
                    self.close_long()
                else:
                    if oldest_long <= oldest_short:
                        self.close_long()
                    else:
                        self.close_short()
                traded = True
        return traded

    def stop_loss_farthest_on_margin(self, net_bal: float, margin_used: float):
        traded = False
        price = self.d.fdata('mid_c', self.i)
        if net_bal < margin_used * self.margin_sl_percent:
            farthest_long_price, farthest_short_price = price, price
            farthest_long, farthest_short = None, None
            for long, trade in self.d.fdata('open_longs', self.i).items():
                if trade[self.ENTRY] > farthest_long_price:
                    farthest_long_price = trade[self.ENTRY]
                    farthest_long = long
            for short, trade in self.d.fdata('open_shorts', self.i).items():
                if trade[self.ENTRY] < farthest_short_price:
                    farthest_short_price = trade[self.ENTRY]
                    farthest_short = short
            if farthest_long == None and farthest_short == None:
                pass
            else:
                if farthest_long == None:
                    self.close_short()
                elif farthest_short == None:
                    self.close_long()
                else:
                    if farthest_long_price - price > price - farthest_short_price:
                        self.close_long()
                    else:
                        self.close_short()
                traded = True
        return traded
    
    def stop_loss(self):
        net_bal, margin_used = self.current_ac_values()
        traded = False
        if self.stop_loss_type == 'grid_count':
            traded = self.stop_loss_grid_count()
        elif self.stop_loss_type == 'grid_count_on_margin':
            traded = self.stop_loss_grid_count_on_margin(net_bal, margin_used)
        elif self.stop_loss_type == 'oldest_on_margin':
            traded = self.stop_loss_oldest_on_margin(net_bal, margin_used)
        elif self.stop_loss_type == 'farthest_on_margin':
            traded = self.stop_loss_farthest_on_margin(net_bal, margin_used)

        if traded:
            self.update_temp_ac_values()
            self.update_events(self.EVENT_SL)
            # self.update_ac_values()

    def margin_call(self):
        net_bal, margin_used = self.current_ac_values()
        traded = False
        if net_bal < margin_used * self.MC_PERCENT:
            open_longs = self.d.fdata('open_longs', self.i).copy()
            for trade_no, trade in open_longs.items():
                self.close_long(trade_no)
                traded = True

            open_shorts = self.d.fdata('open_shorts', self.i).copy()
            for trade_no, trade in open_shorts.items():
                self.close_short(trade_no)
                traded = True

        if traded:
            self.update_temp_ac_values()
            self.update_events(self.EVENT_MC)
            # self.update_ac_values()
    
    def update_init_values(self):
        self.trade_no = 0
        self.next_up_grid = self.d.fdata('mid_c', 0)
        self.next_down_grid = self.d.fdata('mid_c', 0)
        if self.cash_out_factor is not None:
            self.d.update_fdata('cash_bal', self.i, 0)
    
    def run_sim(self):
        for i in tqdm(range(self.d.fdatalen), desc=" Simulating... "):
            self.i = i
            # self.calculate_values(init=True)
            if self.i == 0:
                self.update_init_values()
                self.entry()
            else:
                self.update_temp_ac_values(init=True)
                self.margin_call()
                self.stop_loss()
                self.take_profit()
                self.cash_transfer()
                self.entry()
                self.update_ac_values()

        return self.d.df[self.name].copy()
