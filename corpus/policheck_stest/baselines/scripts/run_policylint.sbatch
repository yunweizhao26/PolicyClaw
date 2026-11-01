#!/usr/bin/env bash
#SBATCH --job-name=bl_policylint
#SBATCH --account=torch_pr_634_general
#SBATCH --partition=cs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=10:00:00
#SBATCH --output=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/policylint_%j.out
#SBATCH --error=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines/work/logs/policylint_%j.err
# Official PolicyLint (PrivacyPolicyAnalysis commit 6c0c163, DockerImage/code/main.sh, run_config "policylint") in the
# python:2.7 image with the package overlay built for the earlier run, then the UTF-8 postprocessing.
set -uo pipefail
unset PYTHONPATH
BL=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/policheck_stest/baselines
W="${BL}/work"
EXT="${W}/policylint/ext"
CHECK="${W}/policylint/ext_utf8check"
TIMEV=/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/stores/timev.py
LOGS="${W}/logs"
APPT=(apptainer exec --fakeroot --overlay "${W}/containers/policylint_py27_fakeroot_overlay_v2.img:ro" --no-mount bind-paths
      --bind "${W}/policylint/code:/src")
echo "host $(hostname) start $(date -Is)"
test -f "${EXT}/run_config" && test "$(cat "${EXT}/run_config")" = policylint
test "$(ls "${EXT}/plaintext_policies" | wc -l)" -eq 200
if [[ -e "${EXT}/output" ]]; then echo "refusing to reuse existing ${EXT}/output" >&2; exit 2; fi
# The official extraction logs sentences that raise RuntimeError to /ext/output/log/, a directory main.sh never creates.
mkdir -p "${EXT}/output/log"

# 1. Official pipeline, unchanged: extraction, contradiction analysis, postprocessing, disclosure classification.
/usr/bin/python3 -I "${TIMEV}" "${LOGS}/policylint_main_${SLURM_JOB_ID}.time" -- \
  env -u APPTAINER_BINDPATH -u SINGULARITY_BINDPATH -u APPTAINER_BIND -u SINGULARITY_BIND \
  "${APPT[@]}" --bind "${EXT}:/ext" "${W}/containers/python_2.7.sif" bash -c 'cd /src && ./main.sh' \
  > "${LOGS}/policylint_main_${SLURM_JOB_ID}.log" 2>&1
echo "main.sh exit status $?"
cat "${LOGS}/policylint_main_${SLURM_JOB_ID}.time"

# 2. Cross-check only: the unchanged official postprocessor on a copy of the result database, with Python 2's default
#    codec set to UTF-8 (work/policylint/utf8_site/sitecustomize.py).
mkdir -p "${CHECK}/output/db" "${CHECK}/combined_tables"
cp -p "${EXT}/output/db/consistency_results_1.db" "${CHECK}/output/db/"
env -u APPTAINER_BINDPATH -u SINGULARITY_BINDPATH -u APPTAINER_BIND -u SINGULARITY_BIND APPTAINERENV_PYTHONPATH=/utf8site \
  "${APPT[@]}" --bind "${CHECK}:/ext" --bind "${W}/policylint/utf8_site:/utf8site" "${W}/containers/python_2.7.sif" \
  bash -c 'cd /src && python2 -c "import sys; print(sys.getdefaultencoding())" && python2 RemoveSameSentenceContradictions.py 1' \
  > "${LOGS}/policylint_utf8check_${SLURM_JOB_ID}.log" 2>&1
echo "utf8 cross-check exit status $?"

# 3. Python 3 UTF-8 port of the contradiction export, cross-checks, and normalization.
/usr/bin/python3 -I "${TIMEV}" "${LOGS}/policylint_post_${SLURM_JOB_ID}.time" -- \
  /usr/bin/python3 -I "${BL}/scripts/policylint_postprocess.py"
echo "postprocess exit status $?"

# 4. Keep the official output files next to the normalized table.
mkdir -p "${BL}/policylint/official_ext"
for p in output combined_tables datasets input policylint_results.csv policheck_results.csv; do
  [[ -e "${EXT}/${p}" ]] && cp -a "${EXT}/${p}" "${BL}/policylint/official_ext/"
done
cp -a "${EXT}"/*.log "${BL}/policylint/official_ext/" 2>/dev/null
echo "end $(date -Is)"
