#!/bin/bash
#SBATCH --job-name=pc-testset-pipeline
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
T=$R/corpus/testset
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
export THREADS=16 LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=LOW \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud
unset POLICYCLAW_PROMPTS POLICYCLAW_SCHEMA EXTRACT_VARIANT SAMPLES MIN_VOTES LENIENT QUALIFIER_VOTES COMPLETE REPAIR
cd $R
start=$(date +%s)
$PY $T/pipeline_inputs.py prep
LLM_CACHE=$T/prep_cache $PY $R/corpus/stores/timev.py $T/logs/prep.time -- \
    $PY -m policyclaw.prep $T/prepare.tsv $T/prepared --resume
echo "prep_elapsed_s=$(( $(date +%s) - start ))"
$PY $T/pipeline_inputs.py extract
status=0
$PY $R/corpus/stores/timev.py $T/logs/extract.time -- \
    $PY $R/corpus/extract_corpus.py --versions $T/versions.jsonl --final-text $T/final_text --out $T/rules \
    --cache $T/extract_cache || status=$?
echo "elapsed_s=$(( $(date +%s) - start )) exit_status=$status"
sstat -j "$SLURM_JOB_ID.batch" --format=JobID,AveCPU,MaxRSS,MaxDiskRead,MaxDiskWrite || true
exit $status
