#!/bin/bash
#SBATCH --job-name=pc-wayback-hist
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=8:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
cd $R
start=$(date +%s)
/scratch/yz5944/miniconda3/envs/llm/bin/python -u corpus/collect/wayback_histories.py --dir confirmation "$@"
echo "elapsed_s=$(( $(date +%s) - start ))"
