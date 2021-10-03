from abc import ABC
from enum import Enum


class BaseMessageException(Exception):
    pass


class NotSupportedTypeMessageException(BaseMessageException):
    pass


class NotValidNumberFoosToSellException(BaseException):
    pass


class TypeMessage(Enum):
    """
        This Enum provides the different types of messages that can be 
        on the Queue
        
        The first 4 actions are the the kind of messages that can send
        the shop to the workers

        From 5 to is the kind of message that can send the workers
        to the shop owner
    """
    send_job_create_foo = 1
    send_job_create_bar = 2
    send_job_join_foo_bar = 3
    send_job_sell = 4
    job_finished_foo = 5
    job_finished_bar = 6
    job_finished_join = 7
    job_finished_sell = 8
    turn_off_robot = 9
    turn_off_done = 10


class BaseMessage(ABC):
    """
        Basic class for message, this is an abstract class and should not
        be implemented

        From this class we will create the specific class for all kind
        of actions
    """
    def __init__(self, type_message: TypeMessage):
        self.type_message = type_message


class MineMessage(BaseMessage):
    """
        Child Class from Message, it will save the messages of type
            - TypeMessage.send_job_create_foo
            - TypeMessage.send_job_create_bar

        Basicly, this messages does not contain any kind of extra information,
        that's why we can group it
    """
    def __init__(self, type_message: TypeMessage):
        """
            Constructor of the class

            If the type of message is not the right one, send Exception
        """
        available_messages = [
            TypeMessage.send_job_create_foo,
            TypeMessage.send_job_create_bar,
        ]
        if type_message not in available_messages:
            raise NotSupportedTypeMessageException
        super().__init__(type_message)


class JoinFooBarMessage(BaseMessage):
    """
        Child class for messages that send from owner to worker to join
        a foo and a bar objects

        We should save on the message the id of the foo and the id of the bar
    """
    def __init__(self, id_foo: str, id_bar: str):
        super().__init__(TypeMessage.send_job_join_foo_bar)
        self.id_foo = id_foo
        self.id_bar = id_bar


class SellMessage(BaseMessage):
    """
        Child Class from Message, it will save the messages of type
            - TypeMessage.send_job_sell

        This message are sent by the owner when want that a worker try
            to sell some foobars

        We should save the list of "foobars" and foos the robot will sell
    """
    def __init__(self, foobars: list, foos: list): 
        """
            Constructor of the class

            If the type of message is not the right one, send Exception
        """
        # we must verify that len of foos is 6 times the len of foobars
        # If not, raise exception
        print(6*len(foobars), len(foos))
        if 6*len(foobars) != len(foos):
            raise NotValidNumberFoosToSellException
        super().__init__(TypeMessage.send_job_sell)
        self.foobars = foobars
        self.foos = foos


class FinishedMineMessage(BaseMessage):
    """
        Child Class from Message, it will save the messages of type
            - TypeMessage.job_finished_foo
            - job_finished_bar

        This kind of messages are sended by the robot when he finish
        the action of creating a foo or creating a bar
        
        - We should save the worker that has sent the message
        - We should save the id of the object created, so the owner can take it
            and save it on the shop properly
    """
    def __init__(self, type_message: TypeMessage, id_worker: int, id_object_created: str):
        """
            Constructor of the class
        """
        available_messages = [
            TypeMessage.send_job_create_foo,
            TypeMessage.send_job_create_bar,
        ]
        if type_message not in available_messages:
            raise NotSupportedTypeMessageException
        super().__init__(type_message)
        self.worker = id_worker
        self.id_object = id_object_created


class FinishedJoinMessage(BaseMessage):
    """
        Child class from Message

        This messages are sent by the robot to the shop, to send the final object
            of the process of join a foo and a bar

        We have to save the result of the process, if it has finished successfully or not
        Also we should save the id, so the shop can save it into the stock
    """
    def __init__(self,
                 id_worker: int,
                 is_finished_succesfully: bool,
                 id_object: str):
        """
            Constructor of the class
        """
        super().__init__(TypeMessage.job_finished_join)
        self.worker = id_worker
        self.is_finished_succesfully = is_finished_succesfully
        self.id_object = id_object


class FinishedSellMessage(BaseMessage):
    """
        Child class from Message

        This messsages are send by robot to note tha the process of selling foobars
            has been ended

        It contains the worker who sold the foobars and the amount of money gained
            by the sale
    """
    def __init__(self,
                 id_worker: int,
                 amout_of_money_gained: int):
        """
            Constructor of the class
        """
        super().__init__(TypeMessage.job_finished_sell)
        self.worker = id_worker
        self.amount = amout_of_money_gained


class TurnOffRobotMessage(BaseMessage):
    """
        Child class from Message

        This message is sent when we try to turn of the thread
    """
    def __init__(self):
        super().__init__(TypeMessage.turn_off_robot)


class RobotIsOff(BaseMessage):
    """
        Child class from Message

        this message is sent from the robot to the shop, when the robot is off
    """
    def __init__(self, id_worker: int):
        super().__init__(TypeMessage.turn_off_done)