#!/bin/bash
#SBATCH --job-name=testset-web
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/web-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
"$PY" -B corpus/testset/measure.py web "$PY" -B corpus/testset/web.py
