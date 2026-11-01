# PolicyClaw

This repository holds the code, data, and labels for the paper From Legal Text to Logic: Compiling Privacy Policies into Verifiable Rules.

PolicyClaw reads a privacy policy, extracts its rules, turns their conditions into logic, and uses the Z3 solver to check whether opposing rules can apply at the same time.

The system is in policyclaw/. The 600 policies we evaluate, with their text, rules, and model caches, are in corpus/testset/. The labels and scoring scripts are in corpus/testset/eval/. The 200 policies we use to compare with other systems are in corpus/policheck_stest/. The scripts behind the numbers in the paper are in vldb/analysis/testset_results/. RESULTS_600.md in that folder lists which script produces each number, and RESULTS_RQ3.md holds the comparison of the solver with model calls.

Our full dataset of app store listings and privacy policies is too large for this repository. We will post the link here. You do not need it to reproduce the paper.

To reproduce the numbers in the paper, run git lfs pull, replace our cluster paths in the scripts with your own, and run these commands. They make no model calls.

    sbatch vldb/analysis/testset_results/run_all.s
    python corpus/testset/eval/score.py
    python corpus/testset/eval/conflicts/score_v2.py
    python corpus/policheck_stest/compare/score_f1.py

To rerun the models, set your Gemini credentials and run corpus/testset/run_pipeline.s. Model answers are cached, so a rerun on the same text returns the cached answer.
