"""
Master Orchestrator Script for Chaos Engine Growth Case.
Executes data audit & cleaning, LTV modeling, spend optimization, creative scheduling,
and generation of all publication-ready tables and figures.
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = [
    "src/01_data_audit_cleaning.py",
    "src/02_ltv_roas_modeling.py",
    "src/03_spend_optimizer_q2.py",
    "src/04_creative_wearout_q3.py",
    "src/05_generate_tables_figs.py",
]

def run_step(script_path: str):
    print(f"\n{'='*70}\n[STEP] Running {script_path}...\n{'='*70}")
    result = subprocess.run([sys.executable, script_path], check=False)
    if result.returncode != 0:
        print(f"\n[ERROR] Step {script_path} failed with exit code {result.returncode}.")
        sys.exit(result.returncode)
    print(f"[SUCCESS] Finished {script_path}.\n")

def main():
    root = Path(__file__).resolve().parent
    print("=" * 70)
    print("CHAOS ENGINE GROWTH CASE - MASTER PIPELINE EXECUTION")
    print("=" * 70)
    for script in SCRIPTS:
        run_step(str(root / script))
    print("\n" + "=" * 70)
    print("[ALL DONE] Master pipeline completed successfully. Output files updated in outputs/ and submission/.")
    print("=" * 70)

if __name__ == "__main__":
    main()

