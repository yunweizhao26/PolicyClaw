#!/bin/bash
#SBATCH --job-name=stores-policies
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --signal=B:TERM@300
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/full-policies-%j.out
source /scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/_full_common.sh
cd "$STORES_DIR"
LINKS=(); for s in android apple; do [ -d "$DATA_DIR/$s/links" ] && LINKS+=("$DATA_DIR/$s/links"); done
[ ${#LINKS[@]} -eq 0 ] && { echo "no links tables under $DATA_DIR yet"; exit 1; }
lim=(); [ -n "${LIMIT:-}" ] && lim=(--limit "$LIMIT")
step shared policies policies.py "${LINKS[@]}" --data-dir "$DATA_DIR" ${POLICY_ARGS:-} "${lim[@]}"
exit $?
