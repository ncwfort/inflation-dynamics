from params import SectorParams, GlobalParams
from sectors import Sector
import rw
from tqdm import tqdm
import numpy as np

# temporarily hard wiring constants here
ALPHA = 0.4
SIGMA_ETA = 0.01

class Economy:
    """Basically a collection of all the sectors in the economy. Allows
        collection of multiple sectors and the updating of multiple sectors
        at a time. Also handles price index calculation."""
    
    def __init__(self, global_params: GlobalParams, stochastic = False,
                 single_persistent_shocks = False):
        self.global_params = global_params
        self.sectors = []
        self.periods = 1 # includes the inital values as a period
        self.stochastic = stochastic
        self.single_shocks = single_persistent_shocks
        self.shocks = [0]

    def set_stochastic(self, value):
        self.stochastic = value

    def add_sector(self, params : SectorParams):
        """
        Creates a sector and adds it to the list of sectors.

        params: The parameters of the sector to be created.
        """
        new_sector = Sector(params)
        self.sectors.append(new_sector)

    def advance_n(self, n):
        """
        Advances all sectors by a specified number of periods.

        n: the number of periods to advance        
        """
        for _ in range(n):
            self.advance()


    def advance(self):
        """Advances each sector by a single period and updates period number"""
        for sector in self.sectors:
            sector.update() # uses sector's built-in update methods
        if self.stochastic:
            self.stochastic_shocks(ALPHA, SIGMA_ETA)
        elif self.single_shocks:
            self.track_single_shocks(ALPHA)
        self.periods += 1
    
    def get_sector(self, index):
        """Returns sector object located at index in the list of sectors."""
        return self.sectors[index]
    
    def add_sector_from_data(self, param_list):
        """
        Placeholder function which takes in a list and adds a sector to the
        model with that specification until I can make all of this work better.
        """
        sector_params = SectorParams(param_list, self.global_params)
        self.add_sector(sector_params)
    
    def add_sectors_from_csv(self, filename):
        """
        Takes in a CSV, where each row is the parameters for a sector. Creates
        a sector from each row and adds it into the economy. Which column
        corresponds to which parameters are defaults, which can be adjusted in
        the params class.
        TODO: think more efficiently about in which class these methods should
        live.

        filename: the name of the CSV file with the list of parameters 
        """
        # get a list of lists, each item of which is a list of sector params
        data_rows = rw.get_params(filename)
        for row in data_rows:
            # create params from each row
            sector_params = SectorParams(row, self.global_params)
            # adds a sector with new params to the economy
            self.add_sector(sector_params)

    def calculate_price_index(self):
        """
        Calculates the price index for each period and returns a list with the
        price index over all periods. The value in period 0 is normalized to 1.
        """
        # handle the first period and set equal to 1
        initial_raw_value = self.get_raw_index_value(0)
        # set the first value of the price series equal to 1
        price_series = [1]
        for i in range(1, self.periods): # begin in period 1
            raw_value = self.get_raw_index_value(i)
            # add the normalized version of the raw value
            price_series.append(raw_value / initial_raw_value)
        return price_series

    def get_raw_index_value(self, period):
        """
        Gets the raw (non-normalized) price index value for a period. That is,
        just returns the sum of prices in a sector multiplied by their weights
        in the price index.

        period: the period to fetch the raw indes value value
        """
        value = 0
        for sector in self.sectors:
            value += sector.get_indexed_price(period) # uses method in Sector
        return value
    
    def period_to_period_inflation_series(self):
        """
        Calculate a period-to-period inflation rate. That is, what is the rate
        of change from one period to the next? Returns a list of all of these
        values for all periods.
        """
        price_index = self.calculate_price_index() # get price index series
        inflation_data = []
        for i in range(1, self.periods):
            index_change = price_index[i] - price_index[i-1]
            percent_change = index_change / price_index[i-1]
            inflation_data.append(percent_change)
        return inflation_data

    def year_over_year_inflation_series(self):
        """
        Gets a year-over-year inflation series, with the convention that a year
        is 12 periods.
        """
        return self.lagged_inflation_series(12)

    def lagged_inflation_series(self, lag):
        """
        Calculates a lagged inflation series, measuring the rate of change of
        price in one period compared to 'lag' periods earlier. Primarily
        used for year-over-year, where a year is 12 periods.

        lag: the length of the lag for the lagged series
        """
        price_index = self.calculate_price_index()
        inflation_data = []
        for i in range(self.periods - lag):
            absolute_change = price_index[i+lag] - price_index[i]
            percent_change = absolute_change / price_index[i]
            inflation_data.append(percent_change)
        return inflation_data
    
    def get_moving_average(self, time_series, window):
        """
        Takes the moving average of a particular time series over a particular
        interval.

        time_series: the data to calculate the moving average on
        window: the size of the window over which the moving average is done
        """
        avg_series = []
        periods = len(time_series)
        for i in range(periods - window + 1):
            data_subset = time_series[i:i+window]
            avg_series.append(sum(data_subset) / window)
        return avg_series
    
    def get_yoy_moving_average(self, window):
        """
        Gets the moving average of the year-over-year inflation figure over
        a particular window of moving average.
        """
        return self.get_moving_average(self.year_over_year_inflation_series(), 
                                       window)
    
    def get_ptp_moving_average(self, window):
        """
        Gets the moving average of the period-to-period inflation figure with a
        particular width (window) of moving average.
        """
        return self.get_moving_average(self.period_to_period_inflation_series(), 
                                       window)

    def shock_all_sectors(self, shock_size):
        """
        Exogenously shocks all sectors with a price increase.
        'Size' is the magnitude of the shock, in terms of the proportion of
        previous prices.
        """
        for sector in self.sectors:
            sector.shock(shock_size)

    def stochastic_shocks(self, alpha, sigma_eta):
        this_shock = alpha * self.shocks[-1] + np.random.normal(0, sigma_eta)
        self.shock_all_sectors(this_shock)
        self.shocks.append(this_shock)

    def track_single_shocks(self, alpha, size = 0):
        this_shock = alpha * self.shocks[-1] + size
        for sector in self.sectors:
            sector.shock_if_prices_update(this_shock)
        self.shocks.append(this_shock)

    def do_single_shock(self, size):
        self.single_shocks = False
        self.advance()
        self.track_single_shocks(ALPHA, size)
        self.single_shocks = True


