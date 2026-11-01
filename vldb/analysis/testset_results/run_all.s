#!/bin/bash
#SBATCH --job-name=pc-testset-results
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/testset_results/out/%x_%j.log

set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
D=$R/vldb/analysis/testset_results
S=$R/vldb/analysis/corpus_results
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
T=$R/corpus/stores/timev.py
mkdir -p "$D/out"
cd "$D"
step() {
  local name=$1; shift
  srun --ntasks=1 --cpus-per-task=8 --job-name="$name" "$PY" "$T" "$D/out/time_$name.log" -- "$PY" "$@"
}
step rules "$S/rules.py" --set testset
step pairs "$S/pairs.py" --set testset
step queries "$S/queries.py" --set testset --terms on
step queries_no_terms "$S/queries.py" --set testset --terms off
step reconcile_pairs "$D/reconcile_pairs.py"
step figures "$D/figures.py"
step reasoning_score "$D/reasoning_score.py"
step reasoning_join "$D/reasoning_join.py" score
step reasoning_batch "$D/reasoning_batch.py" score
step reasoning_check "$D/reasoning_check.py"
step reasoning_report "$D/reasoning_report.py"
step draw_figures "$D/draw_figures.py"
step draw_join "$D/draw_join.py" "$D/figures"
