#!/usr/bin/env bash
#SBATCH --job-name=bl_poligraph
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=10:00:00
#SBATCH --array=0-3
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/poligraph_%A_%a.out
#SBATCH --error=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/poligraph_%A_%a.err
# Official PoliGraph-er (init_document, run_annotators, build_graph --variant extended) on CPU, one shard per array task.
set -euo pipefail
BL=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
echo "host $(hostname) start $(date -Is) shard ${SLURM_ARRAY_TASK_ID}"
/usr/bin/python3 -I "${BL}/scripts/poligraph_shard.py" "${SLURM_ARRAY_TASK_ID}" 4
echo "end $(date -Is)"
