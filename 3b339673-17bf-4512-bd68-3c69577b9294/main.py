from surmount.base_class import Strategy, TargetAllocation
from surmount.data import CorporateProfitAfterTax, StLouisFinancialStressIndex, Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # We focus on defensive assets (e.g., gold and treasury bills)
        self.tickers = ["GLD", "SHY"]  # GLD for gold ETF, SHY for short-term treasury ETF
        self.data_list = [
            CorporateProfitAfterTax(),
            StLouisFinancialStressIndex(),
            Asset("GLD"),
            Asset("SHY")
        ]
        
    @property
    def interval(self):
        # Using daily data for macroeconomic indicators
        return "1day"
    
    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {"GLD": 0.5, "SHY": 0.5}  # Initial equal allocation to both assets

        # Access corporate profits and financial stress index data
        profits = data[("corporate_profit_after_tax",)]
        stress_index = data[("stlouis_financial_stress_index",)]
        
        # Check the latest data for signs of economic trouble
        if profits and stress_index:
            latest_profits = profits[-1]["value"]
            latest_stress = stress_index[-1]["value"]
            
            # If there's a decrease in corporate profits or increase in financial stress,
            # it might indicate economic trouble, increase allocation to treasury bills for safety.
            if latest_profits < 0 or latest_stress > 0:
                allocation_dict["GLD"] = 0.3  # Decrease allocation to gold
                allocation_dict["SHY"] = 0.7  # Increase allocation to treasury bills
        
        return TargetAllocation(allocation_dict)