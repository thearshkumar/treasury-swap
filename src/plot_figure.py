"""
Functions to plot and save them.
"""

import pandas as pd
import matplotlib.pyplot as plt
from calc_swap_spreads import *

output_dir = Path(config("OUTPUT_DIR"))
# output_dir = '/Users/arshkumar/MyPython/FINM/treasury-swap/_output'

def plot_figure(arb_df, savePath, end=None):

    """Displaying and saving the plot generated using the data provided.

    :param arb_df: DataFrame containing the arbitrage calculations per year
    :type arb_df: pd.DataFrame
    :param savePath: Path for saving the plot
    :type savePath: str
    :param end: end date for the plot, defaults to None which then means using 
    the last date in arb_df
    :type end: pd.Timestamp

    :return: void
    """
    start = pd.Timestamp('2010-01-01').date()
    for year in [1,20,2,30,3,5,10]:
        label = f'{year}Y'
        if end:
            plt.plot(arb_df[f'Arb_Swap_{year}'].loc[start:end].dropna(), label = label)
        else:
            plt.plot(arb_df[f'Arb_Swap_{year}'].loc[start:].dropna(), label = label)
    plt.title('Treasury-Swap')
    plt.xlabel('Dates')
    plt.ylabel('Arbitrage Spread (bps)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.grid(axis = 'y')
    plt.savefig(savePath, bbox_inches='tight')
    plt.close()

def plot_main():
    """
    Main function that displays and saves the replicated and updated plots
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_dir = os.path.join(data_dir, '/calc_spread')
    file = os.path.join(file_dir, '/calc_merged.pkl')
    if os.path.exists(file):
        arb_df = pd.read_pickle(file)
    else:
        arb_df = calc_swap_spreads(bloom_main())
    end = pd.Timestamp('2024-02-28').date()

    plot_figure(arb_df, os.path.join(output_dir, 'replicated_swap_spread_arb_figure.png'), end)

    plot_figure(arb_df, os.path.join(output_dir, 'updated_swap_spread_arb_figure.png'))

    print("Dimensions: ")
    print(arb_df.shape)
    print("First valid date: ")
    print(arb_df.first_valid_index())
    print("Last valid date: ")
    print(arb_df.last_valid_index())

if __name__ == '__main__':
    plot_main()