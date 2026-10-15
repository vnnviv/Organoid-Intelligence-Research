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
| Episodes per run | 70 | | |
| Seeds | 150 | | |
| Input designs | image, paddle+ball position, ball position | | |
| Algorithms | DQN, A2C, PPO | | |
| Hyperparameters | per paper appendix A.4 | | |

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
- Observations: image = difference of the last two 40x40 frames. Full = 4-d [ball x, ball y, paddle top, paddle bottom] difference. Ball = 2-d [y segment 1-8, x] difference.
- Network (image): 3 conv layers (1-16-32-32 channels, kernels 5/4/4, stride 2), then a 512-unit linear layer. The paper gives kernels {5,4}, stride 2, hidden 512; the third conv layer and channel counts are my guess.
- Optimizer is Adam and loss is MSE. Neither is stated in the paper as far as I checked.
- Epsilon-greedy decays linearly from 1.0 to 0.05 over 2000 steps. The schedule is my assumption.
- Target network syncs every 10 environment steps; one gradient step per environment step once the buffer holds a batch.
- Sanity check (random policy, 500 episodes): 0.28 mean hits, 82% aces, 2% long rallies. A hand-written tracking policy reaches the 1000-step cap.

## Results differences

| Metric | Paper | Replication | Notes |
|--------|-------|-------------|-------|
| Hits per rally | | | |
| % aces | | | |
| % long rallies | | | |

## Other changes

-
