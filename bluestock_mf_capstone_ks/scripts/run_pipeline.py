"""
Master Pipeline Runner

Runs the complete Mutual Fund Analytics pipeline.

Author: Krithik
"""

import subprocess

scripts = [
    "scripts/etl_pipeline.py",
    "scripts/live_nav_fetch.py",
    "scripts/compute_metrics.py",
    "scripts/recommender.py"
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"Error while running {script}")
        break

print("Pipeline execution completed successfully!")