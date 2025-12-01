import matplotlib
matplotlib.use('TkAgg') # don't know why I did this, but it helped with my bugs
import matplotlib.pyplot as plt
from sectors import Sector
from economy import Economy

class GraphingHelper:
    """
    This class handles all graphing that I need to do. Right now, it just
    consists of a series of functions that are fed a list of data, then
    plot the data value against the index of the data.
    """

    def __init__(self):
        # nothing happens
        pass

    def simple_graph_wage_share(self, sector : Sector):
        """
        Graphs the wage share of a sector over time.

        sector: Sector's wage share to be graphed.
        """
        wage_share_data = sector.get_wage_share_time_series()
        self.basic_plot(wage_share_data)
        plt.axhline(y = sector.get_ws_equilibrium()) #plot equilibrium as well
        plt.show()

    def graph_wages_prices(self, sector):
        """
        Graphs both wages and prices on the same plot.
        """
        self.basic_plot(sector.wages)
        self.basic_plot(sector.prices)
        plt.show()

    def graph_price_index(self, economy : Economy):
        """
        Graphs a price index over time.
        """
        price_index = economy.calculate_price_index()
        self.basic_plot(price_index)
        plt.show()

    def graph_period_to_period_inflation(self, economy : Economy):
        """
        Graphs a period to period inflation rate.
        """
        inflation_data = economy.period_to_period_inflation_series()
        convert_to_percent(inflation_data)
        self.basic_plot(inflation_data)
        plt.show()

    def graph_yoy_inflation(self, economy : Economy):
        """
        Graphs a year over year inflation rate. (Convention being that one
        year is 12 periods.)
        """
        inflation_data = economy.year_over_year_inflation_series()
        convert_to_percent(inflation_data)
        self.basic_plot(inflation_data)
        plt.title("Year Over Year Inflation")
        plt.xlabel("Period")
        plt.ylabel("Inflation Rate (percent)")
        plt.show()

    def graph_ptp_moving_average(self, economy : Economy, window):
        """Graphs a moving average of inflation data with some specified
        window over which the average is calculated."""
        moving_avg = economy.get_ptp_moving_average(window)
        convert_to_percent(moving_avg)
        self.basic_plot(moving_avg)
        plt.show()

    def graph_yoy_moving_average(self, economy : Economy, window):
        """Graphs a moving average of inflation data with some specified
        window over which the average is calculated."""
        moving_avg = economy.get_yoy_moving_average(window)
        convert_to_percent(moving_avg)
        self.basic_plot(moving_avg)
        plt.title(f"\"Year Over Year\" Inflation - {window} Month Moving Average")
        plt.xlabel("Period")
        plt.ylabel("Inflation Rate (percent)")
        plt.show()

    def basic_plot(self, data_series):
        """
        Basic plotting functionality used by other objects. Plots the index of
        a list object on the x-axis against the value at that point on the
        y-axis.

        data_series: list of data
        """
        x_indices = list(range(len(data_series))) # get a list with all indices
        plt.plot(x_indices, data_series)
        plt.ticklabel_format(useOffset=False)
    
    def compare_lines(self, series_a, series_b):
        a_x = series_a[0]
        a_y = series_a[1]
        b_x = series_b[0]
        b_y = series_b[1]
        plt.plot(a_x, a_y, label='Prices and Wages Change in Sync')
        plt.plot(b_x, b_y, color = 'red',
                 label = 'Prices and Wages Change Randomly')
        plt.xlabel("Aspiration Gap (v_w - v_f)")
        plt.ylabel("Average Inflation Rate")
        plt.title("Relationship Between Wage-Price Change Synchronization" + 
                  " and Average Inflation Rate")
        plt.legend()
        plt.show()


def convert_to_percent(data_series):
    """
    Free-standing function that takes in a data series and multiplies every
    value in it by 100 to turn it into a percent.
    """
    for i in range(len(data_series)):
        data_series[i] *= 100



    