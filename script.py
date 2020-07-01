import os
import sys
import time
import datetime

import pandas
import MetaTrader5 as mt5

if __name__ == "__main__":
    
    # parsing input
    try:
        _, output_dir = sys.argv
    except: 
        sys.exit("Usage: python script.py <output_dir>")
    
    os.makedirs(output_dir, exist_ok=True)

    try:
        records = pandas.read_csv('records.csv')
    except:
        records = pandas.DataFrame()

    mt5.initialize()

    while True:
        # fetch all positions from mt5 terminal
        trades = mt5.positions_get()

        for trade in trades:
            record = {
                'open_price'  : [trade.price_open],
                'trade_id'    : [trade.ticket],
                'trade_tag'   : [trade.comment],
                'trade_magic' : [trade.magic],
                'current_pnl' : [trade.profit],
                'current_dt'  : [datetime.datetime.now()]
            }
            record = pandas.DataFrame(record)

            if records.empty:
                records = record
            else:
                records = records.append(record)

            if records.empty: continue
            
            output_path = os.path.join(output_dir, 'records.csv')
            records.to_csv(output_path)

        time.sleep(10)
        




