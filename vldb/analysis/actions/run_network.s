#!/bin/bash
#SBATCH --job-name=pc-actions
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/actions/%x_%j.out
set -euo pipefail
D=/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/actions
/scratch/yz5944/miniconda3/envs/poligraph/bin/python $D/build_lemmas.py
export LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash GEMINI_THINKING_LEVEL=LOW THREADS=8 \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud
/scratch/yz5944/miniconda3/envs/llm/bin/python $D/place_lemmas.py
