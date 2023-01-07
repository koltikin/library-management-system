from openexchangerate import OpenExchangeRates


def make_list():
    all_data = OpenExchangeRates(api_key="641cfcb7ee9c49848d26607c341f8d59")
    currencys = (all_data.latest()).dict
    return currencys


currencys = make_list()


def convert_currency(first_brim, amount, seccond_brim, currency=currencys):
    list_of_contry_names = currency.keys()
    list_of_values = currency.values()
    one = currency[first_brim]
    two = currency[seccond_brim]
    result = (two * amount) / one
    return round(result, 4)


def convert_currency_update(first_brim, amount, seccond_brim):
    currencys = make_list()
    list_of_contry_names = currencys.keys()
    list_of_values = currencys.values()
    one = currencys[first_brim]
    two = currencys[seccond_brim]
    result = (two * amount) / one
    return round(result, 4)
