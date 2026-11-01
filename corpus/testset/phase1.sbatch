#!/bin/bash
#SBATCH --job-name=testset-phase1
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/phase1-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TMPDIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/tmp
mkdir -p "$TMPDIR"
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
status=0
"$PY" -B corpus/testset/phase1.py || status=$?
"$PY" -B corpus/testset/measure.py final_report "$PY" -B corpus/testset/report.py
exit "$status"
