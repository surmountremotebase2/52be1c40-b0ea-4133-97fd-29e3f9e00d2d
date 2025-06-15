from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Dividend, Ratios

class TradingStrategy(Strategy):
    def __init__(self):
        # Populate this list with the tickers you are interested in
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "BRK.B", "JNJ", "V", "PG"]
        
        # Prepare data list with Dividend and Ratios data for each ticker.
        self.data_list = [Dividend(ticker) for ticker in self.tickers] + [Ratios(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1day"  # Using daily data for this strategy

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            dividend_key = ("dividend", ticker)
            ratios_key = ("ratios", ticker)
            
            # Check if both dividend and ratio data are available
            if dividend_key in data and ratios_key in data and data[dividend_key] and data[ratios_key]:
                # Get the latest dividend yield
                latest_dividend = data[dividend_key][-1]['adjDividend']
                
                # Get the latest debt to equity ratio
                latest_ratios = data[ratios_key][-1]
                debt_to_equity_ratio = latest_ratios.get('debtEquityRatio', 0)
                
                # Criteria for high-yield, low-risk selection
                if latest_dividend > 0 and debt_to_equity_ratio < 1.0: 
                    # Basic ranking could be improved with more nuanced scoring
                    allocation_dict[ticker] = latest_dividend / 10.0  # Simplified allocation based on dividend
                else:
                    allocation_dict[ticker] = 0
            else:
                allocation_dict[ticker] = 0  # No allocation if data is missing

        # Normalize allocations to ensure they sum up to 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 0:
            allocation_dict = {ticker: val/total_allocation for ticker, val in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)