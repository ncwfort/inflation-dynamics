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
        pass

    def generate(self, settings : Settings, n_sectors):
        """
        Generates an economy according to the settings, with n sectors.
        """
        self.settings = settings
        self.n_sectors = n_sectors
        self.global_params = self.gen_global_params()
        self.global_params.print_global_params()
        economy = Economy(self.global_params)

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

    def standard_gen(self, param_name):
        settings = self.settings
        if settings.check_if_default(param_name):
            return settings.get_global_default(param_name)
        else:
            rand_min = settings.get_rand_min(param_name)
            rand_max = settings.get_rand_max(param_name)
            return rd.uniform(rand_max, rand_min)