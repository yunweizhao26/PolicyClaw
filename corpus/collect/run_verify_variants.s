#!/bin/bash
#SBATCH --job-name=pc-verify-variants
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=3:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/logs/%x_%j.out
set -euo pipefail
R=/scratch/yz5944/nlp+privacy/PolicyClaw
V=$R/corpus/collect/validation
export LLM_BACKEND=gemini LLM_MODEL_NAME=gemini-3.8-flash \
       GOOGLE_CLOUD_PROJECT=project-21073ade-77cc-47de-979 GOOGLE_CLOUD_LOCATION=global \
       GCLOUD_BIN=/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud LLM_CACHE=$R/corpus/collect/llm_cache
PY=/scratch/yz5944/miniconda3/envs/llm/bin/python
cd $R
start=$(date +%s)
for v in "v2 LOW" "v1 MEDIUM" "v2 MEDIUM"; do
  set -- $v
  out=$V/verifier_${1}_${2,,}.jsonl
  ( GEMINI_THINKING_LEVEL=$2 $PY corpus/collect/verify.py $V/sample.tsv $out --threads 12 --resume --prompt $1 \
      > $out.log 2>&1 || echo "variant $1 $2 exited $?" ) &
done
wait
for v in v2_low v1_medium v2_medium; do
  $PY corpus/collect/score_verifier.py --verifier $V/verifier_$v.jsonl --out $V/score_$v.md > /dev/null
  echo "== $v"; sed -n 5,9p $V/score_$v.md
done
echo "elapsed_s=$(( $(date +%s) - start ))"
