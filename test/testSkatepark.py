#testSkatepark.py
#By: Sam Schmitz
#test code for skatepark

import unittest
from unittest.mock import MagicMock
from datetime import datetime
import datetime

import sb.skatepark

def _getTrades(date):
    return [['MSFT', 'BUY', datetime.datetime(2023, 8, 1), datetime.datetime(2023, 8, 15), 'Joe Biden'], ['AMZN', 'SELL', datetime.datetime(2023, 8, 25), datetime.datetime(2023, 8, 30), 'Joe Biden']]

sb.skatepark.getTrades = MagicMock()
sb.skatepark.getTrades.side_effect = _getTrades

from sb.skatepark import skatepark

class testSkatepark(unittest.TestCase):

    def setUp(self):
        self.skatepark = skatepark(run=False)
        self.skatepark.server = MagicMock()
        self.date = datetime.datetime(2023, 10, 22)

    def test_sb_calls_congressTrades(self):
        self.skatepark.sb(self.date)
        sb.skatepark.getTrades.assert_called_with(self.date)

    def test_sb_calls_add_trades(self):
        self.skatepark.sb(self.date)
        self.skatepark.server.add_trades.assert_called_with([['MSFT', 'BUY', datetime.datetime(2023, 8, 1, 0, 0), datetime.datetime(2023, 8, 15), 'Joe Biden'], ['AMZN', 'SELL', datetime.datetime(2023, 8, 25, 0, 0), datetime.datetime(2023, 8, 30), 'Joe Biden']])


if __name__ == "__main__":
    unittest.main()
