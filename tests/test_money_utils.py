import json
from _decimal import Decimal

from t_money import Money
from money_utils import money_deserializer, money_serializer


def test_money_serializer():
    money = Money.from_str("USD 10.30")
    assert money_serializer(money) == {
        "_type": "Money",
        "amount": Decimal("10.30"),
        "currency": "USD",
    }


def test_money_deserializer():
    money = Money.from_str("USD 10.30")
    assert (
        money_deserializer({"_type": "Money", "amount": "10.30", "currency": "USD"})
        == money
    )


def test_money_deserializer_not_money():
    assert money_deserializer({"amount": "10.30", "currency": "USD"}) == {
        "amount": "10.30",
        "currency": "USD",
    }


def test_with_json():
    money = Money.from_str("USD 10.30")
    sample_dict = {"account": "expenses", "account_id": 3, "total": money}
    json_str = json.dumps(sample_dict, default=money_serializer)
    assert json.loads(json_str, object_hook=money_deserializer) == sample_dict
