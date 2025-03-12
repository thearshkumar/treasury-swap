"""
Responsible for calculating the spreads, and saving it.
"""

import pandas as pd
from pull_bloomberg import *
from pathlib import Path
from settings import config

output_dir = Path(config("OUTPUT_DIR"))

def calc_swap_spreads(treasury_df, swap_df):
    """Combines the treasury and swap data and calculates the spreads

    :param treasury_df: DataFrame containing the treasury yield data
    :type treasury_df: pd.DataFrame
    :param treasury_df: Path for saving the plot
    :type treasury_df: pd.DataFrame
    :return: The merged data frame containing the clean and calculated data
    :rtype: pd.DataFrame
    """

    s_years = [1,2,3,5,10,20,30]
    merged_df = pd.merge(swap_df, treasury_df, left_index = True, right_index = True, how = 'inner')
    for i in s_years:
        merged_df[f'Arb_Swap_{i}'] = 100 * (-merged_df[f'GT{i} Govt'] + merged_df[f'USSO{i} CMPN Curncy'])
        merged_df[f'tswap_{i}_rf'] = merged_df[f'USSO{i} CMPN Curncy'] * 100

    merged_df['Year'] = pd.to_datetime(merged_df.index).year
    merged_df = merged_df[merged_df['Year'] >= 2000]

    arb_list = [f'Arb_Swap_{x}' for x in s_years]
    tswap_list = [f'tswap_{x}_rf' for x in s_years]
    merged_df = merged_df[arb_list + tswap_list]
    merged_df = merged_df[merged_df.isna().all(axis=1) == False]

    return merged_df

def swap_main():
    """Calculates the spreads and saves them.
    """
    swap_df = clean_raw_syields(pull_raw_syields())
    treasury_df = clean_raw_tyields(pull_raw_tyields())

    arb_df = calc_swap_spreads(treasury_df, swap_df)

    file_dir = os.path.join(data_dir , 'calc_spread')
    file = os.path.join(file_dir, 'calc_merged.pkl')
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    arb_df.to_pickle(file)


if __name__ == '__main__':
    swap_main()