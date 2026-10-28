"""Write a local system-health snapshot without collecting hostnames or raw logs."""

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import psutil


def collect():
    """Collect aggregate health metrics; omit network and account identifiers."""
    memory = psutil.virtual_memory()
    uptime_seconds = max(0.0, datetime.now(timezone.utc).timestamp() - psutil.boot_time())
    return {
        "schema_version": 1,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
        },
        "cpu": {"logical_count": psutil.cpu_count(), "usage_percent": psutil.cpu_percent(interval=0.2)},
        "memory": {
            "total_bytes": memory.total,
            "available_bytes": memory.available,
            "usage_percent": memory.percent,
        },
        "uptime_seconds": round(uptime_seconds, 1),
    }


def write_report(report, path):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Local JSON output; existing files are preserved")
    args = parser.parse_args()
    try:
        write_report(collect(), args.output)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print("Local system-health report saved")


if __name__ == "__main__":
    main()
