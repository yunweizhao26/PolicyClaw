#!/usr/bin/env bash
#SBATCH --job-name=bl_pg_contra
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/poligraph_contra_%j.out
#SBATCH --error=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/poligraph_contra_%j.err
# Official PoliGraph contradiction analyses (analyses/contradictions/) on the extended graphs, then normalization.
set -euo pipefail
BL=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines
W="${BL}/work"
PG="${W}/PoliGraph"
ENV=/scratch/yz5944/miniconda3/envs/poligraph
TIMEV=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/timev.py
LOGS="${W}/logs"
export PATH="${ENV}/bin:${PATH}" PYTHONPATH="${PG}" PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
cd "${W}"
echo "host $(hostname) start $(date -Is)"
test -f "${BL}/policylint/policylint_results.csv"
mapfile -t DIRS < <("${ENV}/bin/python" "${BL}/scripts/poligraph_finish.py" list)
echo "completed work directories: ${#DIRS[@]}"
# get-poligraph-contradictions.py reads graph.yml; build_graph --variant extended writes graph-extended.yml.
for d in "${DIRS[@]}"; do ln -sfn graph-extended.yml "${d}/graph.yml"; done
mkdir -p "${BL}/poligraph"
/usr/bin/python3 -I "${TIMEV}" "${LOGS}/poligraph_contradictions.time" -- \
  "${ENV}/bin/python" "${PG}/analyses/contradictions/get-poligraph-contradictions.py" \
  -o "${BL}/poligraph/contradictions.csv" "${DIRS[@]}" > "${LOGS}/poligraph_contradictions.log" 2>&1
/usr/bin/python3 -I "${TIMEV}" "${LOGS}/poligraph_reclassify.time" -- \
  "${ENV}/bin/python" "${PG}/analyses/contradictions/reclassify-policylint-contradictions.py" \
  -r "${BL}/policylint" -o "${BL}/poligraph/policylint_reclassified.csv" "${DIRS[@]}" > "${LOGS}/poligraph_reclassify.log" 2>&1
"${ENV}/bin/python" "${BL}/scripts/poligraph_finish.py" normalize
echo "end $(date -Is)"
