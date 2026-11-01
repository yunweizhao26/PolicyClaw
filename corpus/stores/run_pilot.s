#!/bin/bash
#SBATCH --job-name=stores-pilot
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/pilot-%j.out
set -u
STORES_DIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
DATA_DIR=${DATA_DIR:-$STORES_DIR/data}
N=${N:-5000}
SEED=${SEED:-20261015}
MAX_SITEMAPS=${MAX_SITEMAPS:-}
LIMIT=${LIMIT:-}
SITEMAP_WORKERS=${SITEMAP_WORKERS:-16}
META_WORKERS=${META_WORKERS:-16}
POLICY_WORKERS=${POLICY_WORKERS:-64}
POLICY_PER_HOST=${POLICY_PER_HOST:-2}
TEXT_WORKERS=${TEXT_WORKERS:-12}
cd "$STORES_DIR"

step() {
  local set=$1 name=$2; shift 2
  mkdir -p "$DATA_DIR/$set/logs"
  echo "[$(date -u +%H:%M:%S)] $set $name start"
  $PY timev.py "$DATA_DIR/$set/logs/$name.time" -- $PY "$@" > "$DATA_DIR/$set/logs/$name.log" 2>&1
  local rc=$?
  echo "[$(date -u +%H:%M:%S)] $set $name exit $rc"
  return $rc
}

pipeline() {
  local s=$1
  local sm_args=(); [ -n "$MAX_SITEMAPS" ] && sm_args=(--max-sitemaps "$MAX_SITEMAPS")
  local lim=();     [ -n "$LIMIT" ] && lim=(--limit "$LIMIT")
  step $s sitemaps sitemaps.py $s --data-dir "$DATA_DIR" --workers $SITEMAP_WORKERS "${sm_args[@]}" || return 1
  step $s sitemaps_retry sitemaps.py $s --data-dir "$DATA_DIR" --workers $SITEMAP_WORKERS "${sm_args[@]}" || return 1   # retries failed sub-sitemaps only
  step $s sample sample.py $s "$N" "$SEED" --data-dir "$DATA_DIR" || return 1
  step $s meta meta.py $s "$DATA_DIR/$s/sample" --data-dir "$DATA_DIR" --workers $META_WORKERS "${lim[@]}" || return 1
  step $s links links.py $s --data-dir "$DATA_DIR" || return 1
}

pipeline android & PA=$!
pipeline apple & PB=$!
wait $PA; RA=$?
wait $PB; RB=$?
echo "store pipelines finished: android=$RA apple=$RB"
RC=0
if [ -d "$DATA_DIR/android/links" ] || [ -d "$DATA_DIR/apple/links" ]; then
  LINKS=(); for s in android apple; do [ -d "$DATA_DIR/$s/links" ] && LINKS+=("$DATA_DIR/$s/links"); done
  lim=(); [ -n "$LIMIT" ] && lim=(--limit "$LIMIT")
  step shared policies policies.py "${LINKS[@]}" --data-dir "$DATA_DIR" --workers $POLICY_WORKERS --per-host $POLICY_PER_HOST "${lim[@]}" || RC=1
  step shared text text.py shared --data-dir "$DATA_DIR" --workers $TEXT_WORKERS || RC=1
fi
step shared report report.py --data-dir "$DATA_DIR" || RC=1
exit $(( RA != 0 || RB != 0 || RC != 0 ))
