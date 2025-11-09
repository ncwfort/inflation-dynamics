import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sectors import Sector
from economy import Economy

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

    def graph_price_index(self, economy : Economy):
        price_index = economy.calculate_price_index()
        self.basic_plot(price_index)

    def graph_period_to_period_inflation(self, economy : Economy):
        inflation_data = economy.period_to_period_inflation_series()
        self.basic_plot(inflation_data)

    def graph_yoy_inflation(self, economy : Economy):
        inflation_data = economy.year_over_year_inflation_series()
        self.basic_plot(inflation_data)

    def basic_plot(self, data_series):
        x_indices = list(range(len(data_series)))
        plt.plot(x_indices, data_series)
        plt.show()

    