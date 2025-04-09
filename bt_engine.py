import pandas as pd
from signal_engine import get_moving_averages, get_signal

START_CAPITAL = 10_000_000  # 시작 자본 1천만 원

def run_backtest(price_df, short_window=5, long_window=20):
    df = get_moving_averages(price_df.copy(), short_window, long_window)
    df['Signal'] = df.apply(get_signal, axis=1)

    capital = START_CAPITAL
    position = None
    shares = 0
    portfolio_value = []
    trade_log = []

    for i in range(len(df)):
        date = df.index[i]
        close_price = df['Close'].iloc[i]
        signal = df['Signal'].iloc[i]

        # 매도
        if signal == 'BUY_PSQ' and position != 'PSQ':
            capital += shares * close_price
            trade_log.append((date, 'SELL', position, shares, close_price))
            position = 'PSQ'
            shares = capital // close_price
            capital -= shares * close_price
            trade_log.append((date, 'BUY', 'PSQ', shares, close_price))

        elif signal == 'SWITCH_TO_QQQ' and position != 'QQQ':
            capital += shares * close_price
            trade_log.append((date, 'SELL', position, shares, close_price))
            position = 'QQQ'
            shares = capital // close_price
            capital -= shares * close_price
            trade_log.append((date, 'BUY', 'QQQ', shares, close_price))

        elif signal == 'SWITCH_TO_QLD' and position != 'QLD':
            capital += shares * close_price
            trade_log.append((date, 'SELL', position, shares, close_price))
            position = 'QLD'
            shares = capital // close_price
            capital -= shares * close_price
            trade_log.append((date, 'BUY', 'QLD', shares, close_price))

        elif signal == 'BUY_TQQQ' and position != 'TQQQ':
            capital += shares * close_price
            trade_log.append((date, 'SELL', position, shares, close_price))
            position = 'TQQQ'
            shares = capital // close_price
            capital -= shares * close_price
            trade_log.append((date, 'BUY', 'TQQQ', shares, close_price))

        # 매일 자산 가치 계산
        total_value = capital + shares * close_price
        portfolio_value.append((date, total_value))

    result_df = pd.DataFrame(portfolio_value, columns=['Date', 'PortfolioValue'])
    result_df.set_index('Date', inplace=True)

    trades_df = pd.DataFrame(trade_log, columns=['Date', 'Action', 'Ticker', 'Shares', 'Price'])
    trades_df.set_index('Date', inplace=True)

    return result_df, trades_df
