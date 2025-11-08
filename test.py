from params import GlobalParams
from economy import Economy
from graphing import GraphingHelper
from rw import get_params


def get_equilibrium(sector):
    params = sector.params
    return (params.mu * params.global_params.v_w + 
            params.phi * params.global_params.v_f) / (params.mu + params.phi)

def test_single_sector():
    v_w = 0.7
    v_f = 0.3
    mu_bar = 0.5
    phi_bar = 0.5
    f_max = 12
    global_params = GlobalParams(v_w, v_f, mu_bar, phi_bar, f_max)
    economy = Economy(global_params)

    w0 = 0.6
    p0 = 1
    a = 1
    phi = 0
    mu = 0
    freq_w = 12
    freq_f = 12
    lag_w = 6
    lag_f = 12
    economy.add_sector(w0, p0, a, phi, mu, freq_w, freq_f, lag_w, lag_f)
    economy.advance_n(1000)
    this_sector = economy.get_sector(0)
    wage_shares = this_sector.get_wage_share_time_series()
    equilibrium = get_equilibrium(this_sector)
    print(wage_shares)
    print(equilibrium)
    graphing_helper = GraphingHelper()
    graphing_helper.simple_graph_wage_share(wage_shares, equilibrium)
    graphing_helper.graph_wages_prices(this_sector)

def main():
    get_params("test_csv.csv")


    


if __name__ == '__main__':
    main()