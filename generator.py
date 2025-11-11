import random as rd
from params import GlobalParams, SectorParams
from economy import Economy

TEST_SIMS = 1000 # how many times to run tests to simulate how the random generator is doing.
F_MAX = 12

class EconomyGenerator:

    """This class implements a random economy of n sectors, first generating global parameters."""

    def __init__(self, n_sectors):
        self.n_sectors = n_sectors
        self.global_params = self.gen_global_params()
        self.economy = Economy(self.global_params)


    def gen_global_params(self):
        v_w = rd.uniform(0.5, 0.9)
        v_f = rd.uniform(0.1, 0.9)
        f_max = 12
        mu_bar = rd.uniform(0, 1)
        phi_bar = rd.uniform(0, 1)
        return GlobalParams(v_w, v_f, mu_bar, phi_bar, f_max)
    
    def generate_all_sectors(self):
        for _ in range(self.n_sectors):
            self.generate_sector()
    
    def get_economy(self):
        return self.economy
    
    def generate_sector(self):
        w0 = rd.uniform(0, 1)
        p0 = rd.uniform(w0, 1)
        a = self.get_a(w0, p0)
        
        phi_bar = self.global_params.phi_bar
        phi_i = rd.uniform(-phi_bar, 1 - phi_bar)

        mu_bar = self.global_params.mu_bar
        mu_i = rd.uniform(-mu_bar, 1 - mu_bar)

        freq_w = rd.randint(1, 12)
        freq_f = rd.randint(1, 12)
        lag_w = rd.randint(1, freq_w)
        lag_f = rd.randint(1, freq_f)

        weight = 1 / self.n_sectors
        sector_data = [w0, p0, a, phi_i, mu_i, freq_w, freq_f, lag_w, lag_f, weight]
        self.economy.add_sector_from_data(sector_data)

    def get_a(self, w0, p0):
        """Generates a value for a that behaves reasonably given other values."""
        initial_v = rd.uniform(self.global_params.v_f, self.global_params.v_w)
        return (initial_v * p0) / w0
    
    def constrained_global_params(self):
        """Constrained global parameters, so that mu_bar and phi_bar are equal."""
        v_w = rd.uniform(0.5, 0.9)
        v_f = rd.uniform(0.1, 0.9)
        f_max = 12
        mu_bar = rd.uniform(0, 1)
        phi_bar = mu_bar
        return GlobalParams(v_w, v_f, mu_bar, phi_bar, f_max)
    
    def test_constrained_params(self):
        v_w_list = []
        v_f_list = []
        mu_bar_list = []
        phi_bar_list = []
        for _ in range(TEST_SIMS):
            params = self.constrained_global_params()
            v_w_list.append(params.v_w)
            v_f_list.append(params.v_f)
            mu_bar_list.append(params.mu_bar)
            phi_bar_list.append(params.phi_bar)
        print(f"Average v_w: {sum(v_w_list) / len(v_w_list)}")
        print(f"Average v_f: {sum(v_f_list) / len(v_f_list)}")
        print(f"Average mu_bar: {sum(mu_bar_list)/ len(mu_bar_list)}")
        print(f"Average phi_bar: {sum(phi_bar_list) / len(phi_bar_list)}")
    
