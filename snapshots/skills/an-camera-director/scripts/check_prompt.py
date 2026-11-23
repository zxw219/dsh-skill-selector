"""Portable entry point for the bundled An text checker."""
from pathlib import Path
import runpy
import sys
target = Path(__file__).resolve().parents[1] / 'references/library/an-workflow/scripts/check_prompt.py'
sys.path.insert(0, str(target.parent))
runpy.run_path(str(target), run_name="__main__")
