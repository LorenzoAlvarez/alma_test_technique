from alma.message.message import FinishedMineMessage, MineMessage, TypeMessage
from alma.message.message_queue import ShopMessageQueue
from alma.robot import Robot

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
        self.robot_counter = 0
        self.speed = speed
        self.money = 0
        # We start with two robots
        self.buy_new_robot()

    def run(self):
        """
            Method that runs the shop
        """
        while True:
            self.print_to_console("waiting to receive message")
            message = self.message_queue.wait_message_from_robots()
            self.print_to_console(message)
            if isinstance(message, FinishedMineMessage):
                self.process_receive_mine_message(message)
                self.send_next_job(message.id_robot)
            else:
                continue
            self.print_inventory()

    def process_receive_mine_message(self, message: FinishedMineMessage):
        """
            Method to process the foo received
        """
        if message.type_message == TypeMessage.job_finished_foo:
            self.print_to_console(f"received foo {message.id_object} from worker {message.id_robot}")
            self.inventory.foo.append(message.id_object)
        else:
            self.inventory.bar.append(message.id_object)

    def send_next_job(self, id_robot):
        """
            Method that decides what task will do later
        """
        if len(self.inventory.foo) < 10:
            message = MineMessage(TypeMessage.send_job_create_foo)
        else:
            message = MineMessage(TypeMessage.send_job_create_bar)
        self.message_queue.send_message_to_robot(message, id_robot)

    def buy_new_robot(self):
        """
            Method that provides the shop the hability to buy robots
        """
        id_robot = self.robot_counter
        shop_queue = self.message_queue.get_shop_queue()
        robot_queue = self.message_queue.get_robot_queue(id_robot)
        robot = Robot(id_robot, robot_queue, shop_queue, self.speed)
        self.send_next_job(id_robot)
        robot.start()

    def print_inventory(self):
        """
            Method that prints the inventory every time we receive a message
        """
        print(f"------ SHOP UPDATE -------")
        print(f"foo: {len(self.inventory.foo)}")
        print(f"bar: {len(self.inventory.bar)}")
        print(f"foobar: {len(self.inventory.foobar)}")
        print(f"Money: {self.money}")
        print(f"--------------------------")

    def print_to_console(self, console_message: str):
        """
            Logging method
        """
        print(f"SHOP: {console_message}")

