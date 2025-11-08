class GlobalParams:
    """An object that stores the global parameters of the model:
        - v_w: the target wage share for workers
        - v_f: the target wage share of firms
        - mu_bar: the aggregate ability of workers to achieve wage increases over a year
        - phi_bar: the aggregate ability of firms to raise prices over a year
        - f_max: the maximum number of periods it takes any given firm to update their prices"""
    
    def __init__(self, v_w, v_f, mu_bar, phi_bar, frequency_max):
        self.v_w = v_w
        self.v_f = v_f
        self.mu_bar = mu_bar
        self.phi_bar = phi_bar
        self.frequency_max = frequency_max

class Params:
    """An object that stores the local parameters for a given sector, specifications listed below."""

    def __init__(self, global_params, w0, p0, a, phi, mu, freq_w, freq_f, lag_w, lag_f, index_weight):
        self.global_params = global_params
        self.w0 = w0 # create wage vector with initial wage
        self.p0 = p0 # create price vector with initial prices
        self.phi = phi + global_params.phi_bar # parameter governing how rapidly prices change
        self.mu = mu + global_params.mu_bar # parameter governing how quickly wages change
        self.a = a # labor / output ratio
        self.freq_w = freq_w # frequency with which wages change
        self.freq_f = freq_f # frequency with which prices change
        self.lag_w = lag_w # the first period in which wages change
        self.lag_f = lag_f # the first period in which prices change
        self.index_weight = index_weight # the weight in price and wage indices
