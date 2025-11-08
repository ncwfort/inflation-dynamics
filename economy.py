from params import SectorParams
from sectors import Sector
import rw



class Economy:
    """Basically a collection of all the sectors in the economy"""
    """To implement: price index calculation, etc."""
    def __init__(self, global_params):
        self.global_params = global_params
        self.sectors = []

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


