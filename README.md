# Money dataclass
Advanced Python 3.10 Dataclass for handling monetary values, keeping amount and currency together

This `Money` class provides a simple and efficient way to manage amounts of money and perform arithmetic operations and comparisons on them. It supports different currencies and ensures that the operations are only performed on matching currencies to avoid inconsistencies.

## Features

- Initialize a `Money` object with a specific amount and currency.
- Perform arithmetic operations between `Money` objects with the same currency.
- Compare and sort `Money` objects.
- Convert a `Money` object to another currency.
- Round a `Money` object to a specified number of decimal places.
- Serialize and deserialize `Money` objects to/from JSON.

## Usage

    from t_money import Money

### Creating a Money object

```python
usd = Money(Decimal("10.50"), "USD")
```

### Create a Money object from string

```python
usd_from_str = Money.from_str("USD 5.25")
```

### Arithmetic operations

```python
usd1 = Money(Decimal("10.50"), "USD")
usd2 = Money(Decimal("5.50"), "USD")

usd_sum = usd1 + usd2
usd_difference = usd1 - usd2
usd_product = usd1 * Decimal("2")
```

### Comparisons

```python
print(usd1 == usd2)
print(usd1 < usd2)
```

### Rounding

```python
rounded_usd = usd1.round_to(1)
```

### Currency conversion

```python
eur = usd.convert("EUR", Decimal("0.85"))
```

### Serialization and deserialization

```python
import json

# Serialize data containing Money object
data = {'money': usd}
json_str = json.dumps(data, default=money_serializer)

# Deserialize JSON data to Money object
loaded_data = json.loads(json_str, object_hook=money_deserializer)
```

## Error Handling

When performing operations on `Money` objects with different currencies, a `DifferentCurrencyError` will be raised. Make sure to handle this error if necessary when dealing with multiple currencies.


