# Pong replication: DQN baseline (Khajehnejad et al., 2024)

Early-stage replication attempt of the DQN side of *Biological Neurons Compete with Deep Reinforcement Learning in Sample Efficiency in a Simulated Gameworld* (arXiv:2405.16946), which compares DishBrain neuron cultures to DQN/A2C/PPO on simplified Pong.

**Status: working baseline, not a verified replication.** The environment is my reconstruction (the paper does not fully specify it) and I have not yet compared these numbers to the paper's reported results or its OSF code. Every assumption and deviation is logged in [DEVIATIONS.md](DEVIATIONS.md).

## Findings so far

DQN, full-state input (ball and paddle positions), 70 episodes per run, 50 seeds, epsilon decay over 300 steps. Early = episodes 1-17, late = episodes 18-70, paired t-test across seeds.

| Metric | Early | Late | p |
|---|---|---|---|
| Hits per episode | 0.41 | 0.57 | < 0.001 |
| % aces (zero hits) | 78.8 | 72.3 | 0.001 |
| % long rallies (>= 3 hits) | 4.1 | 5.9 | 0.010 |

![Learning curve](results/abs_full50.png)

**Observation bug found and fixed.** My first build fed the agent only differences between consecutive states, so it could not see where the ball was relative to the paddle. With that input DQN got worse, not better (15 seeds: hits 0.38 -> 0.29, p = 0.021). Adding the current state to the difference fixed it. Use `--diff-only` to reproduce the broken version. I have not confirmed how the original code supplies position.

## Caveats

- Effect size is modest and noisy: per-seed mean hits range from about 0.2 to 1.5, and short runs differ across machines (PyTorch builds drift over many training steps). Cite the 50-seed numbers only.
- Chance level differs from the paper's setup: a random policy here gets 82% aces versus about 50% for the controls in Kagan et al. 2022, so compare changes, not absolute levels.
- Stats are paired t-tests across seeds with no multiple-comparison correction, and no effect sizes or confidence intervals yet.
- Epsilon decay of 300 steps, Adam, MSE loss, the third conv layer and the Pong dynamics are my choices, not taken from the paper.
- Only the full-state vector input has been evaluated. Image mode runs but has not been evaluated. A2C, PPO and the DishBrain comparison are not implemented.

## Run it
`--obs` is one of `image`, `full`, `ball`. Quick smoke test: `python dqn.py --seeds 2 --obs ball --out results\smoke.csv`.

## Files

- `pong_env.py`: Gymnasium Pong (40x40 grid, 3 observation modes)
- `dqn.py`: DQN training (hyperparameters from the paper's appendix)
- `analyze.py`: the paper's three metrics, early vs late, plus a learning-curve plot
- `DEVIATIONS.md`: every difference from the paper, with reasons

## Related: OI rigor review

The [oi-review](oi-review/) folder holds the rubric, search protocol, source list and scoring workbook for the organoid intelligence metascience review this replication feeds into. The workbook's scoring cells are mostly empty drafts, not final scores.

## Next

Compare against the paper's reported DQN numbers; check the OSF code for how input and epsilon are handled; evaluate image mode; add A2C and PPO.
