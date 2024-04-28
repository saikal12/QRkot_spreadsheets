from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def close_invest(obj):
    obj.fully_invested = True
    obj.close_date = datetime.now()


def donation_investing(
        target: Union[Donation, CharityProject],
        sources: List[Union[Donation, CharityProject]]
) -> Union[Donation, CharityProject]:
    while sources and (target.invested_amount is None or target.full_amount > target.invested_amount):
        source = sources.pop()
        need_investing = source.full_amount - source.invested_amount
        if target.full_amount > need_investing:
            target.invested_amount += need_investing
        else:
            target.invested_amount = target.full_amount
            close_invest(target)
            source.invested_amount += target.full_amount

            if source.invested_amount == source.full_amount:
                close_invest(source)

    return target
