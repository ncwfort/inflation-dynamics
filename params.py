class GlobalParams:
    """An object that stores the global parameters of the model:
        - v_w: the target wage share for workers
        - v_f: the target wage share of firms
        - mu_bar: the aggregate ability of workers to 
          achieve wage increases over a year
        - phi_bar: the aggregate ability of firms to 
          raise prices over a year
        - f_max: the maximum number of periods it takes any given firm to
          update their prices"""
    
    def __init__(self, v_w, v_f, mu_bar, phi_bar, frequency_max):
        # takes in parameter values as arguments
        self.v_w = v_w
        self.v_f = v_f
        self.mu_bar = mu_bar
        self.phi_bar = phi_bar
        self.frequency_max = frequency_max

    """Method to print the values of all parameters (for testing purposes)."""
    def print_global_params(self):   
        print(f"v_w: {self.v_w}")
        print(f"v_f: {self.v_f}")
        print(f"mu_bar: {self.mu_bar}")
        print(f"phi_bar: {self.phi_bar}")
        print(f"max frequency: {self.frequency_max}")

""" A constant dict used for processing arrays into parameters object.
    Indicates which parameter is stored at which index."""
PARAMETER_INDICES = {
    0 : 'w0',
    1 : 'p0',
    2 : 'a',
    3 : 'phi',
    4 : 'mu',
    5 : 'freq_w',
    6 : 'freq_f',
    7 : 'lag_w',
    8 : 'lag_f',
    9 : 'index_weight'
}

class SectorParams:
    """ An object that stores the local parameters for a given sector, 
        specifications listed below. Initialized with an array of data,
        which is processed according to the constant dict 
        PARAMETER_INDICES. Any param can then be accessed using the get
        method and set using the set method, which requires string arguments
        with the name of the parameter."""

    def __init__(self, raw_param_data, global_params : GlobalParams):
        self.data = {}
        self.global_params = global_params
        for index in PARAMETER_INDICES:
            # get the name of the parameter at index in the array
            param_name = PARAMETER_INDICES[index]
            # convert to a float and store in the class's main data object
            self.data[param_name] = float(raw_param_data[index])
        # need to add the local phi and mu values to the global value
        self.data['phi'] += self.global_params.phi_bar
        self.data['mu'] += self.global_params.mu_bar

    """ Method takes in a string (the name of a parameter) and returns the 
        value associated with that parameter for this sector.""" 
    def get(self, param_name):
        return self.data[param_name]
    
    """ Takes in a string and sets the value of that parementer to the
        value in the argument"""
    def set(self, param_name, value):
        self.data[param_name] = value

    """ Prints out all sector parameters. Used for testing purposes."""
    def print_params(self):
        for key in self.data.keys():
            print(f"{key}: {self.data[key]}")
        print('\n')
