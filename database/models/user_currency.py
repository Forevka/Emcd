from dataclasses import dataclass


@dataclass
class UserCurrency:
	user_id: int
	currency_id: int
	currency_code: str

	__select__ = """ select "user_id", "currency_id", c."currency_code" from user_currency uc join "currency" c on c.id = uc.currency_id"""

