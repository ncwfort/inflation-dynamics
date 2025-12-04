from params import SectorParams

class Sector:
    """ Implements the price and wage behavior of a single 
        sector of the economy. Includes storage of time series data, the 
        functionality to advance by a period, and return time series.
        Initialized with a params object."""
    def __init__(self, params : SectorParams):
        self.params = params
        self.wages = [params.get('w0')]
        self.prices = [params.get('p0')]
        self.wage_shares = [self.calc_wage_share()]

    
    """ Updates wages and prices for a single period, according to
        difference equation specifying the dynamics of the model."""
    def update(self):
        # get most recent wages, prices, wage share
        last_wages = self.get_last_wages()
        last_prices = self.get_last_prices()
        last_wage_share = self.get_last_wage_share()
        # stores global parameters
        freq_max = self.params.global_params.frequency_max
        v_f = self.params.global_params.v_f
        v_w = self.params.global_params.v_w
        # defaults to last value, only changes based on logic
        new_wages = last_wages
        new_prices = last_prices
        # first, check whether wages update
        if(self.wages_update()):
            # get the fraction by which to adjust parameter
            freq_fraction = self.params.get('freq_w') / freq_max
            # get the departure from aspirational value
            diff_from_desired = v_w - last_wage_share
            mu = self.params.get('mu')
            # calculate wage percent change based on formulaa
            wage_percent_change = freq_fraction * mu * diff_from_desired
            new_wages = last_wages * (1 + wage_percent_change)
        self.wages.append(new_wages)
        # next, check whether prices update
        if(self.prices_update()):
            # get the fraction by which to adjust parameter
            freq_fraction = self.params.get('freq_f') / freq_max
            # get departure from aspiration value
            diff_from_desired = last_wage_share - v_f
            phi = self.params.get('phi')
            prices_percent_change = freq_fraction * diff_from_desired * phi
            new_prices = last_prices * (1 + prices_percent_change)
        self.prices.append(new_prices)
        # calculate new wage share and add to wage share series
        self.wage_shares.append(self.calc_wage_share())

    """Checks whether wages update in the current period"""
    def wages_update(self):
        # gets the current period by finding the length of wages vector
        # since this includes a value at 0
        current_period = len(self.wages)
        freq = self.params.get('freq_w')
        lag = self.params.get('lag_w')
        return (current_period - lag) % freq == 0 
    
    """Checks whether prices update in the current period."""
    def prices_update(self):
        # gets the current period by finding the length of the prices vector
        current_period = len(self.prices)
        freq = self.params.get('freq_f')
        lag = self.params.get('lag_f')
        return (current_period - lag) % freq == 0
    
    """ Calculates the wage share (wa)/p given the data from the most recent 
        period."""
    def calc_wage_share(self):
        a = self.params.get('a')
        return (self.wages[-1] * a) / self.prices[-1]
    
    """Time series of wages."""
    def get_wage_time_series(self):
        return self.wages
    
    """Time series of prices."""
    def get_price_time_series(self):
        return self.prices
    
    """Time series of wage shares."""
    def get_wage_share_time_series(self):
        return self.wage_shares
    
    """Returns wages in last period."""
    def get_last_wages(self):
        return self.wages[-1]
    
    """Returns prices in last period."""
    def get_last_prices(self):
        return self.prices[-1]
    
    """ Returns prices in last period. (Assumes has already been calculated
        and that the list has been updated."""
    def get_last_wage_share(self):
        return self.wage_shares[-1]
    
    """Consider deleting if I don't find a reference for this."""
    def get_n_periods(self):
        return len(self.wages)
    
    """Return the equilibrium wage share value where wages and prices change 
        by the same amount. Obtained through analyzing the equations"""
    def get_ws_equilibrium(self):
        mu = self.params.get('mu')
        phi = self.params.get('phi')
        if mu != 0 or phi != 0:
            return (mu * self.params.global_params.v_w + 
                    phi * self.params.global_params.v_f) / (mu + phi)
        else:
            return 0
    
    """Returns the index weight for this sector"""
    def get_index_weight(self):
        return self.params.get('index_weight')
    
    """ Returns this sector's contribution to the overall price index in a 
        particular period"""
    def get_indexed_price(self, period):
        weight = self.get_index_weight()
        return self.prices[period] * weight
    
    def print_wages_and_prices(self):
        for i in range(len(self.prices)):
            print(f"Period {i}")
            print(f"Wages: {self.wages[i]}")
            print(f"Prices: {self.prices[i]}")
            print('\n')

    def shock(self, size):
        """
        Simulates a shock to the sector's prices. 'Size' gives the size of the
        shock, as a proportion of the previous period's prices.
        Assumes that the last period is greater than or equal to 1, as it calls
        the period before.
        """
        previous_price = self.prices[-2]
        self.prices[-1] += size * previous_price

    def shock_if_prices_update(self, size):
        """
        Simulates a shock, but only if the sector's prices update in that
        period. In general, called after regular price updating, so the period
        to check is actuall the length of the prices list - 1.
        """
        last_period = len(self.prices) - 1
        freq_f = self.params.get('freq_f')
        lag_f = self.params.get('lag_f')
        previous_price = self.prices[-2]
        if (last_period - lag_f) % freq_f == 0:
            self.prices[-1] += size * previous_price



    
