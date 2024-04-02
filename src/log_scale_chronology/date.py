import math
import re
from .config import (
    BP_EPOCH, PRESENT, BIG_BANG,
    HEIGHT,
)


class Date:
    """
    Stores dates as a number between 1 (one year ago)
    and 13787000074 (big bang, as of 2024).
    """
    def __init__(self, string: str):
        self.string = string

        number, unit = re.match(r"(?P<number>\d+(\.\d+)?) (?P<year>bya|mya|kya|BC|AD|present)", string).group("number", "year")
        number = float(number)
        if (unit == "bya"):
            number = number * 10**9 - BP_EPOCH + PRESENT
        elif (unit == "mya"):
            number = number * 10**6 - BP_EPOCH + PRESENT
        elif (unit == "kya"):
            number = number * 10**3 - BP_EPOCH + PRESENT
        elif (unit == "BC"):
            number += PRESENT
        elif (unit == "AD"):
            number = PRESENT - number
        elif (unit == "present"):
            number = 1 # Fixed to the very end of the image
        else:
            raise ValueError(f"Unsupported year unit: {unit}")
        self.value = number

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
