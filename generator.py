import random as rd
from params import GlobalParams, SectorParams
from economy import Economy

TEST_SIMS = 1000 # how many times to run tests to simulate how the random generator is doing.
F_MAX = 12
V_W_MAX = 0.9 # max for uniform draws of v_w
V_W_MIN = 0.5 # min for uniform draws of v_w
V_F_MIN = 0.1 # max for uniform draws of v_f
V_F_MAX = 0.5 # max for uniform draws of v_f

W0_DEFAULT = 0.6 # default value for initial wage
P0_DEFAULT = 1.0 # default value for initial price
A_DEFAULT = 1.0 # default value for a

#default values for global parameters
V_W_DEFAULT = 0.7 
V_F_DEFAULT = 0.5
MU_BAR_DEFAULT = 0.5
PHI_BAR_DEFAULT = 0.5


class EconomyGenerator:

    """This class implements a random economy of n sectors, first generating global parameters."""
    """to do: add defaults for all values, choice of random"""

    def __init__(self, n_sectors, default_globals = True):
        self.n_sectors = n_sectors
        self.global_params = None
        if (default_globals): # generate globals according to default
            self.global_params = GlobalParams(V_W_DEFAULT, V_F_DEFAULT,
                                              MU_BAR_DEFAULT, PHI_BAR_DEFAULT, F_MAX)
        else: # draw globals from random distribution
            self.global_params = self.uniform_global_params()
        self.economy = Economy(self.global_params)
        # specifies default values for each parameter
        self.params_defaults = {
            'w0' : 0.68,
            'p0' : 1.0,
            'a' : 1.0,
            'freq_w' : 1.0,
            'freq_f' : 1.0,
            'lag_w' : 1.0,
            'lag_f' : 1.0,
            'index_weight' : 1 / n_sectors
        }
        # specifies whether default is used or randoms are generated
        self.param_is_default = {
            'w0' : True,
            'p0' : True,
            'a' : True,
            'phi_i' : True,
            'mu_i' : True,
            'freq_w' : False,
            'freq_f' : False,
            'lag_w' : False,
            'lag_f' : False
        }



    def uniform_global_params(self):
        """Generates global params, drawing from a uniform distribution."""
        v_w = rd.uniform(V_W_MIN, V_W_MAX)
        v_f = rd.uniform(V_F_MIN, V_F_MAX)
        f_max = F_MAX
        mu_bar = rd.uniform(0, 1)
        phi_bar = rd.uniform(0, 1)
        return GlobalParams(v_w, v_f, mu_bar, phi_bar, f_max)
    
    def generate_all_sectors(self, match_wages_prices=False):
        for _ in range(self.n_sectors):
            self.generate_sector(match_wages_prices)
    
    def get_economy(self):
        return self.economy
    
    def generate_sector(self, match_wages_prices : bool):
        w0 = p0 = a = phi_i = mu_i = freq_w = freq_f = lag_f = lag_w = 0
        if not self.param_is_default['w0']:
            w0 = rd.uniform(0, 1)
        else:
            w0 = self.params_defaults['w0']

        if not self.param_is_default['p0']:
            p0 = rd.uniform(w0, 1)
        else:
            p0 = self.params_defaults['p0']

        if not self.param_is_default['a']:
            a = self.get_a(w0, p0)
        else:
            a = self.params_defaults['a']
        
        phi_bar = self.global_params.phi_bar
        if self.param_is_default['phi_i']:
            phi_i = 0
        else:
            phi_i = rd.uniform(-phi_bar, 1 - phi_bar)

        mu_bar = self.global_params.mu_bar
        if self.param_is_default['mu_i']:
            mu_i = 0
        else:
            mu_i = rd.uniform(-mu_bar, 1 - mu_bar)

        if self.param_is_default['freq_w']:
            freq_w = self.params_defaults['freq_w']
        else:
            freq_w = rd.randint(1, 12)
        if self.param_is_default['freq_f']:
            freq_f = self.params_defaults['freq_f']
        elif match_wages_prices:
            freq_f = freq_w
        else:
            freq_f = rd.randint(1, 12)

        if self.param_is_default['lag_w']:
            lag_w = self.params_defaults['lag_w']
        else:
            lag_w = rd.randint(1, freq_w)
        if self.param_is_default['lag_f']:
            lag_f = self.params_defaults['lag_f']
        elif match_wages_prices:
            lag_f = lag_w
        else:
            lag_f = rd.randint(1, freq_f)

        weight = 1 / self.n_sectors
        sector_data = [w0, p0, a, phi_i, mu_i, freq_w, freq_f, lag_w, lag_f, weight]
        self.economy.add_sector_from_data(sector_data)

    def randomize_time_variables_only(self):
        """Generates an economy which randomizes time variables only."""
        self.generate_all_sectors()

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
        """Testing generation of constrained global parameters."""
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

    def set_is_default(self, param_name, value):
        self.param_is_default[param_name] = value

    def set_default_value(self, param_name, value):
        self.params_defaults[param_name] = value

    def gen_freq_var_only(self):
        """Generate a version in which there is only varation in frequency, not in lag."""
        """Implies that every sector will start in period 1."""
        self.param_is_default['lag_w'] = True
        self.param_is_default['lag_f'] = True
        self.generate_all_sectors()

    def freqs_lags_match(self):
        """ Generates an economy in which only lags and frequencies vary,
            but wage frequency and lag matches firm frequency and lag across all sectors."""
        self.generate_all_sectors(match_wages_prices=True)

    def gen_all_defaults(self):
        "Sets all values to default. Equivalent to a one-sector model."
        for key in self.param_is_default:
            self.param_is_default[key] = True
        self.generate_all_sectors()
        
