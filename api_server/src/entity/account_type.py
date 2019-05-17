# coding=utf-8
from dataclasses import dataclass


@dataclass()
class AccountType:
    Adherent = 'adherent'
    Club = 'club'
    Event = 'event'


ALL_ACCOUNT_TYPES = {AccountType.Adherent, AccountType.Club, AccountType.Event}