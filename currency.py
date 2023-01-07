from openexchangerate import OpenExchangeRates


class make_list:
    def __init__(self):
        self.mm = OpenExchangeRates(api_key="641cfcb7ee9c49848d26607c341f8d59")
        self.kk = (self.mm.latest()).dict


currencys = make_list().kk


class convert_currency:
    def __init__(self):
        self.currency = currencys
        self.list_of_contry_names = list(self.currency.keys())
        self.list_of_values = list(self.currency.values())

    def see(self, one, amount_one, two):
        one = self.currency[one]
        two = self.currency[two]
        result = (two * amount_one) / one
        return round(result, 4)


# def make_list():
#     all_data = OpenExchangeRates(api_key="641cfcb7ee9c49848d26607c341f8d59")
#     dict_data = (all_data.latest()).dict
#     return dict_data


# currencys = make_list()


# def convert_currency(first_brim, amount, seccond_brim):
#     list_of_contry_names = currencys.keys()
#     list_of_values = currencys.values()

#     one = currencys[first_brim]
#     two = currencys[seccond_brim]
#     result = (two * amount) / one
#     return round(result, 4)
