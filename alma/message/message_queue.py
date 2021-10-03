from queue import Queue
from abc import ABC
from alma.message.message import BaseMessage


class BaseMessageQueueException(Exception):
    pass


class ChannelDoesntExistException(BaseMessageQueueException):
    pass


class ChannelAlreadyExistsException(BaseMessageQueueException):
    pass


class MessageQueue(ABC):
    """
        Class to implements a custom basic Message Queue
    """

    def __init__(self) -> None:
        self._channels = dict()

    def initialize_channel(self, key):
        if key in self._channels:
            raise ChannelAlreadyExistsException
        self._channels[key] = Queue()

    def get_channel(self, key) -> Queue:
        if key not in self._channels:
            self.initialize_channel(key)
        return self._channels[key]

    def put_item(self, key, item):
        try:
            self._channels[key].put(item)
        except KeyError:
            raise ChannelDoesntExistException(f"Channel {key} do not exist")   

    def get_item(self, key):
        try:
            return self._channels[key].get()
        except KeyError:
            raise ChannelDoesntExistException(f"Channel {key} do not exist")

    def available_channels(self) -> list:
        return self._channels.keys()


class ShopMessageQueue(MessageQueue):
    """
        Message Queue derived class specifically for this exercise

        It will contain a queue that save all messages the robots send to
            the shop, as well as specific queue for each robot, to receive
            the messages from the shop.
    """    
    def __init__(self) -> None:
        """
            Initialize the Message Queue and the shop channel
        """
        super().__init__()
        # Create the queue for the shop
        self.initialize_channel("SHOP")

    def initialize_robot_channel(self, id_robot):
        self.initialize_channel(id_robot)

    def get_shop_queue(self) -> Queue:
        """
            Method to get the queue related to shop
        """
        return self.get_channel("SHOP")

    def get_robot_queue(self, id_robot):
        """
            Method that returns the queue that correspond to the channel
        """
        return self.get_channel(id_robot)

    def wait_message_from_robots(self) -> BaseMessage:
        """
            Method to get a message sent by a robot
        """
        return self.get_item("SHOP")

    def send_message_to_robot(self, message: BaseMessage, id_robot):
        """
            Method that sends a message to a robot
        """
        self.put_item(id_robot, message)
