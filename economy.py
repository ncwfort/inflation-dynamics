from params import SectorParams
from sectors import Sector
import rw



class Economy:
    """Basically a collection of all the sectors in the economy"""
    """To implement: price index calculation, etc."""
    def __init__(self, global_params):
        self.global_params = global_params
        self.sectors = []
        self.periods = 1

    # add a new sector 
    def add_sector(self, params):
        # to implement new version
        new_sector = Sector(params)
        self.sectors.append(new_sector)

    # advance by n periods
    def advance_n(self, n):
        for _ in range(n):
            self.advance()

    # advance by a single period
    def advance(self):
        for sector in self.sectors:
            sector.update()
        self.periods += 1
    
    """Returns sector object located at index."""
    def get_sector(self, index):
        return self.sectors[index]
    
    """imports parameters from a CSV and creates """
    def add_sectors_from_csv(self, filename):
        data_rows = rw.get_params(filename)
        for row in data_rows:
            self.add_sector_from_data(row)

    def add_sector_from_data(self, data_row):
        sector_params = SectorParams(data_row, self.global_params)
        self.add_sector(sector_params)

    def calculate_price_index(self):
        """Calculates the price index, setting the level in the first period to 1."""
        """Returns an array with the time series of the price index."""
        # handle the first period and set equal to 1
        initial_raw_value = self.get_raw_index_value(0)
        price_series = [1]
        for i in range(1, self.periods):
            raw_value = self.get_raw_index_value(i)
            price_series.append(raw_value / initial_raw_value)
        return price_series

    def get_raw_index_value(self, period):
        """Gets the raw (non-normalized) price index value for a period."""
        value = 0
        for sector in self.sectors:
            value += sector.get_indexed_price(period)
        return value
    
    def period_to_period_inflation_series(self):
        """Calculate a period-to-period inflation rate."""
        price_index = self.calculate_price_index()
        inflation_data = []
        for i in range(1, self.periods):
            percent_change = (price_index[i] - price_index[i-1]) / price_index[i-1]
            inflation_data.append(percent_change)
        return inflation_data

    def year_over_year_inflation_series(self):
        """Calculate a year over year inflation rate."""
        price_index = self.calculate_price_index()
        inflation_data = []
        for i in range(self.periods - 12):
            percent_change = (price_index[i+12] - price_index[i]) / price_index[i]
            inflation_data.append(percent_change)
        return inflation_data


