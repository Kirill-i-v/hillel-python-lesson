class Price:
    conversion_rates_to_chf = {
        "USD": 0.9,
        "EUR": 1.0,
        "CHF": 1.0
    }

    conversion_rates_from_chf = {
        "USD": 1 / 0.9,
        "EUR": 1 / 1.0,
        "CHF": 1.0
    }

    def __init__(self, value: int, currency: str) -> None:
        self.value = value
        self.currency = currency

        if self.currency not in self.conversion_rates_to_chf:
            raise ValueError(f"Unsupported currency: {self.currency}")

    def to_chf(self) -> "Price":
        value_in_chf = self.value * self.conversion_rates_to_chf[self.currency]
        return Price(int(value_in_chf), "CHF")

    def convert(self, to: str) -> "Price":
        if to not in self.conversion_rates_from_chf:
            raise ValueError(f"Unsupported currency: {to}")

        chf_price = self.to_chf().value

        new_value = chf_price * self.conversion_rates_from_chf[to]
        return Price(int(new_value), to)

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            result = self.to_chf().value + other.to_chf().value
            return Price(int(result), "CHF").convert(self.currency)

    def __sub__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            result = self.to_chf().value - other.to_chf().value
            return Price(int(result), "CHF").convert(self.currency)

    def __repr__(self) -> str:
        return f"{self.value} {self.currency}"


a = Price(100, "USD")
b = Price(100, "USD")
c = Price(100, "EUR")

print(a + b)
print(a - b)
print(a + c)
print(a - c)
