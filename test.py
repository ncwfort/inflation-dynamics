from params import GlobalParams
from economy import Economy
from graphing import GraphingHelper
from sectors import Sector
from generator import EconomyGenerator
from gen import Generator
from settings import Settings


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

def graphing_test():
    n_sectors = 1
    settings = Settings()
    gen = Generator()
    test_economy = gen.generate(settings, n_sectors)
    test_economy.advance_n(150)
    grapher = GraphingHelper()
    grapher.graph_period_to_period_inflation(test_economy)
    grapher.graph_price_index(test_economy)
    grapher.graph_yoy_inflation(test_economy)
    grapher.graph_ptp_moving_average(test_economy, 6)
    grapher.graph_yoy_moving_average(test_economy, 6)

def main():
    """
    n_sectors = 1000
    gen = EconomyGenerator(n_sectors)
    gen.generate_all_sectors()
    test_economy = gen.get_economy()

    test_economy.advance_n(200)
    grapher = GraphingHelper()
    grapher.graph_period_to_period_inflation(test_economy)
    grapher.graph_price_index(test_economy)
    grapher.graph_yoy_inflation(test_economy)
    grapher.graph_ptp_moving_average(test_economy, 6)
    grapher.graph_yoy_moving_average(test_economy, 6)"""
    
    graphing_test()




    


if __name__ == '__main__':
    main()