from dataclasses import dataclass
from decimal import Decimal
from typing import NewType

CurrencyCode = NewType("CurrencyCode", str)


class DifferentCurrencyError(Exception):
    pass


@dataclass
class Money:
    amount: Decimal
    currency: CurrencyCode

    def __post_init__(self):
        assert len(self.currency) == 3, f"Invalid currency code: {self.currency}"
        self.currency = self.currency.upper()

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"

    @classmethod
    def from_str(cls, money_str: str) -> "Money":
        currency, amount = money_str.split()
        currency = CurrencyCode(currency)
        amount = amount.replace(",", "")
        amount = Decimal(amount)
        return cls(amount, currency)

    def _require_same_currency(self, other):
        if self.currency != other.currency:
            raise DifferentCurrencyError(
                f"Currencies don't match: {self.currency}, {other.currency}"
            )

    def __add__(self, other):
        self._require_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        self._require_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __eq__(self, other):
        self._require_same_currency(other)
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __lt__(self, other):
        self._require_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other):
        self._require_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other):
        self._require_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other):
        self._require_same_currency(other)
        return self.amount >= other.amount

    def __neg__(self):
        return Money(-self.amount, self.currency)

    def __mul__(self, factor: Decimal) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __rmul__(self, factor: Decimal) -> "Money":
        return self * factor

    def convert(self, target_currency: CurrencyCode, exchange_rate: Decimal) -> "Money":
        converted_amount = self.amount * exchange_rate
        return Money(converted_amount, target_currency)

    def round_to(self, decimal_places: int) -> "Money":
        rounded_amount = self.amount.quantize(Decimal(10) ** -decimal_places)
        return Money(rounded_amount, self.currency)

    # Let's make it hashable, so we can use Money in sets and dicts
    def __hash__(self):
        return hash((self.amount, self.currency))
