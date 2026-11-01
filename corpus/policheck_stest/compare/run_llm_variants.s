#!/bin/bash
#SBATCH --job-name=pc-pgtest-llm
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
export THREADS=16 LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=LOW \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud
cd $R
$PY $R/corpus/stores/timev.py $R/corpus/policheck_stest/logs/llm_${1}.time -- $PY $R/corpus/policheck_stest/compare/llm_variants.py $1
