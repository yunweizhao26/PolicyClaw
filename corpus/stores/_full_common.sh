# Shared shell helpers for the run_full_*.s scripts (sourced).
STORES_DIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
DATA_DIR=${DATA_DIR:-$STORES_DIR/data_full}
PILOT_DIR=${PILOT_DIR:-$STORES_DIR/data}
CHILD=
forward_term() { [ -n "$CHILD" ] && kill -TERM "$CHILD" 2>/dev/null; }
trap forward_term TERM INT

# step SET NAME args...: run under timev with the TERM signal forwarded; logs append across resubmissions.
step() {
  local set=$1 name=$2; shift 2
  mkdir -p "$DATA_DIR/$set/logs"
  echo "[$(date -u +%H:%M:%S)] $set $name start"
  $PY "$STORES_DIR/timev.py" "$DATA_DIR/$set/logs/$name.time" -- $PY "$@" >> "$DATA_DIR/$set/logs/$name.log" 2>&1 &
  CHILD=$!
  wait $CHILD; local rc=$?
  while kill -0 $CHILD 2>/dev/null; do wait $CHILD; rc=$?; done   # a trapped signal interrupts the first wait
  CHILD=
  echo "[$(date -u +%H:%M:%S)] $set $name exit $rc"
  return $rc
}
