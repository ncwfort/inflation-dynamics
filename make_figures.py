"""
Regenerates the sample figures shown in README.md.

Run with:

    python make_figures.py

Figures are written to the `figures/` directory. Random seeds are fixed so
that the output matches what is displayed in the README.
"""
import copy
import os
import random as rd

import matplotlib
matplotlib.use('Agg', force=True) # write files instead of opening windows
import matplotlib.pyplot as plt
import numpy as np

import settings as settings_module
from settings import Settings
from gen import Generator
from graphing import GraphingHelper

FIGURE_DIR = 'figures'
SEED = 20251101

# Settings objects share the module-level default dicts, so each run needs its
# own copies to keep one experiment from leaking into the next.
_PRISTINE = {
    'global_defaults': copy.deepcopy(settings_module.GLOBAL_DEFAULTS),
    'sector_defaults': copy.deepcopy(settings_module.SECTOR_DEFAULTS),
    'is_default': copy.deepcopy(settings_module.IS_DEFAULT),
    'rand_max': copy.deepcopy(settings_module.RAND_MAX),
    'rand_min': copy.deepcopy(settings_module.RAND_MIN),
    'constraints': copy.deepcopy(settings_module.OTHER_CONSTRAINTS),
}


def fresh_settings():
    """A Settings object with its own copy of every default, plus a reset RNG."""
    rd.seed(SEED)
    np.random.seed(SEED)
    settings = Settings()
    for name, value in _PRISTINE.items():
        setattr(settings, name, copy.deepcopy(value))
    return settings


def save(filename):
    """Saves the current figure into the figure directory and clears it."""
    path = os.path.join(FIGURE_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close('all')
    print(f"wrote {path}")


# GraphingHelper ends every plot with plt.show(); saving instead of showing
# lets the figures below stay identical to what an interactive run displays.
plt.show = lambda *args, **kwargs: None


def figure_wage_share():
    """
    A single sector with wages and prices both adjusting every other period,
    wages one period out of step with prices. Shows the wage share cycling
    around its equilibrium value.
    """
    settings = fresh_settings()
    settings.set_all_defaults()
    settings.set_sector_default('freq_f', 2)
    settings.set_sector_default('freq_w', 2)
    settings.set_sector_default('lag_w', 2)
    settings.set_global_default('freq_max', 2)
    economy = Generator().generate(settings, 1)
    economy.advance_n(60)
    gr = GraphingHelper()
    gr.simple_graph_wage_share(economy.sectors[0])
    plt.title("Wage Share in a Single Staggered Sector")
    save('wage_share.png')


def figure_aggregate_shock():
    """
    50 sectors with heterogeneous adjustment frequencies and lags, hit by a
    5% price shock to every sector in period 20.
    """
    settings = fresh_settings()
    economy = Generator().generate(settings, 50)
    economy.advance_n(20)
    economy.shock_all_sectors(0.05)
    economy.advance_n(80)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)
    plt.title("Year Over Year Inflation - 5% Aggregate Price Shock")
    save('aggregate_shock.png')


def figure_persistent_shock():
    """
    The same heterogeneous economy, but the shock only reaches a sector when
    that sector's prices are due to update, and it decays at rate ALPHA.
    """
    settings = fresh_settings()
    economy = Generator().generate(settings, 50)
    economy.single_shocks = True
    economy.advance_n(19)
    economy.do_single_shock(0.05)
    economy.advance_n(80)
    gr = GraphingHelper()
    gr.graph_yoy_inflation(economy)
    plt.title("Year Over Year Inflation - Decaying Shock, Staggered Pass-Through")
    save('persistent_shock.png')


def figure_stochastic():
    """
    An economy subject to a persistent, normally distributed aggregate shock
    in every period, smoothed with a 6 period moving average.
    """
    settings = fresh_settings()
    economy = Generator().generate(settings, 50)
    economy.set_stochastic(True)
    economy.advance_n(200)
    gr = GraphingHelper()
    gr.graph_yoy_moving_average(economy, 6)
    save('stochastic.png')


def figure_synchronization():
    """
    Average inflation as a function of the aspiration gap between workers and
    firms, comparing economies where wage and price adjustment are
    synchronized within a sector against economies where they are not.
    """
    n_sims = 20
    n_sectors = 20
    n_periods = 100
    increment = 0.01
    n_steps = 40
    eq_value = 0.6
    results = {}
    for lags_match in (True, False):
        offsets, rates = [], []
        settings = fresh_settings()
        settings.set_lags_match(lags_match)
        gen = Generator()
        for i in range(n_steps):
            offset = (i + 1) * increment
            offsets.append(offset)
            run_rates = []
            for _ in range(n_sims):
                settings.set_global_default('v_w', eq_value + offset / 2)
                settings.set_global_default('v_f', eq_value - offset / 2)
                economy = gen.generate(settings, n_sectors)
                economy.advance_n(n_periods)
                series = economy.year_over_year_inflation_series()
                run_rates.append(sum(series) / len(series))
            rates.append(sum(run_rates) / len(run_rates))
        results[lags_match] = [offsets, rates]
    gr = GraphingHelper()
    gr.compare_lines(results[True], results[False])
    save('synchronization.png')


def main():
    os.makedirs(FIGURE_DIR, exist_ok=True)
    figure_wage_share()
    figure_aggregate_shock()
    figure_persistent_shock()
    figure_stochastic()
    figure_synchronization()


if __name__ == '__main__':
    main()
