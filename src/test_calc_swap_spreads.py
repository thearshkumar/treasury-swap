"""
Tests functions in calc_swap_spreads responsible for calculation and plots.
"""
import pandas as pd
from datetime import datetime, timedelta
import calc_swap_spreads
from pull_bloomberg import *

def test_calc_swap_spreads():
    """Checking Column Names and Expected Outputs Given Input Data
    """

    raw_syields = pull_raw_syields()
    swap_df = clean_raw_syields(raw_syields)

    raw_tyields = pull_raw_tyields()
    treasury_df = clean_raw_tyields(raw_tyields)

    total_list = swap_df.columns + treasury_df.columns

    output = calc_swap_spreads()
    years = [1,2,3,5,10,20,30]
    for year in years:
        total_list.append(f'Arb_Swap_{year}')
        total_list.append(f'tswap_{year}_rf')
    total_list.append('Year')

    assert output.columns == total_list

    for year in years:
        assert (output[f'Arb_Swap_{year}'] == 100 * (-treasury_df[f'GT{year} Govt'] + swap_df[f'USSO{year} CMPN Curncy'])).all()
        assert (output[f'tswap_{year}_rf'] == swap_df[f'USSO{year} CMPN Curncy'] * 100).all()
        assert (output['year'] == pd.to_datetime(output.index).year).all()

def test_plot_figure():
    """TODO: could check if two plots are identical based on the rgb values
    """
    # Test with dummy plot, and check if it saves the correct name in the dir
    pass
def test_swap_main():
    """TODO: Tests swap_main to check if it saves the correct files in the correct
    destination
    """
    # Checking the actual plots if they are being saved
    pass