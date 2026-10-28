import json

import pytest

from report import collect, write_report


def test_report_contains_metrics_and_omits_identifiers():
    report = collect()
    assert report["uptime_seconds"] >= 0
    assert 0 <= report["memory"]["usage_percent"] <= 100
    assert set(report["platform"]) == {"system", "release", "architecture"}
    assert "hostname" not in json.dumps(report)
    assert "username" not in json.dumps(report)


def test_report_refuses_overwrite(tmp_path):
    output = tmp_path / "report.json"
    write_report({"schema_version": 1}, output)
    with pytest.raises(FileExistsError):
        write_report({"schema_version": 2}, output)
    assert json.loads(output.read_text())["schema_version"] == 1
