import pandas as pd

def get_moving_averages(df, short_window, long_window):
    df['short_sma'] = df['Close'].rolling(window=short_window).mean()
    df['long_sma'] = df['Close'].rolling(window=long_window).mean()
    df['long_sma_1.2'] = df['long_sma'] * 1.2
    df['long_sma_1.1'] = df['long_sma'] * 1.1
    return df

def get_signal(row):
    short = row['short_sma']
    long = row['long_sma']
    long_1_1 = row['long_sma_1.1']
    long_1_2 = row['long_sma_1.2']

    signal = None
    # 시그널 구간 분기 처리
    if pd.isna(short) or pd.isna(long):
        return None

    if short > long:
        signal = 'BUY_TQQQ'
    elif short < long:
        signal = 'BUY_PSQ'
    elif short < long_1_1:
        signal = 'SWITCH_TO_QQQ'
    elif short < long_1_2:
        signal = 'SWITCH_TO_QLD'

    return signal
