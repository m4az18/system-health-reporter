# System health reporter

A local JSON snapshot of CPU usage, memory pressure, uptime and platform
details, exported through a portable command-line tool with explicit output
and a small data footprint.

## Run

Python 3.10+:

```bash
python -m pip install -r requirements.txt
python report.py --output reports/health.json
```

Reports are written locally and an existing file is never overwritten.
The tool collects no hostname, username, IP address, process list or raw
operating-system logs. Aggregate hardware and OS details can still identify
a system when combined with other data; review a report before sharing it.

Uptime is reported as elapsed seconds rather than a boot timestamp. Each
report includes a UTC collection timestamp.
CPU usage is a short sample, so it is a snapshot rather than a monitoring history.

## Checks

```bash
python -m pip install -r requirements-dev.txt
ruff check .
pytest -q
```
