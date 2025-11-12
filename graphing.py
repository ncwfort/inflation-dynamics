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
        plt.show()

    def graph_period_to_period_inflation(self, economy : Economy):
        inflation_data = economy.period_to_period_inflation_series()
        self.basic_plot(inflation_data)
        plt.show()

    def graph_yoy_inflation(self, economy : Economy):
        inflation_data = economy.year_over_year_inflation_series()
        for i in range(len(inflation_data)):
            inflation_data[i] *= 100
        self.basic_plot(inflation_data)
        plt.title("Year Over Year Inflation")
        plt.xlabel("Period")
        plt.ylabel("Inflation Rate (percent)")
        plt.show()

    def graph_ptp_moving_average(self, economy : Economy, window):
        moving_avg = economy.get_ptp_moving_average(window)
        self.basic_plot(moving_avg)
        plt.show()

    def graph_yoy_moving_average(self, economy : Economy, window):
        moving_avg = economy.get_yoy_moving_average(window)
        for i in range(len(moving_avg)):
            moving_avg[i] *= 100
        self.basic_plot(moving_avg)
        plt.title("Year Over Year Inflation - 6 Month Moving Average")
        plt.xlabel("Period")
        plt.ylabel("Inflation Rate (percent)")
        plt.show()

    def basic_plot(self, data_series):
        x_indices = list(range(len(data_series)))
        plt.plot(x_indices, data_series)
        plt.ticklabel_format(useOffset=False)

    