from __future__ import annotations
import re
from dataclasses import dataclass

class Time:
    _RE = re.compile(
        r'^\s*(1[0-2]|0?[1-9])'          # hour 1..12
        r'(?:\s*:\s*([0-5]?\d))?'       # allow single digit minute
        r'\s*([AaPp][Mm])\s*$'          # AM/PM
    )

    def __init__(self, s: str):
        # 9:00 AM", "12:15 pm
        m = self._RE.match(s)
        if not m:
            raise ValueError(f"invalid time format: {s!r}")
        try:
            hour = int(m.group(1))
            minute = 0 if not m.group(2) else int(m.group(2))
            ampm = m.group(3).upper()
            if ampm == "AM":
                if hour == 12:
                    hour = 0
            else:  # PM
                if hour != 12:
                    hour += 12
            self.minutes = hour * 60 + minute  # 0..1439
        except TypeError as e:
            print(f'Something wrong with {s}')
            print(f"hour, min, ampm = {m.group(1)}, {m.group(2)}, {m.group(3).upper()}")
            raise e

    def __str__(self):
        h = self.minutes // 60
        m = self.minutes % 60
        suffix = "AM" if h < 12 else "PM"
        display_h = h % 12
        if display_h == 0:
            display_h = 12
        return f"{display_h}:{m:02d} {suffix}"

    def __repr__(self):
        return f"Time('{str(self)}')"

    # comparison
    def __lt__(self, other: Time) -> bool:
        if not isinstance(other, Time):
            return NotImplemented
        return self.minutes < other.minutes

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Time):
            return False
        return self.minutes == other.minutes

    # addition: Time + int minutes -> Time
    def __add__(self, offset: int) -> Time:
        if not isinstance(offset, int):
            return NotImplemented
        total = (self.minutes + offset) % (24 * 60)
        return Time.from_minutes(total)

    __radd__ = __add__

    # subtraction: Time - int minutes -> Time, or Time - Time -> difference in minutes
    def __sub__(self, other):
        if isinstance(other, int):
            total = (self.minutes - other) % (24 * 60)
            return Time.from_minutes(total)
        if isinstance(other, Time):
            return self.minutes - other.minutes  # can be negative
        return NotImplemented

    @classmethod
    def from_minutes(cls, minutes: int) -> "Time":
        if not (0 <= minutes < 24 * 60):
            minutes %= 24 * 60
        hour = minutes // 60
        minute = minutes % 60
        suffix = "AM" if hour < 12 else "PM"
        display_h = hour % 12
        if display_h == 0:
            display_h = 12
        return cls(f"{display_h}:{minute:02d} {suffix}")

    # convenience for other comparisons
    def __le__(self, other: Time) -> bool:
        return self == other or self < other

    def __gt__(self, other: Time) -> bool:
        return not (self <= other)

    def __ge__(self, other: Time) -> bool:
        return not (self < other)
    def __hash__(self):
        return hash(str(self))

        
@dataclass(frozen=True)
class TimeRange:
    start: Time
    end: Time
     
    @classmethod
    def from_string(cls, s: str) -> "TimeRange":
        left, right = [part.strip() for part in s.split("-", 1)]
        return cls(start=Time(left), end=Time(right))

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError("end time must not be before start time")

    def duration_minutes(self) -> int:
        return self.end - self.start  

    def overlaps(self, other: "TimeRange") -> bool:
        return not (self.end <= other.start or other.end <= self.start)

    def __str__(self):
        return f"{self.start} - {self.end}"
    
    def __lt__(self, other : TimeRange):
        return self.start < other.start
