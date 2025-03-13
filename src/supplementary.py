import pandas as pd
from pull_bloomberg import *

# Assumption: Swap and treasury can both be entered for the same floating rate.
# Swap on SOFR
# Assumption is that floating rate repo on treasury is the same as SOFR (or whatever the swap floating rate is - which is almost never going to be the case)
# However, if this was the case, then we would say that 'borrowing' the treasury on a repo exactly replicates the payoff of the swap if the swap rate is the same as
# The coupon on the treasury (if they have the same coupon structure)

def replication_df(treasury_df, swap_df):
    years = [1, 2, 3, 5, 10, 20, 30]
    t_list = [f'GT{year} Govt' for year in years]
    s_list = [f'USSO{year} CMPN Curncy' for year in years]
    return pd.merge(treasury_df[t_list].loc[pd.Timestamp('2010').date():], swap_df[s_list].loc[pd.Timestamp('2010').date():], left_index = True, right_index = True, how = 'inner')

def supplementary_main():
    swap_df = clean_raw_syields(pull_raw_syields())
    treasury_df = clean_raw_tyields(pull_raw_tyields())
    return replication_df(treasury_df, swap_df)


if __name__ == '__main__':
    supplementary_main()
