#!/bin/bash
#SBATCH --job-name=testset-v2
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/revision-%j.log
set -euo pipefail
: "${SLURM_JOB_ID:?Run through Slurm on a compute node}"
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TMPDIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/tmp
mkdir -p "$TMPDIR"
exec 9>corpus/testset/.fetch.lock
flock -n 9 || { echo 'Another testset fetch/selection process holds the lock'; exit 1; }
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
if [[ -f corpus/testset/v1/archive_manifest.json && -f corpus/testset/selection.parquet && -f corpus/testset/audit.json ]]; then
    echo 'Revised selection and audit already exist; refusing to overwrite the completed run.'
    exit 1
fi
step() { "$PY" -B corpus/testset/measure.py "v2_$1" "$PY" -B "corpus/testset/$2"; }
finish() {
    status=$?
    trap - EXIT
    if [[ -f corpus/testset/v1/archive_manifest.json ]]; then
        printf '{"exit_code":%s,"slurm_job_id":"%s"}\n' "$status" "$SLURM_JOB_ID" > corpus/testset/revision_failure.json
        step report revision_report.py || { if [[ "$status" == 0 ]]; then status=1; fi; }
    fi
    exit "$status"
}
trap finish EXIT
step selfcheck revision_selfcheck.py
step archive archive_revision.py
step psl psl.py
step exclusions exclusions.py
step app_frames rebuild_app_frames.py
step web_frame web.py
step selection revision_select.py
step audit revision_audit.py
