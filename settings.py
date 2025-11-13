"""
Store default values for global parameters. Change these to affect the run.
"""
GLOBAL_DEFAULTS = {
    'v_w' : 0.7,
    'v_f' : 0.5,
    'mu_bar' : 0.5,
    'phi_bar' : 0.5,
    'freq_max' : 12
}

SECTOR_DEFAULTS = {
    'w0' : 0.6,
    'p0' : 1.0,
    'a' : 1.0,
    'freq_w' : 1.0,
    'freq_f' : 1.0,
    'lag_w' : 1.0,
    'lag_f' : 1.0
}

IS_DEFAULT = {
    'v_w' : True,
    'v_f' : True,
    'mu_bar' : True,
    'phi_bar' : True,
    'freq_max' : True,
    'w0' : True,
    'p0' : True,
    'a' : True,
    'phi_i' : True,
    'mu_i' : True,
    'freq_w' : False,
    'freq_f' : False,
    'lag_w' : False,
    'lag_f' : False,
    'index_weight' : True
}

RAND_MAX = {
    'v_w' : 1.0,
    'v_f' : 1.0,
    'mu_bar' : 1.0,
    'phi_bar' : 1.0,
    'freq_max' : 100,
    'p0' : 10
}

RAND_MIN = {
    'v_w' : 0,
    'v_f' : 0,
    'mu_bar' : 0,
    'phi_bar' : 0,
    'w0' : 0,
    'p0' : 0,
    'a' : 0,
}

OTHER_CONSTRAINTS = {
    'lags_match' : False # whether wage and price lags match each other
}



class Settings:
    """
    A class which contains all settings for the model. This can be used to
    tweak the model. This is then fed to the new generator (which I will update)
    which will return an economy with the specified settings.

    Settings need to include:
    - default values for all parameters
    - default number of sectors
    - whether random values will be generated for certain parameters
    - whether sectors will vary across frequency
    - whether sectors will vary in lag
    - whether wage and price frequencies will match in each sector

    This is a bit clunky but will ultimately make fiddling with the model much
    easier. Then if I want to generate a bunch of different versions of the
    model I can add methods to the class that I call to modify it, then I feed
    the settings object to the economy generator.

    The main idea is to use a dict with 
    """
    
    def __init__(self):
        self.global_defaults = GLOBAL_DEFAULTS
        self.sector_defaults = SECTOR_DEFAULTS
        self.is_default = IS_DEFAULT
        self.rand_max = RAND_MAX
        self.rand_min = RAND_MIN
        self.constraints = OTHER_CONSTRAINTS

    def get_global_default(self, param_name):
        return self.global_defaults[param_name]
    
    def get_sector_default(self, param_name):
        return self.sector_defaults[param_name]
    
    def check_if_default(self, param_name):
        return self.is_default[param_name]
    
    def get_rand_max(self, param_name):
        return self.rand_max[param_name]
    
    def get_rand_min(self, param_name):
        return self.rand_min[param_name]
    
    def lags_match(self):
        return self.constraints['lags_match']
    
    def set_global_default(self, name, value):
        self.global_defaults[name] = value

    def set_sector_default(self, name, value):
        self.sector_defaults[name] = value

    def set_is_default(self, name, value):
        self.is_default[name] = value

    def set_lags_match(self, value):
        self.constraints['lags_match'] = value