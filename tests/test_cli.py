import json
import pandas as pd
from circular_bias_cli.main import CircularBiasCLI


def _make_sample_csv(path):
    df = pd.DataFrame(
        {
            "time_period": [1, 1, 2, 2, 3, 3],
            "algorithm": ["A", "B", "A", "B", "A", "B"],
            "performance": [0.80, 0.78, 0.82, 0.79, 0.83, 0.81],
            "constraint_compute": [512, 512, 512, 512, 512, 512],
            "constraint_memory": [8.0, 8.0, 8.0, 8.0, 8.0, 8.0],
            "constraint_dataset_size": [10000, 10000, 10000, 10000, 10000, 10000],
        }
    )
    df.to_csv(path, index=False)


def test_cli_detect_json_output(tmp_path):
    csv_path = tmp_path / "sample.csv"
    out_json = tmp_path / "results.json"
    _make_sample_csv(csv_path)

    cli = CircularBiasCLI()
    exit_code = cli.run([
        "detect",
        str(csv_path),
        "--format",
        "json",
        "--output",
        str(out_json),
    ])

    # Should return 0 or 1 depending on detection
    assert exit_code in (0, 1)
    assert out_json.exists()
    data = json.loads(out_json.read_text())
    assert isinstance(data, dict)


def test_cli_info_local_file(tmp_path, capsys):
    csv_path = tmp_path / "sample.csv"
    _make_sample_csv(csv_path)

    cli = CircularBiasCLI()
    exit_code = cli.run(["info", str(csv_path)])

    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "Rows:" in captured
    assert "Columns:" in captured


def test_cli_list_algorithms(capsys):
    cli = CircularBiasCLI()
    exit_code = cli.run(["list-algorithms"]) 
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Available Algorithms" in out
