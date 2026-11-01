#!/bin/bash
#SBATCH --job-name=testset-finish
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/finish-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
bash corpus/testset/warmup.sbatch
while [ ! -f corpus/testset/metrics/apple.json ]; do
    sleep 30
done
/scratch/yz5944/miniconda3/envs/llm/bin/python -B - <<'PY'
import json
from pathlib import Path
record=json.loads(Path('corpus/testset/metrics/apple.json').read_text())
assert record['exit_code']==0, 'Apple frame job failed; inspect its log before resuming'
PY
bash corpus/testset/phase1.sbatch
