# Example Scripts

Runnable, genericized demonstrations of the techniques behind the
[design patterns](../docs/patterns). Everything here runs against the dummy data
in [`sample_data/`](sample_data) — no real data, no credentials.

| Script | Demonstrates | Needs |
|--------|-------------|-------|
| [`business_days.py`](business_days.py) | The business-day gate (pattern 1) — compute BD-N, no-op otherwise | stdlib only |
| [`tie_out.py`](tie_out.py) | Tie-out verification (pattern 5) — named checks that must equal zero | stdlib only |
| [`make_census_pivot.py`](make_census_pivot.py) | Building an .xlsx with **genuine, refreshable Excel PivotTables** via the LibreOffice UNO bridge | openpyxl + LibreOffice |

## Quickstart

```bash
pip install -r requirements.txt

# Pattern 1 — the gate
python business_days.py date 6 2026-10              # what date is BD6 of Oct 2026?
python business_days.py gate 6 --on 2026-10-08      # would a run on this date act?
python business_days.py nth 6 2026-10-08 --holidays us

# Pattern 5 — tie-outs
python tie_out.py                                   # runs a worked example

# The LibreOffice live-pivot technique
python make_census_pivot.py sample_data/roster_sample.csv -o roster.xlsx --data-only
python make_census_pivot.py sample_data/roster_sample.csv -o roster_with_pivots.xlsx
```

## The LibreOffice pivot technique (why it's here)

The single most reusable trick in this repo. The naive approach — hand-writing
the `pivotTable`/`pivotCache` XML, or patching an openpyxl workbook to fake a
pivot — produces a file Excel flags as corrupt ("needs repair"), even though
other tools open it fine. The reliable approach is two-phase:

1. **openpyxl** builds the data-only workbook (all sheets, formatting, and an
   empty sheet reserved for the pivots).
2. **LibreOffice headless**, driven over the python-UNO bridge, inserts native
   DataPilot tables and writes the final `.xlsx` with the
   `Calc MS Excel 2007 XML` filter — which Excel reads as real, refreshable
   PivotTables.

`make_census_pivot.py` is a complete, commented implementation you can lift and
point at your own data and pivot fields. Installing LibreOffice is an OS-level
step (see [`requirements.txt`](requirements.txt)); `--data-only` lets you run
everything except the pivot step with no LibreOffice at all.

> Reminder: these scripts are structure and technique. Never commit your real
> roster, financials, names, or exports — run them on your own data locally.
