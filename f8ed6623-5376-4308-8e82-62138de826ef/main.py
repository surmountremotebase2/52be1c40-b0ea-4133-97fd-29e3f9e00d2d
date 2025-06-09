from surmount.base_class import Strategy, TargetAllocation
from surmount.data import IndustriesPERatio
from collections import defaultdict

class TradingStrategy(Strategy):
    def __init__(self):
        # Ideally, this list would be dynamically generated based on some criteria
        # For simplicity, we're using a static list of tickers known to belong to diverse industries
        self.tickers = ["AAPL", "XOM", "JPM", "T", "PFE", "WMT"]  # Example tickers from different industries
        self.industries = ["Technology", "Oil & Gas", "Financials", "Telecommunications", "Healthcare", "Consumer Goods"]
        # Data list should include PE ratio for each industry we're interested in
        self.data_list = [IndustriesPERatio("NYSE") for _ in self.industries]

    @property
    def interval(self):
        # Set the interval to daily for this strategy
        return "1day"

    @property
    def assets(self):
        # The assets we are interested in are the tickers we selected
        return self.tickers

    @property
    def data(self):
        # Return the list of data we need, i.e., PE ratios for industries
        return self.data_list

    def run(self, data):
        allocations = defaultdict(float)
        industry_allocations = self._calculate_industry_allocations(data)

        for ticker in self.tickers:
            industry = self._get_ticker_industry(ticker)
            allocations[ticker] = industry_allocations[industry] / self.tickers.count(ticker)  # Equal weight within the industry

        total_alloc = sum(allocations.values())

        # Normalize allocations so they sum up to 1
        for ticker in allocations:
            allocations[ticker] /= total_alloc

        return TargetAllocation(allocations)

    def _calculate_industry_allocations(self, data):
        """
        Calculate the allocation for each industry based on PE ratios
        Returns a dictionary with industry as key and allocation as value
        """
        pe_ratios = self._get_pe_ratios(data)
        total_pe = sum(pe_ratios.values())
        industry_allocations = {industry: pe / total_pe for industry, pe in pe_ratios.items()}
        return industry_allocations

    def _get_pe_ratios(self, data):
        """
        Extracts and calculates the average PE ratio for the industries of interest
        Returns a dictionary with industry as key and average PE ratio as value
        """
        pe_ratios = {}
        for industry_data in data[("industries_pe_ratio", "NYSE")]:
            if industry_data["industry"] in self.industries:
                pe_ratios[industry_data["industry"]] = float(industry_data["pe"])
        return pe_ratios

    def _get_ticker_industry(self, ticker):
        """
        Returns the industry for the given ticker. This would typically require access
        to a mapping of tickers to industries or an API call.
        """
        # This is a placeholder method; in practice, you would need a reliable way
        # to map tickers to industries, perhaps via an external dataset or API.
        ticker_industry_map = {
            "AAPL": "Technology",
            "XOM": "Oil & Gas",
            "JPM": "Financials",
            "T": "Telecommunications",
            "PFE": "Healthcare",
            "WMT": "Consumer Goods"
        }
        return ticker_industry_map[ticker]