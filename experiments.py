"""
This file contains various experiments I am doing to study the behavior of the
model.
"""
from graphing import GraphingHelper
from settings import Settings
from gen import Generator
from tqdm import tqdm

N_SIMS = 10_000

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

"""
Next: do a 50 sector economy.
Let the difference between worker and employer targets range from 0.01 to 0.4
in increments of 0.4.
"""

def main():
    print(get_average_when_lags_match())
    print(get_average_no_lag_match())


if __name__ == '__main__':
    main()