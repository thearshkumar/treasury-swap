import pandas as pd
from xbbg import blp
import numpy as np
from datetime import timedelta
import os

data_dir = '../_data'

def pull_raw_tyields(override_download = False):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    file_dir = data_dir + '/bbg'
    file = file_dir + '/raw_tyields.pkl'
    if os.path.exists(file) and not override_download:
        print('Loading local treasury yield data.')
        df = pd.read_pickle(file)
    else:
        print('Fetching treasury yield data from Bloomberg')
        TODAY = pd.to_datetime('today').normalize() - timedelta(days=1)
        months = [1, 2, 3, 6, 12]
        years = [2, 3, 5, 7, 10, 20, 30]
        t_list = [f'GB{x} Govt' for x in months] + [f'GT{x} Govt' for x in years]
        try:
            df = blp.bdh(
                tickers = t_list,
                flds = ['PX_LAST',],
                start_date = '2000-01-01',
                end_date = TODAY
            )
        except Exception as e:
            print(f'Failed Bloomberg data pull.  See error below.')
            raise e
        df = df.rename(columns = {'GB12 Govt': 'GT1 Govt'})
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def pull_raw_syields(override_download = False):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    file_dir = data_dir + '/bbg'
    file = file_dir + '/raw_syields.pkl'
    if os.path.exists(file) and not override_download:
        print('Loading local swap yield data.')
        df = pd.read_pickle(file)
    else:
        print('Fetching swap yield data from Bloomberg')
        TODAY = pd.to_datetime('today').normalize() - timedelta(days=1)
        years = [1, 2, 3, 5, 10, 20, 30]
        swap_list = [f'USSO{x} CMPN Curncy' for x in years]
        try:
            df = blp.bdh(
                tickers = swap_list,
                flds = ['PX_LAST',],
                start_date = '2000-01-01',
                end_date = TODAY
            )
        except Exception as e:
            print(f'Failed Bloomberg data pull.  See error below.')
            raise e
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def clean_raw_tyields(raw_df, override = False):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    file_dir = data_dir + '/bbg'
    file = file_dir + '/tyields.pkl'
    if os.path.exists(file) and not override:
        print('Loading local cleaned treasury yield data.')
        df = pd.read_pickle(file)
    else:
        df = raw_df.apply(pd.to_numeric, errors = 'coerce')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def clean_raw_syields(raw_df, override = False):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    file_dir = data_dir + '/bbg'
    file = file_dir + '/syields.pkl'
    if os.path.exists(file) and not override:
        print('Loading local cleaned swap yield data.')
        df = pd.read_pickle(file)
    else:
        df = raw_df.apply(pd.to_numeric, errors = 'coerce')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_pickle(file)
    return df

def bloom_main():
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    raw_tyields = pull_raw_tyields()
    tyields = clean_raw_tyields(raw_tyields)

    raw_syields = pull_raw_syields()
    syields = clean_raw_syields(raw_syields)

if __name__ == '__main__':
    bloom_main()