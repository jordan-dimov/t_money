from decimal import Decimal
import pytest

from t_money import Money, DifferentCurrencyError


def test_money_with_invalid_currency():
    with pytest.raises(AssertionError):
        Money(10, "US")


def test_money_from_str():
    money = Money.from_str("USD 10.00")
    assert money == Money(10, "USD")


def test_money_from_str_with_spaces():
    money = Money.from_str("USD  10.00")
    assert money == Money(10, "USD")


def test_money_from_str_with_commas():
    money = Money.from_str("USD 10,000.00")
    assert money == Money(10000, "USD")


def test_money_from_str_with_commas_and_spaces():
    money = Money.from_str("USD  10,000.00")
    assert money == Money(10000, "USD")


def test_add():
    money1 = Money(10, "USD")
    money2 = Money(20, "USD")
    assert money1 + money2 == Money(30, "USD")


def test_add_different_currency():
    money1 = Money(10, "USD")
    money2 = Money(20, "EUR")
    with pytest.raises(DifferentCurrencyError):
        money1 + money2


def test_sub():
    money1 = Money(10, "USD")
    money2 = Money(20, "USD")
    assert money1 - money2 == Money(-10, "USD")


def test_sub_different_currency():
    money1 = Money(10, "USD")
    money2 = Money(20, "EUR")
    with pytest.raises(DifferentCurrencyError):
        money1 - money2


def test_mul():
    money = Money(10, "USD")
    assert money * 2 == Money(20, "USD")


def test_rmul():
    money = Money(Decimal("10.56"), "USD")
    assert Decimal("3.14") * money == Money(Decimal("33.1584"), "USD")


def test_convert():
    money = Money(10, "EUR")
    converted = money.convert("USD", Decimal("1.02"))
    assert converted == Money(Decimal("10.2"), "USD")


def test_round_to():
    money = Money(Decimal("10.567"), "USD")
    rounded = money.round_to(2)
    assert rounded == Money(Decimal("10.57"), "USD")


def test_round_to_0():
    money = Money(Decimal("10.567"), "USD")
    rounded = money.round_to(0)
    assert rounded == Money(Decimal("11"), "USD")


def test_neg():
    money = Money(10, "USD")
    assert -money == Money(-10, "USD")


def test_compare():
    money1 = Money(10, "USD")
    money2 = Money(20, "USD")
    assert money1 < money2
    assert money2 > money1
    assert money1 <= money2
    assert money2 >= money1
    assert money1 != money2
    assert money1 == Money(10, "USD")


def test_compare_different_currency():
    money1 = Money(10, "USD")
    money2 = Money(20, "EUR")
    with pytest.raises(DifferentCurrencyError):
        money1 < money2
    with pytest.raises(DifferentCurrencyError):
        money1 > money2
    with pytest.raises(DifferentCurrencyError):
        money1 <= money2
    with pytest.raises(DifferentCurrencyError):
        money1 >= money2
    with pytest.raises(DifferentCurrencyError):
        money1 == money2
    with pytest.raises(DifferentCurrencyError):
        money1 != money2


def test_repr():
    money = Money(10, "USD")
    assert repr(money) == "Money(amount=10, currency='USD')"


def test_str():
    money = Money(10, "USD")
    assert str(money) == "USD 10.00"


def test_sort():
    money1 = Money(40, "USD")
    money2 = Money(20, "USD")
    money3 = Money(Decimal("20.1"), "USD")
    assert sorted([money3, money1, money2]) == [money2, money3, money1]


def test_hash():
    money1 = Money(40, "USD")
    money2 = Money(40, "USD")
    assert hash(money1) == hash(money2)


def test_hash_different_currency():
    money1 = Money(40, "USD")
    money2 = Money(40, "EUR")
    assert hash(money1) != hash(money2)


def test_hash_different_amount():
    money1 = Money(40, "USD")
    money2 = Money(41, "USD")
    assert hash(money1) != hash(money2)


def test_hash_different_amount_and_currency():
    money1 = Money(40, "USD")
    money2 = Money(41, "EUR")
    assert hash(money1) != hash(money2)


def test_set_of_money():
    money1 = Money(40, "USD")
    money2 = Money(40, "USD")
    money3 = Money(Decimal("20.1"), "USD")
    assert set([money1, money2, money3]) == {money1, money3}
