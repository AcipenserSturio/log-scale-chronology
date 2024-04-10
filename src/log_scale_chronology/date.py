import math
import re
from .config import (
    BP_EPOCH, PRESENT, BIG_BANG,
    HEIGHT,
)


DATE_PATTERN = r"""
(?P<number>\d+(\.\d+)?)
(?P<month>-\d+)?
(?P<day>-\d+)?
 (?P<unit>bya|mya|kya|BC|AD|present|ky before 2015)
""".replace("\n", "")


class Date:
    """
    Stores dates as a number between 1 (one year ago)
    and 13787000074 (big bang, as of 2024).
    """
    def __init__(self, string: str):
        self.string = string

        number, month, day, unit = (
            re.match(DATE_PATTERN, string)
            .group("number", "month", "day", "unit")
        )
        number = float(number)
        if (unit == "bya"):
            number = number * 10**9 - BP_EPOCH + PRESENT
        elif (unit == "mya"):
            number = number * 10**6 - BP_EPOCH + PRESENT
        elif (unit == "kya"):
            number = number * 10**3 - BP_EPOCH + PRESENT
        elif (unit == "ky before 2015"):
            number = number * 10**3 - 2015 + PRESENT
        elif (unit == "BC"):
            number += PRESENT
        elif (unit == "AD"):
            number = PRESENT - number
        elif (unit == "present"):
            number = 1 # Fixed to the very end of the image
        else:
            raise ValueError(f"Unsupported year unit: {unit}")

        if month and not day:
            month = int(month[1:])
            number -= (month-1) / 12
        if month and day:
            month = int(month[1:])
            day = int(day[1:])
            # Technically not accurate.
            # An accurate implementation would take into account
            # Varying lengths of months, leap years.
            # Since all we want is a tack on a timeline,
            # It doesn't matter, this is good enough.
            number -= (month-1) / 12 + (day-1) / 365

        self.value = number

    def __str__(self):
        return f"Date({self.string})"

    @property
    def percentile(self) -> float:
        """
        Returns value in the form of [0, 1],
        where Big Bang = 0,
        one year ago = 1.
        """
        return 1 - math.log(self.value) / math.log(BIG_BANG)

    @property
    def y(self) -> int:
        """
        Returns value in the form of [0, HEIGHT],
        where Big Bang = 0,
        one year ago = HEIGHT.
        """
        return round(self.percentile * HEIGHT)
        # Non logarithmic option:
        # return round((1 - self.value / BIG_BANG) * HEIGHT)
