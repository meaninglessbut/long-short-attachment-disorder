def weekly_additional_investment(current_date, current_signal, portfolio, psq_holding_value):
    if current_date.weekday() != 0:  # 월요일만 매수
        return portfolio
    
    if current_signal == 'BUY_TQQQ' or current_signal == 'SWITCH_TO_QQQ':
        # 장기 우상향: QQQ 정기 적립
        portfolio['QQQ'] += 1  # 예시: 1주 매수
    elif current_signal == 'BUY_PSQ':
        # PSQ 매수 중일 때 → 50만원어치 PSQ 팔고 QQQ 분할 매수
        amount_to_sell = min(psq_holding_value, 500000)
        portfolio['PSQ'] -= amount_to_sell
        portfolio['QQQ'] += amount_to_sell  # 단순 예시, 가격 적용 필요

    return portfolio
