# Idea Queue

Add one idea per section. Keep it testable.

## Template
- **Hypothesis:**
- **Metric / invariant:**
- **Experiment:**
- **Disconfirming outcome:**
- **Notes / links:**

## Idea: Complex escape-time atlas
- **Hypothesis:** The analytic Collatz extension in the complex plane has structured basins that correlate with integer stopping-time regions near the real axis.
- **Metric / invariant:** Escape fraction, escape-step histogram, and min-distance-to-1 heatmap over a fixed grid.
- **Experiment:** Run `scripts/exp_complex_escape_map.py` at multiple windows/resolutions and compare patterns as steps increase.
- **Disconfirming outcome:** Maps converge to near-uniform noise with no stable structures under parameter changes.
- **Notes / links:** Use the parity proxy extension implemented in `src/collatz/experiments.py`.

## Idea: Residue-class transition graph
- **Hypothesis:** A higher-modulus residue transition graph (mod 2^k and mod 3*2^k) exposes bottleneck classes associated with long stopping times.
- **Metric / invariant:** Hitting probabilities, strongly connected components, and mean path length to the class containing 1.
- **Experiment:** Build a script that computes class-to-class transitions from sampled trajectories and visualizes graph centrality.
- **Disconfirming outcome:** Graph structure remains statistically flat without distinguishable bottlenecks.
- **Notes / links:** Candidate output: `analysis/results/residue_graph_*.csv`.

## Idea: Prefix-tree motif mining
- **Hypothesis:** Binary parity patterns in early trajectory prefixes contain predictive signal for long stopping time.
- **Metric / invariant:** Mutual information between prefix motif and stopping-time quantiles.
- **Experiment:** Mine top motifs from dataset prefixes and evaluate predictive lift over random baseline.
- **Disconfirming outcome:** Motifs show no out-of-sample predictive lift.
- **Notes / links:** Pair with `scripts/exp_baseline_dataset.py`.

## Idea: Reverse Collatz tree growth law
- **Hypothesis:** Reverse tree branching statistics obey a stable growth law after depth normalization.
- **Metric / invariant:** Node count by depth, branching factor distribution, and entropy profile.
- **Experiment:** Expand reverse tree from 1 under valid inverse rules and fit asymptotic growth curves.
- **Disconfirming outcome:** No stable normalized profile emerges across depth windows.
- **Notes / links:** Useful for paper appendix + visualization figures.

## Idea: Prime-discriminator family map
- **Hypothesis:** Rules of the form `n%p==0 ? n/p : an+1` exhibit phase boundaries (termination/cycle/escape) in `(p, a)` parameter space.
- **Metric / invariant:** Termination fraction, cycle fraction, unresolved fraction, and median steps on finite windows.
- **Experiment:** Sweep tuples with `scripts/exp_generalized_rule_scan.py` and chart outcomes by parameter pair.
- **Disconfirming outcome:** No meaningful stratification appears; metrics are flat across tested families.
- **Notes / links:** Directly supports "%3 with 5n+1" and other next-prime discriminator experiments.
