
# agent.add_order(True, "IBM", 1000, 100.0)  # Buy 1000 IBM shares at $100 or below
# agent.add_order(False, "TCS", 600, 130.0)  # Sell 500 TCS shares at $110 or above

import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent


class LimitOrderAgentTest(unittest.TestCase):

    def test_buy_order_execution(self):
        mock_client = Mock()
        agent_data = LimitOrderAgent(mock_client)
        agent_data.add_order(True, "IBM", 1000, 100.0)
        agent_data.on_price_tick("IBM", 99.5)
        mock_client.buy.assert_called_once_with("IBM", 1000)

    def test_sell_order_execution(self):
        mock_client = Mock()
        agent_data = LimitOrderAgent(mock_client)
        agent_data.add_order(False, "TCS", 600, 130.0)
        agent_data.on_price_tick("TCS", 130.5)
        mock_client.sell.assert_called_once_with("TCS", 600)


if __name__ == "__main__":
    unittest.main()
