#!/bin/bash
#SBATCH --job-name=stores-follow
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --signal=B:TERM@300
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/full-follow-%j.out
source /scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/_full_common.sh
cd "$STORES_DIR"
STOP=0
trap 'STOP=1; forward_term' TERM INT

quota_ok() {
  local line used files
  line=$(myquota 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | grep '^/scratch')
  used=$(echo "$line" | sed -E 's/.* ([0-9.]+)TB\(.*/\1/')
  files=$(echo "$line" | sed -E 's/.*\)\/([0-9]+)\(.*/\1/')
  echo "[$(date -u +%H:%M:%S)] scratch used ${used} TB, ${files} files"
  awk -v u="$used" -v f="$files" 'BEGIN { exit !(u != "" && f != "" && u < 4.95 && f < 4950000) }'
}

while [ $STOP -eq 0 ]; do
  quota_ok || { echo "scratch nearly full: stopping"; exit 2; }
  for s in android apple; do
    [ -d "$DATA_DIR/$s/meta" ] && step $s links links.py $s --data-dir "$DATA_DIR"
    [ $STOP -ne 0 ] && break 2
  done
  fetched=0
  LINKS=(); for s in android apple; do [ -d "$DATA_DIR/$s/links" ] && LINKS+=("$DATA_DIR/$s/links"); done
  if [ ${#LINKS[@]} -gt 0 ]; then
    step shared policies policies.py "${LINKS[@]}" --data-dir "$DATA_DIR" ${POLICY_ARGS:-}
    [ $STOP -ne 0 ] && break
    fetched=$(grep -o '"fetched_this_run": [0-9]*' "$DATA_DIR/shared/reports/policies.json" 2>/dev/null | grep -o '[0-9]*$')
    step shared text text.py shared --data-dir "$DATA_DIR" --workers 14 ${TEXT_ARGS:-}
    [ $STOP -ne 0 ] && break
  fi
  meta_jobs=$(squeue -h -u "$USER" -n stores-meta 2>/dev/null | wc -l)
  echo "[$(date -u +%H:%M:%S)] cycle done: fetched ${fetched:-0} policies; metadata jobs queued or running: $meta_jobs"
  if [ "$meta_jobs" -eq 0 ] && [ "${fetched:-0}" -eq 0 ]; then echo "metadata finished and nothing new: done"; exit 0; fi
  for _ in $(seq 60); do [ $STOP -ne 0 ] && break; sleep 30; done   # 30 minutes between cycles
done
echo "stopped by signal; resubmit to continue"
exit 143
