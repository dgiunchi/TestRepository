# ROADMAP - Collatz Lab

## Milestones
### M0 - Repo ready for multi-agent research (now)
- [ ] Paper skeleton compiles
- [ ] Core library extracted to `src/collatz/`
- [ ] Baseline experiments reproducible

### M1 - Baseline empirical study
- [ ] Dataset: stopping time + peak for starts 1..N (configurable)
- [ ] Plots: stopping time landscape, peak landscape, joint scatter
- [ ] Paper: intro + related work draft

### M2 - New ideas and visualizations
- [ ] 3-5 hypotheses from `docs/ideas/queue.md` tested
- [ ] 2 new visualization families implemented

### M3 - Paper submission-ready
- [ ] Polished narrative + figures
- [ ] Complete references
- [ ] Reproducibility appendix

## Current questions
- What features predict unusually large stopping time / peak?
- How do residue classes mod 2^k influence trajectories?
- Which visual encodings reveal structure beyond standard stopping-time plots?

## Backlog (agents)
- Orchestrator: keep tasks small and tracked
- Paper: intro, notation, related work
- Code: stats engine, viz engine, experiment runner

