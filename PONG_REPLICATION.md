# Pong replication: DQN baseline

Early replication attempt of the DQN side of Khajehnejad et al. (2024), *Biological Neurons Compete with Deep Reinforcement Learning in Sample Efficiency in a Simulated Gameworld* (arXiv:2405.16946). The paper compares DishBrain neuron cultures to DQN, A2C and PPO on simplified Pong.

**Status:** working baseline, not a verified replication. The environment is my reconstruction because the paper does not fully specify it, and I have not compared my numbers to the paper's or to its OSF code. Every assumption is logged in [DEVIATIONS.md](DEVIATIONS.md).

## Result

DQN, full-state input, 70 episodes per run, 50 seeds, epsilon decay over 300 steps. Early = episodes 1-17, late = 18-70, paired t-test across seeds.

| Metric | Early | Late | p |
|---|---|---|---|
| Hits per episode | 0.41 | 0.57 | < 0.001 |
| % aces | 78.8 | 72.3 | 0.001 |
| % long rallies (3+ hits) | 4.1 | 5.9 | 0.010 |

For scale, a random policy gets 0.28 hits and 82% aces.

![Learning curve](results/abs_full50.png)

## Bug I fixed

My first build gave the agent only the difference between consecutive states, so it could not see where the ball was relative to the paddle. DQN got worse (15 seeds, hits 0.38 to 0.29, p = 0.021). Adding the current state to the difference fixed it. `--diff-only` reproduces the broken version. I have not checked how the original code handles position.

## Caveats

- The effect is modest and noisy. Per-seed mean hits range from about 0.2 to 1.5, and short runs differ across machines. Use the 50-seed numbers.
- A random policy aces 82% of the time here but only about 50% in Kagan's controls, so my environment is harder. Compare changes, not levels.
- Epsilon decay, Adam, MSE, the third conv layer and the Pong dynamics are my choices.
- Stats are paired t-tests across seeds with no correction for three metrics, and no effect sizes or confidence intervals yet.
- Only full-state input is evaluated. Image mode runs but is untested. A2C, PPO and the DishBrain comparison are not implemented.

## Run it

`--obs` is `image`, `full` or `ball`. Smoke test: `python dqn.py --seeds 2 --obs ball --out results\smoke.csv`

## Files

- `pong_env.py`: Gymnasium Pong, 40x40 grid, 3 observation modes
- `dqn.py`: DQN training with the paper's appendix hyperparameters
- `analyze.py`: the paper's three metrics, early vs late, plus a learning curve
- `DEVIATIONS.md`: every difference from the paper

## Next

Compare to the paper's reported DQN numbers, check the OSF code for input and epsilon, evaluate image mode, add A2C and PPO, report effect sizes with confidence intervals.

Back to the [project overview](README.md).
