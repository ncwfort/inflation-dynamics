import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sectors import Sector

class GraphingHelper:

    def __init__(self):
        pass

    def simple_graph_wage_share(self, sector : Sector):
        wage_share_data = sector.get_wage_share_time_series()
        x_indices = list(range(len(wage_share_data)))
        plt.plot(x_indices, wage_share_data)
        plt.axhline(y = sector.get_equilibrium())
        plt.show()

    def graph_wages_prices(self, sector):
        x_indices = list(range(sector.get_n_periods()))
        plt.plot(x_indices, sector.wages)
        plt.plot(x_indices, sector.prices)
        plt.show()