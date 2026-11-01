#!/bin/bash
#SBATCH --job-name=pc-pgtest-pipeline
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/logs/%x_%j.out
# PolicyClaw on PoliGraph's 200 test policies with the system used for the evaluation set (corpus/testset/run_pipeline.s):
# text preparation (policyclaw.prep) of the visible text, extraction with the default prompts in one pass
# (corpus/extract_corpus.py), then the opposing pairs and their resolution (conflict_pairs.py). Every model step is
# Gemini 3.8 Flash at low thinking. Resubmitting resumes from the caches.
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
T=$R/corpus/policheck_stest
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
export THREADS=16 LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=LOW \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud
unset POLICYCLAW_PROMPTS POLICYCLAW_SCHEMA EXTRACT_VARIANT SAMPLES MIN_VOTES LENIENT QUALIFIER_VOTES COMPLETE REPAIR
cd $R
start=$(date +%s)
LLM_CACHE=$T/prep_cache $PY $R/corpus/stores/timev.py $T/logs/prep.time -- \
    $PY -m policyclaw.prep $T/prepare.tsv $T/prepared --resume
echo "prep_elapsed_s=$(( $(date +%s) - start ))"
$PY $T/pipeline_inputs.py
status=0
$PY $R/corpus/stores/timev.py $T/logs/extract.time -- \
    $PY $R/corpus/extract_corpus.py --versions $T/versions.jsonl --final-text $T/final_text --out $T/rules \
    --cache $T/extract_cache || status=$?
echo "extract_elapsed_s=$(( $(date +%s) - start )) exit_status=$status"
$PY $R/corpus/testset/eval/conflict_pairs.py --workers 16 --dir $T
echo "elapsed_s=$(( $(date +%s) - start ))"
sstat -j "$SLURM_JOB_ID.batch" --format=JobID,AveCPU,MaxRSS,MaxDiskRead,MaxDiskWrite || true
exit $status
