#!/usr/bin/env python3
"""
tie_out.py — a tiny, dependency-free verification harness.

Implements docs/patterns/05-tie-out-verification.md: define the named checks
that must equal zero, run them all, and get a structured pass/fail report with
exact variances. An agent should produce exactly this shape of result before it
is allowed to claim a process is "done".

Two check styles:
  Check.equal(name, left, right)      -> passes when left == right (diff -> 0)
  Check.zero(name, value)             -> passes when value == 0

Both take an optional `tol` (absolute tolerance, default 0.00 == exact). Keep
tolerances at a cent or below for currency; a dollars-wide tolerance hides real
variances — see the pattern doc.

CLI demo:
  python tie_out.py            # runs a worked example and prints the report
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Check:
    name: str
    left: float
    right: float
    tol: float = 0.0

    @classmethod
    def equal(cls, name: str, left: float, right: float, tol: float = 0.0) -> "Check":
        return cls(name, float(left), float(right), tol)

    @classmethod
    def zero(cls, name: str, value: float, tol: float = 0.0) -> "Check":
        return cls(name, float(value), 0.0, tol)

    @property
    def diff(self) -> float:
        return round(self.left - self.right, 10)

    @property
    def passed(self) -> bool:
        return abs(self.diff) <= self.tol

    def line(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"  [{status}] {self.name}: diff = {self.diff:+.2f} (tol {self.tol:.2f})"


@dataclass
class Report:
    checks: List[Check] = field(default_factory=list)

    def add(self, check: Check) -> "Report":
        self.checks.append(check)
        return self

    def equal(self, name: str, left: float, right: float, tol: float = 0.0) -> "Report":
        return self.add(Check.equal(name, left, right, tol))

    def zero(self, name: str, value: float, tol: float = 0.0) -> "Report":
        return self.add(Check.zero(name, value, tol))

    @property
    def failures(self) -> List[Check]:
        return [c for c in self.checks if not c.passed]

    @property
    def ok(self) -> bool:
        return not self.failures

    def render(self) -> str:
        head = "All tie-outs passed." if self.ok else \
               f"{len(self.failures)} of {len(self.checks)} tie-out(s) FAILED."
        body = "\n".join(c.line() for c in self.checks)
        return f"{head}\n{body}"

    def assert_ok(self) -> None:
        """Raise if any check failed — the 'zero is a gate' precondition."""
        if not self.ok:
            names = ", ".join(c.name for c in self.failures)
            raise AssertionError(f"tie-out(s) failed: {names}\n{self.render()}")


def _demo() -> int:
    # A worked example: a small fixed-asset-style roll-forward.
    begin, additions, disposals, depreciation, ending = 100000.00, 12500.00, 3000.00, 4166.67, 105333.33
    subledger_total, gl_balance = 105333.33, 105333.33

    r = Report()
    r.equal("Roll-forward (begin + add - disp - dep = end)",
            begin + additions - disposals - depreciation, ending, tol=0.01)
    r.equal("Subledger ties to GL", subledger_total, gl_balance)
    r.zero("Unexplained variance", 0.00)

    print(r.render())
    print()
    print("ok =", r.ok)
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(_demo())
