from params import SectorParams

class Sector:
    """Implements the price and wage behavior of a single sector of the economy."""
    def __init__(self, params):
        self.params = params
        self.wages = [params.w0]
        self.prices = [params.p0]
        self.wage_shares = [self.calc_wage_share()]

    def calc_wage_share(self):
        """Calculates the wage share given the most recent price and wage information."""
        a = self.params.a
        return (self.wages[-1] * a) / self.prices[-1]
    
    def update(self):
        """Updates wages and prices for another period."""
        # get most recent wages, prices, wage share
        last_wages = self.get_last_wages()
        last_prices = self.get_last_prices()
        last_wage_share = self.get_last_wage_share()
        freq_max = self.params.global_params.frequency_max
        v_f = self.params.global_params.v_f
        v_w = self.params.global_params.v_w

        new_wages = 0
        new_prices = 0
        # first, check whether wages update
        if(self.wages_update()):
            wage_percent_change = (self.params.freq_w / freq_max) * self.params.mu * (v_w - last_wage_share)
            new_wages = last_wages * (1 + wage_percent_change)
        else:
            new_wages = last_wages # wages stay the same
        self.wages.append(new_wages)

        # next, check whether prices update
        if(self.prices_update()):
            prices_percent_change = (self.params.freq_f / freq_max) * self.params.phi * (last_wage_share - v_f)
            new_prices = last_prices * (1 + prices_percent_change)
        else:
            new_prices = last_prices
        self.prices.append(new_prices)
        self.wage_shares.append(self.calc_wage_share())


    def wages_update(self):
        """Checks whether wages update in the current period"""
        current_period = len(self.wages)
        freq = self.params.freq_w
        lag = self.params.lag_w
        return (current_period - lag) % freq == 0 
    
    def prices_update(self):
        """Checks whether prices update in the current period."""
        current_period = len(self.prices)
        freq = self.params.freq_f
        lag = self.params.lag_f
        return (current_period - lag) % freq == 0
    
    """Time series of wages."""
    def get_wage_time_series(self):
        return self.wages
    
    """Time series of prices."""
    def get_price_time_series(self):
        return self.prices
    
    """Time series of wage shares."""
    def get_wage_share_time_series(self):
        return self.wage_shares
    
    def get_last_wages(self):
        return self.wages[-1]
    
    def get_last_prices(self):
        return self.prices[-1]

    def get_last_wage_share(self):
        return self.wage_shares[-1]
    
    def get_n_periods(self):
        # how many periods have elapse
        return len(self.wages)


    
