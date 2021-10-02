import pytest
from alma.message import (JoinFooBarMessage, MineMessage,
                          NotSupportedTypeMessageException, SellMessage, TypeMessage,
                          NotValidNumberFoosToSellException)


def test_create_mine_message_not_valid():
    with pytest.raises(NotSupportedTypeMessageException):
        message = MineMessage(TypeMessage.job_finished_join)


def test_create_sell_message_wrong_parameters():
    with pytest.raises(NotValidNumberFoosToSellException):
        message = SellMessage(["1", "2"], ["1", "2"])


def test_create_sell_message_good_parameters():
    message = SellMessage(["1"], ["1", "2", "3", "4", "5", "6"])
    assert True


def test_create_finished_message_not_valid():
    with pytest.raises(NotSupportedTypeMessageException):
        message = MineMessage(TypeMessage.job_finished_join)