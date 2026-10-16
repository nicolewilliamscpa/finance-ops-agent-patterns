#!/usr/bin/env python3
"""
business_days.py — dependency-free business-day math for scheduled agents.

Implements the gate from docs/patterns/01-business-day-gating.md: schedule a
task across a calendar-day window, then on each wake-up call
`is_target_business_day()` and no-op unless today is the real BD-N.

Holiday modes:
  "weekend"  -> skip Sat/Sun only (ignore holidays)
  "us"       -> skip weekends + US federal holidays (computed, no dependency)
  callable   -> pass your own holidays(year) -> set[date] for any calendar

Everything here uses only the standard library.

CLI:
  python business_days.py nth 6 2026-10-08        # which BD is this date?
  python business_days.py date 6 2026-10          # what date is BD6 of Oct 2026?
  python business_days.py gate 6 --window 6-10     # is today BD6? (exit 0/1)
  python business_days.py gate 6 --on 2026-10-08   # test the gate for a date
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from typing import Callable, Iterable, Optional, Union

Date = _dt.date
HolidayRule = Union[str, Callable[[int], "set[Date]"]]


# --------------------------------------------------------------------------- #
# US federal holidays (observed), computed — no external dependency.
# --------------------------------------------------------------------------- #
def _nth_weekday(year: int, month: int, weekday: int, n: int) -> Date:
    """The n-th `weekday` (Mon=0..Sun=6) of a month. n=1 => first."""
    d = _dt.date(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + _dt.timedelta(days=offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> Date:
    """The last `weekday` of a month."""
    if month == 12:
        nxt = _dt.date(year + 1, 1, 1)
    else:
        nxt = _dt.date(year, month + 1, 1)
    last = nxt - _dt.timedelta(days=1)
    return last - _dt.timedelta(days=(last.weekday() - weekday) % 7)


def _observed(d: Date) -> Date:
    """Federal holiday observation: Sat -> Fri before, Sun -> Mon after."""
    if d.weekday() == 5:  # Saturday
        return d - _dt.timedelta(days=1)
    if d.weekday() == 6:  # Sunday
        return d + _dt.timedelta(days=1)
    return d


def us_federal_holidays(year: int) -> "set[Date]":
    """US federal holidays for `year`, as observed. Juneteenth included (2021+)."""
    h: set[Date] = set()
    h.add(_observed(_dt.date(year, 1, 1)))                 # New Year's Day
    h.add(_nth_weekday(year, 1, 0, 3))                     # MLK Jr. Day (3rd Mon)
    h.add(_nth_weekday(year, 2, 0, 3))                     # Washington's Bday
    h.add(_last_weekday(year, 5, 0))                       # Memorial Day
    if year >= 2021:
        h.add(_observed(_dt.date(year, 6, 19)))            # Juneteenth
    h.add(_observed(_dt.date(year, 7, 4)))                 # Independence Day
    h.add(_nth_weekday(year, 9, 0, 1))                     # Labor Day (1st Mon)
    h.add(_nth_weekday(year, 10, 0, 2))                    # Columbus Day (2nd Mon)
    h.add(_observed(_dt.date(year, 11, 11)))              # Veterans Day
    h.add(_nth_weekday(year, 11, 3, 4))                    # Thanksgiving (4th Thu)
    h.add(_observed(_dt.date(year, 12, 25)))              # Christmas
    return h


# --------------------------------------------------------------------------- #
# Core business-day logic
# --------------------------------------------------------------------------- #
def _holiday_set(rule: HolidayRule, year: int) -> "set[Date]":
    if rule == "weekend":
        return set()
    if rule == "us":
        return us_federal_holidays(year)
    if callable(rule):
        return set(rule(year))
    raise ValueError(f"unknown holiday rule: {rule!r}")


def is_business_day(d: Date, holiday_rule: HolidayRule = "weekend") -> bool:
    if d.weekday() >= 5:  # Sat/Sun
        return False
    return d not in _holiday_set(holiday_rule, d.year)


def business_day_number(d: Date, holiday_rule: HolidayRule = "weekend") -> Optional[int]:
    """
    Which business day of its own month `d` is (1-based), or None if `d` itself
    is not a business day. Counts from the 1st of the month.
    """
    if not is_business_day(d, holiday_rule):
        return None
    hol = _holiday_set(holiday_rule, d.year)
    count = 0
    cur = d.replace(day=1)
    while cur <= d:
        if cur.weekday() < 5 and cur not in hol:
            count += 1
        cur += _dt.timedelta(days=1)
    return count


def nth_business_day(year: int, month: int, n: int,
                     holiday_rule: HolidayRule = "weekend") -> Date:
    """The date of the n-th business day of `year`-`month`."""
    if n < 1:
        raise ValueError("n must be >= 1")
    hol = _holiday_set(holiday_rule, year)
    cur = _dt.date(year, month, 1)
    count = 0
    while True:
        if cur.month != month:
            raise ValueError(f"month {year}-{month:02d} has fewer than {n} business days")
        if cur.weekday() < 5 and cur not in hol:
            count += 1
            if count == n:
                return cur
        cur += _dt.timedelta(days=1)


def is_target_business_day(n: int, today: Optional[Date] = None,
                           holiday_rule: HolidayRule = "weekend") -> bool:
    """
    The gate. True iff `today` is exactly the n-th business day of its month.
    This is what a scheduled task calls at the top of every run.
    """
    today = today or _dt.date.today()
    return business_day_number(today, holiday_rule) == n


def parse_window(window: str) -> "tuple[int, int]":
    """'6-10' -> (6, 10). Used only to sanity-check a schedule window."""
    lo, hi = window.split("-")
    return int(lo), int(hi)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _add_rule_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--holidays", default="weekend", choices=["weekend", "us"],
                   help="holiday rule (default: weekend-only)")


def main(argv: Optional[Iterable[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_nth = sub.add_parser("nth", help="business-day number of a given date")
    p_nth.add_argument("n", type=int, help="(unused, kept for symmetry) target BD")
    p_nth.add_argument("date", help="YYYY-MM-DD")
    _add_rule_arg(p_nth)

    p_date = sub.add_parser("date", help="date of BD-n for a given month")
    p_date.add_argument("n", type=int)
    p_date.add_argument("month", help="YYYY-MM")
    _add_rule_arg(p_date)

    p_gate = sub.add_parser("gate", help="is today (or --on) the target BD?")
    p_gate.add_argument("n", type=int)
    p_gate.add_argument("--on", help="test a specific date YYYY-MM-DD")
    p_gate.add_argument("--window", help="optional schedule window like 6-10 to sanity check")
    _add_rule_arg(p_gate)

    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "nth":
        d = _dt.date.fromisoformat(args.date)
        bd = business_day_number(d, args.holidays)
        if bd is None:
            print(f"{d} is NOT a business day ({args.holidays})")
            return 1
        print(f"{d} is business day {bd} of {d:%B %Y} ({args.holidays})")
        return 0

    if args.cmd == "date":
        y, m = (int(x) for x in args.month.split("-"))
        d = nth_business_day(y, m, args.n, args.holidays)
        print(f"BD{args.n} of {args.month} is {d:%Y-%m-%d (%A)} ({args.holidays})")
        return 0

    if args.cmd == "gate":
        today = _dt.date.fromisoformat(args.on) if args.on else _dt.date.today()
        if args.window:
            lo, hi = parse_window(args.window)
            if not (lo <= today.day <= hi):
                print(f"[gate] {today}: outside wake-up window {args.window} — would not even fire")
        hit = is_target_business_day(args.n, today, args.holidays)
        bd = business_day_number(today, args.holidays)
        where = f"BD{bd}" if bd else "not a business day"
        print(f"[gate] {today} is {where}; target BD{args.n} -> {'RUN' if hit else 'no-op'}")
        return 0 if hit else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
