#!/bin/bash
#SBATCH --job-name=pc-conflicts
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=16
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
DIR=${1:?set directory}
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
export THREADS=16 LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=LOW \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud
cd $R
start=$(date +%s)
$PY $R/corpus/stores/timev.py $DIR/logs/relate_terms.time -- $PY $R/corpus/testset/eval/relate_terms_run.py --dir $DIR
echo "relate_elapsed_s=$(( $(date +%s) - start ))"
$PY $R/corpus/testset/eval/find_conflicts.py --dir $DIR --workers ${WORKERS:-16}
echo "elapsed_s=$(( $(date +%s) - start ))"
