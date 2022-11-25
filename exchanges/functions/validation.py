def valid_fiat(fiat, all_fiat):
    q = 0
    for i in range(len(all_fiat)):
        if all_fiat[i] == fiat:
            q += 1
            break

    if q == 1: result = []
    else: result = ["None"]

    return result
