import bdshare
import numpy as np
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta


def momentum_strategy(start, end, formation, rolling_months):
	"""
	    Provides a list of stocks based on a monthly momentum strategy

	            Parameters:
	                    start (str): Start date
	                    end (str): End date
	                    formation (str): portfolio formation date
	                    rolling_months (int): no of months rolling period
	            Returns:
	                    momentum_profit (float64): mean of winner stock returns for latest month
	                    winners(list): list of winner stocks
	    """
	# parse all the values to datetime
	start = parser.parse(start)
	end = parser.parse(end)
	formation = parser.parse(formation)
	if start <= formation <= end:
		pass
	else:
		return 0
	# checks if date is between stored values and loads them in if it is
	# there is scope to optimize this
	if end <= parser.parse('2021-03-23') and start >= parser.parse('2020-01-01'):
		share_price_pivot = pd.read_csv(f"share_price_pivot_23-03-2021.csv", index_col='date')
	else:
		share_price_pivot = bdshare.get_hist_data(start, end)
	# take the closing price
	share_price_pivot["close"] = share_price_pivot["close"].astype('float64')
	# make a pivot of the closing price
	close_price_pivot = pd.pivot_table(share_price_pivot, values="close", columns="symbol",
	                                   index=share_price_pivot.index)

	# turn index column to datetime
	close_price_pivot.index = pd.to_datetime(close_price_pivot.index)
	# finds monthly return
	mtl_ret = close_price_pivot.pct_change().resample('M').agg(lambda x: (x + 1).prod() - 1)
	# returns over past 11 months
	past_11 = (mtl_ret + 1).rolling(rolling_months).apply(np.prod) - 1
	# take the formation date
	# check if it  is between start end end date
	end_measurement = formation - relativedelta(months=1)
	# find the return on the past month for this

	ret_12 = past_11.loc[end_measurement]
	# turn back to dataframe
	ret_12 = ret_12.reset_index()
	# drop null values
	ret_12.dropna(inplace=True)
	# take 10 quintiles
	ret_12["quintile"] = pd.qcut(ret_12.iloc[:, 1], 10, duplicates='drop', labels=False)
	# take winners in highest quintile
	winners = ret_12[ret_12.quintile == ret_12.quintile.max()]
	# sort winner values
	winners.sort_values(by=winners.columns[1], ascending=False, inplace=True)
	# find out winner returns
	winnerret = mtl_ret.loc[formation + relativedelta(months=1), close_price_pivot.columns.isin(winners.symbol)]
	# calculate momentum profit
	momentum_profit = winnerret.mean()

	return (str(momentum_profit*100) +'%'), winners


if __name__ == '__main__':
	print(momentum_strategy(start='2020-1-31', end='2021-3-3',formation='2021-1-31', rolling_months=12))
