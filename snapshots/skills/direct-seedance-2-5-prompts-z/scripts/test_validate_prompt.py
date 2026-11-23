"""Run with python scripts/test_validate_prompt.py."""

import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    skill = Path(__file__).resolve().parents[1]
    example = (skill / "references" / "scene-patterns.md").read_text(encoding="utf-8")
    sample = example.split("```text\n", 1)[1].split("\n```", 1)[0]
    required_line = "完全忽略@黑屏素材"
    out_of_order = sample.replace("【全局关系】", "\0").replace("【事件脚本】", "【全局关系】").replace("\0", "【事件脚本】")
    cases = [
        (sample, None),
        (sample.replace("【全局关系】", ""), "Missing heading"),
        (out_of_order, "expected order"),
        (sample.replace(required_line, ""), "Missing required line"),
        (required_line + "\n" + sample.replace(required_line, ""), "Missing required line"),
        (sample.replace("3.5–7秒", "4–7秒"), "Timeline gap"),
    ]
    with TemporaryDirectory() as directory:
        prompt = Path(directory) / "prompt.txt"
        for text, expected_error in cases:
            prompt.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(skill / "scripts" / "validate_prompt.py"),
                 str(prompt), "--duration", "14"],
                capture_output=True, encoding="utf-8",
            )
            report = json.loads(result.stdout)
            if expected_error is None:
                assert result.returncode == 0 and report["valid"] and report["timeline_ranges"] == 4, report
            else:
                assert result.returncode == 2 and any(expected_error in error for error in report["errors"]), report
    print("Six prompt validation checks passed.")


if __name__ == "__main__":
    main()
