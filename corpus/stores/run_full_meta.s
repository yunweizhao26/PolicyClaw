#!/bin/bash
#SBATCH --job-name=stores-meta
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=48:00:00
#SBATCH --signal=B:TERM@300
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/full-meta-%x-%j.out
STORE=${1:?usage: sbatch run_full_meta.s android|apple}
source /scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/_full_common.sh
cd "$STORES_DIR"
if [ ! -d "$DATA_DIR/$STORE/ids" ]; then
  mkdir -p "$DATA_DIR/$STORE"
  cp -r "$PILOT_DIR/$STORE/ids" "$DATA_DIR/$STORE/ids" || exit 1     # copy of the pilot's complete id table
fi
lim=(); [ -n "${LIMIT:-}" ] && lim=(--limit "$LIMIT")
step $STORE meta meta.py $STORE "$DATA_DIR/$STORE/ids" --data-dir "$DATA_DIR" --full ${META_ARGS:-} "${lim[@]}"
rc=$?
if [ $rc -ne 0 ]; then echo "meta exited $rc; resubmit to continue"; exit $rc; fi
step $STORE links links.py $STORE --data-dir "$DATA_DIR"
exit $?
