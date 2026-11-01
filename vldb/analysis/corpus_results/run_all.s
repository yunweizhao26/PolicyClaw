#!/bin/bash
#SBATCH --job-name=pc-corpus-results
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/corpus_results/out/%x_%j.log

set -euo pipefail
D=/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/corpus_results
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
cd "$D"
R=/scratch/yz5944/nlp+privacy/PolicyClaw
srun --ntasks=1 --cpus-per-task=8 --job-name=reconcile "$PY" "$R/corpus/reconcile.py"
for s in corpus rules; do
  srun --ntasks=1 --cpus-per-task=8 --job-name="$s" "$PY" "$s.py"
done
for rules in reconciled extracted; do
  for s in pairs history queries; do
    srun --ntasks=1 --cpus-per-task=8 --job-name="$s-$rules" "$PY" "$s.py" --rules "$rules"
  done
done
