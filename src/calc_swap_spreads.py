import pandas as pd
from pull_bloomberg import *
import matplotlib.pyplot as plt

output_dir = '../_output'

def calc_swap_spreads():

    raw_syields = pull_raw_syields()
    swap_df = clean_raw_syields(raw_syields)

    raw_tyields = pull_raw_tyields()
    treasury_df = clean_raw_tyields(raw_tyields)

    s_years = [1,2,3,5,10,20,30]
    merged_df = pd.merge(swap_df, treasury_df, left_index = True, right_index = True, how = 'inner')
    for i in s_years:
        # Calculating the Treasury yield minus the Swap Yield (swap rate)
        # The assumption here is that if this value goes negative, then this is an arb.
        # We pay fixed in the swap agreement and receive the floating rate. Then, we 
        # purchase a treasury on repo, meaning that we are receiving the treasury rate
        # and paying a floating repo rate.  Thus, we get paid 
        # T_rate - Swap_rate + Swap_floating - Repo_Floating.  Hence, this is not a true
        # arbitrage unless you are guaranteed that you can secure 3mo treasury repos at the
        # SOFR (if you are paying fixed in a quarterly SOFR swap).  Since repos have a
        # premium over SOFR (SOFR + ~10 bps)
        # Furthermore, **this is in no way an arb, but we ball anyway**
        merged_df[f'Arb_Swap_{i}'] = 100 * (-merged_df[f'GT{i} Govt'] + merged_df[f'USSO{i} CMPN Curncy'])
        merged_df[f'tswap_{i}_rf'] = merged_df[f'USSO{i} CMPN Curncy'] * 100

    merged_df['Year'] = pd.to_datetime(merged_df.index).year
    merged_df = merged_df[merged_df['Year'] >= 2000]

    arb_list = [f'Arb_Swap_{x}' for x in s_years]
    tswap_list = [f'tswap_{x}_rf' for x in s_years]
    merged_df = merged_df[arb_list + tswap_list]
    merged_df = merged_df[merged_df.isna().all(axis=1) == False]

    return merged_df

if __name__ == '__main__':
    arb_df = calc_swap_spreads()
    years = [1,2,3,5,10,20,30]
    start = pd.Timestamp('2010-01-01').date()
    end = pd.Timestamp('2020-03-01').date()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for year in years:
        label = f'{year}Y'
        plt.plot(arb_df[f'Arb_Swap_{year}'].loc[start:end].dropna(), label = label)
    plt.title('Treasury-Swap')
    plt.xlabel('Dates')
    plt.ylabel('Arbitrage Spread (bps)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.grid(axis = 'y')
    plt.savefig(output_dir + '/replicated_swap_spread_arb_figure.png')
    plt.show()
    for year in years:
        label = f'{year}Y'
        plt.plot(arb_df[f'Arb_Swap_{year}'].loc[start:].dropna(), label = label)
    plt.title('Treasury-Swap')
    plt.xlabel('Dates')
    plt.ylabel('Arbitrage Spread (bps)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.grid(axis = 'y')
    plt.savefig(output_dir + '/updated_swap_spread_arb_figure.png')
    plt.show()