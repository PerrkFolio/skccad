def get_payments_okx(pay_methods, all_pay_methods):
    result = []
    for item in pay_methods:
        for i in range(len(all_pay_methods)):
            if item.find(all_pay_methods[i]) != -1: result.append(all_pay_methods[i])

    return result

def list_to_json(list_):
    json_result = [
        {"sell_price": list_[0][0], "sell_limit": list_[0][1], "sell_payments": list_[0][2], "buy_price": list_[0][3], "buy_limit": list_[0][4], "buy_payments": list_[0][5], "crypto": list_[0][6], "fiat": list_[0][7]},
        {"sell_price": list_[1][0], "sell_limit": list_[1][1], "sell_payments": list_[1][2], "buy_price": list_[1][3], "buy_limit": list_[1][4], "buy_payments": list_[1][5], "crypto": list_[1][6], "fiat": list_[1][7]},
        {"sell_price": list_[2][0], "sell_limit": list_[2][1], "sell_payments": list_[2][2], "buy_price": list_[2][3], "buy_limit": list_[2][4], "buy_payments": list_[2][5], "crypto": list_[2][6], "fiat": list_[2][7]},
        {"sell_price": list_[3][0], "sell_limit": list_[3][1], "sell_payments": list_[3][2], "buy_price": list_[3][3], "buy_limit": list_[3][4], "buy_payments": list_[3][5], "crypto": list_[3][6], "fiat": list_[3][7]},
        {"sell_price": list_[4][0], "sell_limit": list_[4][1], "sell_payments": list_[4][2], "buy_price": list_[4][3], "buy_limit": list_[4][4], "buy_payments": list_[4][5], "crypto": list_[4][6], "fiat": list_[4][7]},
        {"sell_price": list_[5][0], "sell_limit": list_[5][1], "sell_payments": list_[5][2], "buy_price": list_[5][3], "buy_limit": list_[5][4], "buy_payments": list_[5][5], "crypto": list_[5][6], "fiat": list_[5][7]}
    ]
    return json_result