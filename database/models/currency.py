from dataclasses import dataclass


@dataclass
class Currency:
	id: int
	currency_code: str

	__select__ = """ select "id", "currency_code" from currency"""

