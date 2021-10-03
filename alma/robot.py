from threading import Thread
from queue import Queue
from enum import Enum
from alma.message.message import MineMessage, TypeMessage, FinishedMineMessage
import random
import time


class TypeTask(Enum):
    mine_foo = 1
    mine_bar = 2
    join_foobar = 3
    sell = 4


class Robot(Thread):
    """
    class derived from a Thread that will contains all properties and
        function that has a robot

    Robot will receive orders from the shop via the IN Queue, also
        has an Out Queue to ask for new tasks to the shop
    """

    # Constant Times waiting
    TIME_CHANGE_ACTIVITY = 5
    TIME_MINE_FOO = 1
    TIME_MINE_BAR_MINIMUM = 0.5
    TIME_MINE_BAR_MAXIMUM = 2
    TIME_JOIN_FOO_BAR = 2
    TIME_SELL = 10

    def __init__(self, id_robot, in_queue: Queue, out_queue: Queue, speed: int) -> None:
        super(Robot, self).__init__()
        self.id_robot = id_robot
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.last_task = None
        self.speed = speed
        self.counter_foo = 0
        self.counter_bar = 0

    def run(self) -> None:
        self.print_to_console("Initialization of Robot")
        while True:
            message = self.in_queue.get()
            if isinstance(message, MineMessage):
                if message.type_message == TypeMessage.send_job_create_foo:
                    # once we have the message, send foo to the shop
                    self.send_foo_to_shop(self.process_foo())
                else:
                    self.send_bar_to_shop(self.process_bar())
        return

    def process_foo(self):
        """
        Method called when we receive from shop to process a foo

        It will return a new foo generated by the robot
        """
        self.print_to_console("Process Foo")
        # If we change task, wait 5 units of times
        if self.last_task is not None and self.last_task != TypeTask.mine_foo:
            time.sleep(self.TIME_CHANGE_ACTIVITY / self.speed)

        # mine foo cost 1 unit of time
        time.sleep(self.TIME_MINE_FOO / self.speed)
        id_foo = f"{self.id_robot}{self.counter_foo}"
        self.counter_foo += 1
        self.print_to_console(f"Creating Foo {id_foo}")
        return id_foo

    def process_bar(self):
        """
        Method called when we receive from shop to process a bar

        It will return a new generated bar by the robot
        """
        self.print_to_console("Process Bar")
        # If we change task, wait 5 units of times
        if self.last_task is not None and self.last_task != TypeTask.mine_bar:
            time.sleep(self.TIME_CHANGE_ACTIVITY / self.speed)
        # mine bar cost between 0.5 and 2 units of time
        time.sleep(
            random.uniform(self.TIME_MINE_BAR_MINIMUM, self.TIME_MINE_BAR_MAXIMUM)
            / self.speed
        )
        id_bar = f"{self.id_robot}{self.counter_bar}"
        self.counter_bar += 1
        self.print_to_console(f"Creating Bar {id_bar}")

    def send_foo_to_shop(self, id_foo: str):
        """
        Method called after generating the foo

        Send the foo to the shop thanks to the queue
        """
        self.print_to_console(f"Send Foo {id_foo} to Shop")
        message_to_send = FinishedMineMessage(
            TypeMessage.job_finished_foo, self.id_robot, id_foo
        )
        self.out_queue.put(message_to_send)

    def send_bar_to_shop(self, id_bar: str):
        """
        Method called after generating the bar

        Send the bar to the shop thanks to the queue
        """
        self.print_to_console(f"Send Bar {id_bar} to Shop")
        message_to_send = FinishedMineMessage(
            TypeMessage.job_finished_bar, self.id_robot, id_bar
        )
        self.out_queue.put(message_to_send)

    def print_to_console(self, console_message: str):
        """
        Logging Method
        """
        print(f"Robot {self.id_robot}: {console_message}")
