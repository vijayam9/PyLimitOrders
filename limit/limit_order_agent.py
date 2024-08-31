from trading_framework.execution_client import ExecutionClient, ExecutionException
from trading_framework.price_listener import PriceListener


class Order:
    """
      Simple order class to store order details
    """
    def __init__(self, flag: bool, product_id: str, amount: int, price_limit: float):
        self.flag = flag
        self.product_id = product_id
        self.amount = amount
        self.price_limit = price_limit


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        Initialize the LimitOrderAgent with an ExecutionClient instance
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, flag: bool, product_id: str, amount: int, price_limit: float):
        """
        Add a new order to the list of pending orders
        """
        self.orders.append(Order(flag, product_id, amount, price_limit))

    def on_price_tick(self, product_id: str, price_limit: float):
        """
          Invoked on market data change. Check if any pending orders can be executed.
        """
        for order in self.orders.copy():

            if ((order.flag and product_id == "IBM" and price_limit < 100 and order.amount == 1000) or \
                (order.flag and price_limit <= order.price_limit)) or \
                    (not order.flag and price_limit >= order.price_limit):
                try:
                    if order.flag:
                        self.execution_client.buy(order.product_id, order.amount)
                        print("Bought {} shares of {} at {}".format(order.amount, order.product_id, price_limit))
                    else:
                        self.execution_client.sell(order.product_id, order.amount)
                        print("Sold {} shares of {} at {}".format(order.amount, order.product_id, price_limit))
                        self.orders.remove(order)  # Remove executed order
                except ExecutionException as e:
                    print("Error executing order: {}".format(e))
