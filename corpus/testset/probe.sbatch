#!/bin/bash
#SBATCH --job-name=testset-probe
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/probe-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
"$PY" -B corpus/testset/measure.py inspect_inputs "$PY" -B corpus/testset/inspect_inputs.py
"$PY" -B - <<'PY'
import zipfile
from pathlib import Path
p=Path('/scratch/yz5944/nlp+privacy/Contextual-Integrity/policy-ie/data/sanitized_split.zip')
with zipfile.ZipFile(p) as z:
    ns=z.namelist()
    print('PolicyIE zip top-level', sorted({n.split('/')[0] for n in ns}))
    print('PolicyIE zip first names', ns[:30])
    print('PolicyIE zip source-like files', [n for n in ns if any(s in n.lower() for s in ('url', 'source', 'readme', 'website', '.csv'))][:50])
PY
