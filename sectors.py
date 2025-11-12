from params import SectorParams

class Sector:
    """Implements the price and wage behavior of a single sector of the economy."""
    def __init__(self, params : SectorParams):
        self.params = params
        self.wages = [params.get('w0')]
        self.prices = [params.get('p0')]
        self.wage_shares = [self.calc_wage_share()]

    def calc_wage_share(self):
        """Calculates the wage share given the most recent price and wage information."""
        a = self.params.get('a')
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
        # defaults to 0
        new_wages = last_wages
        new_prices = last_prices
        # first, check whether wages update
        if(self.wages_update()):
            wage_freq_fraction = self.params.get('freq_w') / freq_max
            wage_percent_change = wage_freq_fraction * self.params.get('mu') * (v_w - last_wage_share)
            new_wages = last_wages * (1 + wage_percent_change)
        self.wages.append(new_wages)
        # next, check whether prices update
        if(self.prices_update()):
            price_freq_fraction = self.params.get('freq_f') / freq_max
            prices_percent_change = price_freq_fraction * self.params.get('phi') * (last_wage_share - v_f)
            new_prices = last_prices * (1 + prices_percent_change)
        self.prices.append(new_prices)
        self.wage_shares.append(self.calc_wage_share())


    def wages_update(self):
        """Checks whether wages update in the current period"""
        current_period = len(self.wages)
        freq = self.params.get('freq_w')
        lag = self.params.get('lag_w')
        return (current_period - lag) % freq == 0 
    
    def prices_update(self):
        """Checks whether prices update in the current period."""
        current_period = len(self.prices)
        freq = self.params.get('freq_f')
        lag = self.params.get('lag_f')
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
    
    """Return the equilibrium value where wages and prices change by the same amount."""
    def get_equilibrium(self):
        mu = self.params.get('mu')
        phi = self.params.get('phi')
        return (mu * self.params.global_params.v_w + 
                phi * self.params.global_params.v_f) / (mu + phi)
    
    def get_index_weight(self):
        """Returns the index weight for this sector"""
        return self.params.get('index_weight')
    
    def get_indexed_price(self, period):
        """Returns this sector's contribution to the overall price index in a particular period"""
        weight = self.get_index_weight()
        return self.prices[period] * weight



    
