from params import Params
from sectors import Sector
import rw

PARAMETER_INDICES = {
    'w0' : 0,
    'p0' : 1,
    'a' : 2,
    'phi' : 3,
    'mu' : 4,
    'freq_w' : 5,
    'freq_f' : 6,
    'lag_w' : 7,
    'lag_f' : 8,
    'index_weight' : 9
}

class Economy:
    """Basically a collection of all the sectors in the economy"""
    """To implement: price index calculation, etc."""
    def __init__(self, global_params):
        self.global_params = global_params
        self.sectors = []

    # add a new sector 
    def add_sector(self, w0, p0, a, phi, mu, freq_w, freq_f, lag_w, lag_f, index_weight):
        params = Params(self.global_params, w0, p0, a, phi, mu, freq_w, freq_f, lag_w, lag_f)
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
        w0 = data_row[PARAMETER_INDICES['w0']]
        p0 = data_row[PARAMETER_INDICES['p0']]
        a = data_row[PARAMETER_INDICES['a']]
        phi = data_row[PARAMETER_INDICES['phi']]
        mu = data_row[PARAMETER_INDICES['mu']]
        freq_w = data_row[PARAMETER_INDICES['freq_w']]
        freq_f = data_row[PARAMETER_INDICES['freq_f']]
        lag_w = data_row[PARAMETER_INDICES['lag_w']]
        lag_f = data_row[PARAMETER_INDICES['lag_f']]
        index_weight = data_row[PARAMETER_INDICES['index_weight']]
        self.add_sector(w0, p0, a, phi, mu, 
                        freq_w, freq_f, lag_w, lag_f, index_weight)


