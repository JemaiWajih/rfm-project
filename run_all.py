"""Run te whole project in order: python run_all.py"""

import subprocess, sys
from pathlib import Path

base = Path(__file__).resolve().parent / "analysis"

scripts = [
    "1_load_and_clean.py",
    "2_calculate_rfm.py",
    "3_score_and_segment.py",
    "4_marketing_ideas.py",
    "5_visualize.py"
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run([sys.executable, str(base / script)], check=True, cwd=base.parent)