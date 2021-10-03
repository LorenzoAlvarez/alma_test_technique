from alma.message.message_queue import ShopMessageQueue


class Inventory():
    def __init__(self) -> None:
        self.foo = list()
        self.bar = list()
        self.foobar = list()


class Shop:
    """
        Main class that contais all functions and properties to run the shop.
        Including the Inventory class, that contains the different objects that
            are on stocks and the datastructure of messageQueue
    """
    def __init__(self, speed: int) -> None:
        """
            Constructor of the class

            It will initialize all variables

            - Inventory
            - Channels to comunicate
        """
        self.inventory = Inventory()
        self.message_queue = ShopMessageQueue()

    def run(self):
        while True:
            message = self.message_queue.wait_for_message_from_robots()

