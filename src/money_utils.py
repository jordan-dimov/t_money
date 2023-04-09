from _decimal import Decimal
from dataclasses import asdict

from t_money import Money


def money_serializer(obj):
    if isinstance(obj, Money):
        result = asdict(obj)
        result["_type"] = "Money"
        return result
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def money_deserializer(dct):
    if (
        dct.get("_type") == "Money"
    ):  # Check if the _type field is present and set to 'Money'
        return Money(Decimal(dct["amount"]), dct["currency"])
    return dct
