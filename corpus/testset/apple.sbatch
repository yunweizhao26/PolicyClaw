#!/bin/bash
#SBATCH --job-name=testset-apple
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/apple-%j.log
set -euo pipefail
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
"$PY" -B corpus/testset/measure.py apple "$PY" -B corpus/testset/apple.py
