#!/bin/bash
#SBATCH --job-name=stores-text
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --signal=B:TERM@300
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/full-text-%j.out
source /scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/_full_common.sh
cd "$STORES_DIR"
step shared text text.py shared --data-dir "$DATA_DIR" --workers 28 ${TEXT_ARGS:-}
exit $?
