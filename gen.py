from settings import Settings
from economy import Economy
import random as rd
from params import GlobalParams

class Generator:
    """
    New generator classes which uses Settings object. Has a single external
    method which takes in a settings object and a number of sectors, and
    generates an economy from scratch according to that specification.
    """

    def __init__(self):
        # nothing happens until the generate method is called
        self.settings = None
        self.n_sectors = 0
        self.global_params = None
        self.economy = None
        pass

    def generate(self, settings : Settings, n_sectors):
        """
        Generates an economy according to the settings, with n sectors.
        """
        self.settings = settings
        self.n_sectors = n_sectors
        self.global_params = self.gen_global_params()
        self.economy = Economy(self.global_params)
        for _ in range(n_sectors):
            self.gen_sector()
        return self.economy

    def gen_global_params(self):
        """
        Generates the global parameters according to settings.
        """
        v_w = v_f = mu_bar = phi_bar = freq_max = 0
        settings = self.settings
        v_w = self.standard_gen('v_w')
        v_f = self.standard_gen('v_f')
        mu_bar = self.standard_gen('mu_bar')
        phi_bar = self.standard_gen('phi_bar')
        if settings.check_if_default('freq_max'):
            freq_max = settings.get_global_default('freq_max')
        else:
            rand_max = settings.get_rand_max('freq_max')
            freq_max = rd.randint(1, rand_max)
        return GlobalParams(v_w, v_f, mu_bar, phi_bar, freq_max)
    
    def gen_sector(self):
        """Generates a single sector based on the settings."""
        p0 = self.get_p0()
        w0 = self.get_w0(p0)
        a = self.get_a(w0, p0)
        phi_i = self.get_phi_i()
        mu_i = self.get_mu_i()
        freq_w = self.get_freq_w()
        freq_f = self.get_freq_f(freq_w)
        lag_w = self.get_lag_w(freq_w)
        lag_f = self.get_lag_f(freq_f, lag_w)
        index_weight = self.get_index_weight()
        sector_data = [w0, p0, a, phi_i, mu_i, freq_w, freq_f, lag_w,
                       lag_f, index_weight]
        self.economy.add_sector_from_data(sector_data)


    def get_w0(self, p0):
        settings = self.settings
        name = 'w0'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        else:
            rand_min = settings.get_rand_min(name)
            rand_max = p0
            return rd.uniform(rand_min, rand_max)

    def get_p0(self):
        settings = self.settings
        name = 'p0'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        else:
            rand_min = settings.get_rand_min(name)
            rand_max = settings.get_rand_max(name)
            return rd.uniform(rand_min, rand_max)
        
    def get_a(self, w0, p0):
        settings = self.settings
        name = 'a'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        else:
            v_w = self.global_params.v_w
            v_f = self.global_params.v_f
            v = rd.uniform(v_f, v_w) # generate random wage share instead
            # so that the number makes sense
            return (v * p0) / w0
        
    def get_phi_i(self):
        settings = self.settings
        name = 'phi_i'
        if settings.check_if_default(name):
            return 0
        else:
            phi_bar = self.global_params.phi_bar
            return rd.uniform(- phi_bar, 1 - phi_bar)
        
    def get_mu_i(self):
        settings = self.settings
        name = 'mu_i'
        if settings.check_if_default(name):
            return 0
        else:
            mu_bar = self.global_params.mu_bar
            return rd.uniform(-mu_bar, 1 - mu_bar)
        
    def get_freq_w(self):
        settings = self.settings
        name = 'freq_w'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        else:
            freq_max = self.global_params.frequency_max
            return rd.randint(1, freq_max)
        
    def get_freq_f(self, freq_w):
        settings = self.settings
        name = 'freq_f'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        elif settings.lags_match():
            return freq_w
        else:
            freq_max = self.global_params.frequency_max
            return rd.randint(1, freq_max)
        
    def get_lag_w(self, freq_w):
        settings = self.settings
        name = 'lag_w'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        else:
            return rd.randint(1, freq_w)
        
    def get_lag_f(self, freq_f, lag_w):
        settings = self.settings
        name = 'lag_f'
        if settings.check_if_default(name):
            return settings.get_sector_default(name)
        elif settings.lags_match():
            return lag_w
        else:
            return rd.randint(1, freq_f)
        
    def get_index_weight(self):
        return 1 / self.n_sectors


    def standard_gen(self, param_name):
        """
        Generates the simple global parameters that are continuous and
        bounded between two numbers.
        """
        settings = self.settings
        if settings.check_if_default(param_name):
            return settings.get_global_default(param_name)
        else:
            rand_min = settings.get_rand_min(param_name)
            rand_max = settings.get_rand_max(param_name)
            return rd.uniform(rand_max, rand_min)