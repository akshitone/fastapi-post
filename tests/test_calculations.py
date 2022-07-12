import pytest
from app.calculations import add, BankAccount


@pytest.mark.parametrize('num1, num2, sum', [
    (3, 10, 13), (5, 10, 15), (10, 15, 25)
])
def test_calculations_of_sum(num1, num2, sum):
    assert add(num1, num2) == sum


@pytest.fixture
def zero_balance_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account_with_balance():
    return BankAccount(1000)


def test_bank_set_starting_balance(bank_account_with_balance):
    assert bank_account_with_balance.balance == 1000


def test_bank_default_balance(zero_balance_bank_account):
    assert zero_balance_bank_account.balance == 0


def test_deposit_amount(bank_account_with_balance):
    bank_account_with_balance.deposit(50)
    assert bank_account_with_balance.balance == 1050


def test_withdraw_amount(bank_account_with_balance):
    bank_account_with_balance.withdraw(50)
    assert bank_account_with_balance.balance == 950


@pytest.mark.parametrize('deposited_amount, withdrawal_amount, final_balance', [
    (500, 1000, 500), (100, 1100, 0), (300, 700, 600)
])
def test_bank_transaction(bank_account_with_balance, deposited_amount, withdrawal_amount, final_balance):
    bank_account_with_balance.deposit(deposited_amount)
    bank_account_with_balance.withdraw(withdrawal_amount)
    assert bank_account_with_balance.balance == final_balance


def test_insufficient_balance(zero_balance_bank_account):
    with pytest.raises(Exception):
        zero_balance_bank_account.withdraw(200)
