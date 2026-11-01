#!/bin/bash
#SBATCH --job-name=testset-required-fetch
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/required-fetch-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
"$PY" -B corpus/testset/measure.py required_apple_fetch_text "$PY" -B corpus/testset/fetch_candidates.py corpus/testset/warmup/required-apple-800.json
"$PY" -B corpus/testset/measure.py required_web_fetch_text "$PY" -B corpus/testset/fetch_candidates.py corpus/testset/warmup/required-web-800.json
