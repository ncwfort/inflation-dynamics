"""
This file contains various experiments I am doing to study the behavior of the
model.
"""
from graphing import GraphingHelper
from settings import Settings
from gen import Generator
from tqdm import tqdm

N_SIMS = 100

def equilibrium_wage(settings : Settings):
    """
    From a settings object, get the global equilibrium value.
    """
    v_w = settings.get_global_default('v_w')
    v_f = settings.get_global_default('v_f')
    return (v_w + v_f) / 2

def gen_simple_staggered_economy():
    settings = Settings()
    settings.set_lags_match(False)
    eq_wage = equilibrium_wage(settings)
    settings.set_sector_default('w0', eq_wage)
    gen = Generator()
    test_economy = gen.generate(settings, 1)
    test_economy.advance_n(100)
    gr = GraphingHelper()
    gr.graph_period_to_period_inflation(test_economy)
    this_sector = test_economy.sectors[0]
    this_sector.params.print_params()

def one_sector_economy(lags_match : bool, n_periods):
    settings = Settings()
    settings.set_lags_match(lags_match)
    eq_wage = equilibrium_wage(settings)
    settings.set_sector_default('w0', eq_wage)
    gen = Generator()
    test_economy = gen.generate(settings, 1)
    test_economy.advance_n(n_periods)
    yoy_inflation = test_economy.year_over_year_inflation_series()
    return sum(yoy_inflation) / len(yoy_inflation)

def get_average_when_lags_match():
    """
    Get the average YoY inflation rate when lags match. All economies have same
    initial conditions and vary over lag structure only.
    """
    inflation_rates = []
    for i in tqdm(range(N_SIMS)):
        inflation_rates.append(one_sector_economy(lags_match=True, 
                                                  n_periods=100))
    return sum(inflation_rates) / len(inflation_rates)

def get_average_no_lag_match():
    inflation_rates = []
    for i in tqdm(range(N_SIMS)):
        inflation_rates.append(one_sector_economy(lags_match=False, 
                                                  n_periods=100))
    return sum(inflation_rates) / len(inflation_rates)


def yoy_inflation_based_on_desire_offset(lags_match : bool, n_sectors, 
                                         n_periods):
    """
    Next: do a 50 sector economy.
    Let the difference between worker and employer targets range from 0.01 to 0.4
    in increments of 0.01.
    """
    increment = 0.01
    desire_offsets = []
    inflation_rate = []
    gen = Generator()
    settings = Settings()
    settings.set_lags_match(lags_match)
    eq_value = 0.6
    for i in tqdm(range(80)):
        desire_offset = (i + 1) * increment
        desire_offsets.append(desire_offset)
        rates = []
        for _ in range(N_SIMS):
            v_w = eq_value + desire_offset / 2
            v_f = eq_value - desire_offset / 2
            settings.set_global_default('v_w', v_w)
            settings.set_global_default('v_f', v_f)
            test_economy = gen.generate(settings, n_sectors)
            test_economy.advance_n(n_periods)
            yoy_inflation = test_economy.year_over_year_inflation_series()
            rates.append(sum(yoy_inflation) / len(yoy_inflation))
        inflation_rate.append(sum(rates) / len(rates))
    return [desire_offsets, inflation_rate]


def compare_lag_constraints():
    lags_match = yoy_inflation_based_on_desire_offset(lags_match=True, 
                                                      n_sectors=50,
                                                      n_periods=100)
    lags_no_match = yoy_inflation_based_on_desire_offset(lags_match=False,
                                                         n_sectors=50,
                                                         n_periods=100)
    gr = GraphingHelper()
    gr.compare_lines(lags_match, lags_no_match)

def completely_random_run(n_sectors, n_periods):
    """
    Does a completely random run of the model, other than the price index.
    """
    settings = Settings()
    settings.set_all_random()
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.advance_n(n_periods)
    gr = GraphingHelper()
    gr.graph_yoy_moving_average(economy, 6)

def simple_staggered_economy(n_periods):
    settings = Settings()
    settings.set_all_defaults()
    settings.set_sector_default('freq_f', 2)
    settings.set_sector_default('freq_w', 2)
    settings.set_sector_default('lag_w', 2)
    settings.set_global_default('freq_max', 2)
    gen = Generator()
    economy = gen.generate(settings, 1)
    economy.advance_n(n_periods)
    gr = GraphingHelper()
    gr.simple_graph_wage_share(economy.sectors[0])
    # have learned that the magnitude of variation around equilibrium wage
    # share in either direction depends on which 'moves first'

def semi_random(n_sectors, n_periods):
    """
    Allowing initial wages share, pricing and bargaining power to vary across
    sectors.
    """
    settings = Settings()
    settings.set_is_default('w0', False)
    settings.set_is_default('phi_i', False)
    settings.set_is_default('mu_i', False)
    settings.rand_min['w0'] = 0.5
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.advance_n(n_periods)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)

def test_shock(n_sectors, n_periods, shock_period, shock_size):
    settings = Settings()
    settings.set_global_default('mu_bar', 0.1)
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.advance_n(shock_period)
    economy.shock_all_sectors(shock_size)
    economy.advance_n(n_periods - shock_period)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)

def test_shock_no_variability(n_sectors, n_periods, shock_period, shock_size):
    settings = Settings()
    settings.set_all_defaults()
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.advance_n(shock_period)
    economy.shock_all_sectors(shock_size)
    economy.advance_n(n_periods - shock_period)
    gr = GraphingHelper()
    gr.graph_period_to_period_inflation(economy)

def run_stochastic(n_sectors, n_periods):
    settings = Settings()
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.set_stochastic(True)
    economy.advance_n(n_periods)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)

def test_single_shocks(n_sectors, n_periods, shock_period, shock_size):
    settings = Settings()
    gen = Generator()
    economy = gen.generate(settings, n_sectors)
    economy.single_shocks = True
    economy.advance_n(shock_period - 1)
    economy.do_single_shock(shock_size)
    economy.advance_n(n_periods - shock_period)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)

def main():
    test_single_shocks(50, 100, 20, 0.05)

if __name__ == '__main__':
    main()