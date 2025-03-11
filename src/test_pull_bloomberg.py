"""
Tests functions in pull_bloomberg responsible for the raw and clean data.
"""
import pandas as pd
import os
import pull_bloomberg
import numpy as np

data_dir = '../_data'

def test_pull_raw_tyields():
    """Checking if column names are correct
    and if raw data file is properly created
    """
    months = [x for x in range(1, 12)]
    years = [1, 2, 3, 5, 7, 10, 20, 30]
    t_list = [f'GB{x} Govt' for x in months] + [f'GT{x} Govt' for x in years]
    df = pull_bloomberg.pull_raw_tyields()
    assert df.columns == t_list
    
    file_dir = data_dir + '/bbg'
    file = file_dir + '/raw_syields.pkl'
    assert os.path.exists(file)

def test_pull_raw_syields():
    """Checking if column names are correct
    and if raw data file is properly created
    """
    years = [1, 2, 3, 5, 10, 20, 30]
    swap_list = [f'USSO{x} CMPN Curncy' for x in years]
    df = pull_bloomberg.pull_raw_syields()
    assert df.columns == swap_list

    file_dir = data_dir + '/bbg'
    file = file_dir + '/raw_syields.pkl'
    assert os.path.exists(file)

def test_clean_raw_tyields():
    """Checking with dummy data that all outputs are in the cleaned
    dtype and that the length of the output df is the same as the
    input df
    """
    test_df_index = pd.date_range('2025-01-01', '2025-01-03')
    test_df = pd.DataFrame(index = test_df_index)
    test_df['test1'] = ['1','2.3','seven']
    test_df['test2'] = ['1', '2', '0']
    test_df['test3'] = ['1.3', '9.01', '3.62']
    test_df['test4'] = ['sesdf', 'teststr', 'fakenews']
    test_len = len(test_df)
    test_df = pull_bloomberg.clean_raw_tyields(test_df, override = False, save_data = False)
    assert ((test_df.dtypes == np.int64) | (test_df.dtypes == np.float64)).all()
    
    assert len(test_df) == test_len

def test_clean_raw_syields():
    """Checking with dummy data that all outputs are in the cleaned
    dtype and that the length of the output df is the same as the
    input df
    """
    test_df_index = pd.date_range('2025-01-01', '2025-01-03')
    test_df = pd.DataFrame(index = test_df_index)
    test_df['test1'] = ['1','2.3','seven']
    test_df['test2'] = ['1', '2', '0']
    test_df['test3'] = ['1.3', '9.01', '3.62']
    test_df['test4'] = ['sesdf', 'teststr', 'fakenews']
    test_len = len(test_df)
    test_df = pull_bloomberg.clean_raw_syields(test_df, override = False, save_data = False)
    assert ((test_df.dtypes == np.int64) | (test_df.dtypes == np.float64)).all()
    
    assert len(test_df) == test_len