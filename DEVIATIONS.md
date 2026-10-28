# Deviations from the original paper

Replication of Khajehnejad et al. (2024), "Biological Neurons Compete with Deep Reinforcement Learning in Sample Efficiency in a Simulated Gameworld" (arXiv:2405.16946).

Log every place this replication differs from the paper or its released code. Add a row when you make the change, not afterward.

## Environment

| Item | Original | Replication | Why it matters |
|------|----------|-------------|----------------|
| PyTorch | 1.8.1 | 2.14.0 | API and default behavior changes |
| Game environment | OpenAI Gym | Gymnasium 1.4.0 | Different reset/step signatures |
| Python | not stated | 3.12 | |
| Hardware | 2.3 GHz quad-core Intel i5 | (fill in) | Speed only |

## Setup

| Item | Original | Replication | Reason |
|------|----------|-------------|--------|
| Episodes per run | 70 | 70 | Same |
| Seeds | 150 | 50 (headline run) | Fewer seeds; 15-seed runs were too noisy to cite |
| Input designs | image, paddle+ball position, ball position | full-state vector evaluated; image runs but is unevaluated; ball mode smoke-tested only | Time |
| Algorithms | DQN, A2C, PPO | DQN only | A2C and PPO not implemented |
| Hyperparameters | per paper appendix A.4 | per appendix A.4 where stated; Adam, MSE, third conv layer and epsilon schedule are my choices | Paper silent |

## Code and data

- Source of original code and data: (OSF link from the paper's Code Availability section)
- Date downloaded:
- Original code found and used: yes / no
- Parts rebuilt from the appendix instead:

## Pong environment

The paper describes the environment only as a simplified Pong rendered as a 40x40 grayscale image. Note every assumption made where the paper or code is silent (ball speed, paddle size, reward structure, episode termination).

- Grid: 40x40. Paddle height 8 cells, in column 1; a miss is the ball reaching column 0 without the paddle covering its row.
- Ball: starts at x=38 moving left at 1 cell/step, vertical speed +/-1 chosen at random; bounces off top, bottom and right walls.
- Paddle: moves 1 cell/step. Actions are stay / up / down. Start row is random.
- Paddle hit: ball reverses and the new vertical direction is re-randomized (+/-1). The paper does not say how angle changes.
- Reward: +1 per step survived (episode length). The paper does not give its reward function in the text I read.
- Episode = one rally. It ends at the first miss, or at a 1000-step cap that I added.
- Observations (current default, see Oct 15 section): image = current frame plus difference of the last two frames (2 channels). Full = 4-d [ball x, ball y, paddle top, paddle bottom] current state concatenated with its difference. Ball = 2-d [y segment 1-8, x], same construction. The original diff-only build is available via `--diff-only`.
- Network (image): 3 conv layers (1-16-32-32 channels, kernels 5/4/4, stride 2), then a 512-unit linear layer. The paper gives kernels {5,4}, stride 2, hidden 512; the third conv layer and channel counts are my guess.
- Optimizer is Adam and loss is MSE. Neither is stated in the paper as far as I checked.
- Epsilon-greedy decays linearly from 1.0 to 0.05. The schedule is my assumption; code default is 2000 steps, results below use 300 (`--eps-decay-steps 300`).
- Target network syncs every 10 environment steps; one gradient step per environment step once the buffer holds a batch.
- Sanity check (random policy, 500 episodes): 0.28 mean hits, 82% aces, 2% long rallies. A hand-written tracking policy reaches the 1000-step cap.

## Results differences

Replication column is the 50-seed run (full-state, absolute + diff input, epsilon decay 300), early = episodes 1-17, late = episodes 18-70. The paper's DQN numbers have not been entered; I have not yet compared against its reported results or the OSF code.

| Metric | Paper (DQN) | Replication early -> late | Notes |
|--------|-------------|---------------------------|-------|
| Hits per rally | not yet compared | 0.41 -> 0.57 (p < 0.001) | Random policy: 0.28 |
| % aces | not yet compared | 78.8 -> 72.3 (p = 0.001) | Random policy: 82%. Kagan et al. 2022 controls ace about 50%, so this environment is harder |
| % long rallies | not yet compared | 4.1 -> 5.9 (p = 0.010) | I count >= 3 hits; the paper's threshold is more than 3, so mine is looser |

Statistics: paired t-tests across seeds on early vs late means; seeds treated as independent; no multiple-comparison correction across the three metrics. No effect sizes or confidence intervals yet.

## Other changes

-

## Observation change (Oct 15)

- The first build used frame/vector differences only, with no absolute positions. With eps decay 300 and 15 seeds, hits per episode went 0.38 -> 0.29 (p=0.021). The agent got worse.
- Current default adds the current state to the difference (image: 2 channels; vector modes: current + diff concatenated). `--diff-only` restores the old behavior. This is my fix and is not confirmed against the paper's code (check OSF).
- With absolute state (full, 15 seeds, eps decay 300): hits 0.44 -> 0.60 (p=0.043), aces 80% -> 71% (p=0.002), long rallies 4.3% -> 6.4% (p=0.09, not significant). Effect size varies between machines and seeds. Image mode has not been tested.
- Epsilon decay was set to 300 steps for these tests (`--eps-decay-steps 300`). The code default is still 2000.
