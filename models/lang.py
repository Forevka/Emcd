import datetime
import typing
from dataclasses import dataclass


@dataclass
class Lang:
	id: int
	name: str

	__select__ = """ select "id", "name" from lang"""

