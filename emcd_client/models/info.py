# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = account_info_from_dict(json.loads(json_string))

from config import Coin
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple, TypeVar, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class CoinInfo:
    balance: float
    total_paid: float
    min_payout: float
    address: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CoinInfo':
        assert isinstance(obj, dict)
        balance = from_float(obj.get("balance"))
        total_paid = from_float(obj.get("total_paid"))
        min_payout = from_float(obj.get("min_payout"))
        address = from_union([from_none, from_str], obj.get("address"))
        return CoinInfo(balance, total_paid, min_payout, address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["balance"] = to_float(self.balance)
        result["total_paid"] = to_float(self.total_paid)
        result["min_payout"] = to_float(self.min_payout)
        result["address"] = from_union([from_none, from_str], self.address)
        return result


@dataclass
class Notifications:
    email: int
    telegram: int

    @staticmethod
    def from_dict(obj: Any) -> 'Notifications':
        assert isinstance(obj, dict)
        email = from_int(obj.get("email"))
        telegram = from_int(obj.get("telegram"))
        return Notifications(email, telegram)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_int(self.email)
        result["telegram"] = from_int(self.telegram)
        return result


@dataclass
class AccountInfo:
    username: str
    bitcoin: CoinInfo
    litecoin: CoinInfo
    bitcoin_cash: CoinInfo
    bitcoin_sv: CoinInfo
    dash: CoinInfo
    eth: CoinInfo
    etc: CoinInfo
    notifications: Notifications

    @staticmethod
    def from_dict(obj: Any) -> 'AccountInfo':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        bitcoin = CoinInfo.from_dict(obj.get("bitcoin"))
        litecoin = CoinInfo.from_dict(obj.get("litecoin"))
        bitcoin_cash = CoinInfo.from_dict(obj.get("bitcoin_cash"))
        bitcoin_sv = CoinInfo.from_dict(obj.get("bitcoin_sv"))
        dash = CoinInfo.from_dict(obj.get("dash"))
        eth = CoinInfo.from_dict(obj.get("eth"))
        etc = CoinInfo.from_dict(obj.get("etc"))
        notifications = Notifications.from_dict(obj.get("notifications"))
        return AccountInfo(username, bitcoin, litecoin, bitcoin_cash, bitcoin_sv, dash, eth, etc, notifications)

    def to_dict(self) -> dict:
        result: dict = {}
        result["username"] = from_str(self.username)
        result["bitcoin"] = to_class(CoinInfo, self.bitcoin)
        result["litecoin"] = to_class(CoinInfo, self.litecoin)
        result["bitcoin_cash"] = to_class(CoinInfo, self.bitcoin_cash)
        result["bitcoin_sv"] = to_class(CoinInfo, self.bitcoin_sv)
        result["dash"] = to_class(CoinInfo, self.dash)
        result["eth"] = to_class(CoinInfo, self.eth)
        result["etc"] = to_class(CoinInfo, self.etc)
        result["notifications"] = to_class(Notifications, self.notifications)
        return result
    
    def get_coins(self,) -> Dict[Coin, CoinInfo]:
        coins = {}
        coins.update({Coin.Bitcoin.value: self.bitcoin})
    
        coins.update({Coin.Litecoin.value: self.litecoin})

        coins.update({Coin.BitcoinHash.value: self.bitcoin_cash})

        coins.update({Coin.BitcoinSV.value: self.bitcoin_sv})

        coins.update({Coin.Dash.value: self.dash})

        coins.update({Coin.Ethereum.value: self.eth})

        coins.update({Coin.EthereumClassic.value: self.etc})
        
        return coins;



def account_info_from_dict(s: Any) -> AccountInfo:
    return AccountInfo.from_dict(s)


def account_info_to_dict(x: AccountInfo) -> Any:
    return to_class(AccountInfo, x)
