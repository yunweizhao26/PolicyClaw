#!/bin/bash
#SBATCH --job-name=testset-v2-audit
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=4:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/revision-audit-%j.log
set -euo pipefail
: "${SLURM_JOB_ID:?Run through Slurm on a compute node}"
cd /scratch/yz5944/nlp+privacy/PolicyClaw
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TMPDIR=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/tmp
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
step() { "$PY" -B corpus/testset/measure.py "v2_$1" "$PY" -B "corpus/testset/$2"; }
T=/scratch/yz5944/.trash/policyclaw_testset_20261021
if [[ -f corpus/testset/revision_failure.json ]]; then
    mkdir -p "$T"
    printf '%s\t%s\t%s\n' "$(stat -c %s corpus/testset/revision_failure.json)" "$PWD/corpus/testset/revision_failure.json" \
        "Job 20495716 audit failed only on newline translation in read_text; superseded by rerun $SLURM_JOB_ID" >> "$T/MANIFEST.tsv"
    mv corpus/testset/revision_failure.json "$T/revision_failure_20495716.json"
fi
status=0
step audit revision_audit.py || status=$?
[[ $status == 0 ]] || printf '{"exit_code":%s,"slurm_job_id":"%s"}\n' "$status" "$SLURM_JOB_ID" > corpus/testset/revision_failure.json
step report revision_report.py
exit $status
