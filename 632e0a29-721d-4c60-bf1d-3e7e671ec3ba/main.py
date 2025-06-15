from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Dividend

class TradingStrategy(Strategy):
    def __init__(self):
        # A placeholder list of ETF tickers known for monthly dividends.
        # Ideally, this list should be dynamically generated based on the actual top 30 monthly dividend ETFs.
        self.etf_tickers = ["PFF", "SPHD", "VIG", "DVY", "SDIV"]

    @property
    def assets(self):
        # Targets the selected ETFs for the strategy
        return self.etf_tickers

    @property
    def interval(self):
        # Monthly evaluation aligns with the dividend payout frequency
        return "1month"

    @property
    def data(self):
        # No additional data required for this simplistic strategy
        return []

    def run(self, data):
        # Simple allocation - equally divides the investment among the ETFs
        # This could be further refined to consider factors like yield, stability, and performance
        allocation_dict = {etf: 1/len(self.etf_tickers) for etf in self.etf_tickers}

        # The allocation could be dynamically adjusted based on dividend data and other factors if available
        # This code assumes an equal-weight strategy due to limited data scope

        return TargetAllocation(allocation_dict)