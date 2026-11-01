#!/bin/bash
#SBATCH --job-name=testset-warmup
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=06:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/warmup-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TMPDIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/tmp
mkdir -p "$TMPDIR"
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
"$PY" -B corpus/testset/measure.py reuse_index "$PY" -B corpus/testset/fetch_candidates.py index
"$PY" -B corpus/testset/measure.py batch-0000_fetch_text "$PY" -B corpus/testset/fetch_candidates.py corpus/testset/warmup/batch-0000.json
"$PY" -B corpus/testset/measure.py batch-0000_verify "$PY" -B corpus/testset/verify_candidates.py corpus/testset/warmup/batch-0000.json
