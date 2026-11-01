#!/bin/bash
#SBATCH --job-name=pc-confirmation
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=2:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
C=$R/corpus/collect/confirmation
export LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=MEDIUM \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud LLM_CACHE=$R/corpus/collect/llm_cache
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
cd $R
start=$(date +%s)
[ -f $C/sample.tsv ] || $PY corpus/collect/make_confirmation.py
$PY corpus/collect/verify.py $C/sample.tsv $C/verifier_v1_medium.jsonl --threads 12 --resume --prompt v1
echo "elapsed_s=$(( $(date +%s) - start ))"
