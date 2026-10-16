import argparse
import csv
import os
import random
import time
from collections import deque

import numpy as np
import torch
import torch.nn as nn

from pong_env import SimplePong

torch.set_num_threads(1)


class QNet(nn.Module):
    def __init__(self, obs_mode, in_shape):
        super().__init__()
        if obs_mode == "image":
            self.body = nn.Sequential(
                nn.Conv2d(in_shape[0], 16, 5, 2), nn.ReLU(),
                nn.Conv2d(16, 32, 4, 2), nn.ReLU(),
                nn.Conv2d(32, 32, 4, 2), nn.ReLU(),
                nn.Flatten(),
                nn.Linear(32 * 3 * 3, 512), nn.ReLU(),
            )
        else:
            self.body = nn.Sequential(nn.Linear(in_shape[0], 512), nn.ReLU())
        self.head = nn.Linear(512, 3)

    def forward(self, x):
        return self.head(self.body(x))


def run_seed(seed, obs_mode, episodes, lr, buffer_size, batch, gamma,
             target_every, eps_start, eps_end, eps_decay_steps, absolute=True):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    env = SimplePong(obs_mode=obs_mode, seed=seed, absolute=absolute)
    shape = env.observation_space.shape
    q, q_target = QNet(obs_mode, shape), QNet(obs_mode, shape)
    q_target.load_state_dict(q.state_dict())
    opt = torch.optim.Adam(q.parameters(), lr=lr)
    buf = deque(maxlen=buffer_size)
    rows, total_steps = [], 0

    for ep in range(1, episodes + 1):
        s, _ = env.reset(seed=seed * 1000 + ep)
        done, ep_steps, hits = False, 0, 0
        while not done:
            eps = max(eps_end, eps_start - (eps_start - eps_end) * total_steps / eps_decay_steps)
            if random.random() < eps:
                a = random.randrange(3)
            else:
                with torch.no_grad():
                    a = int(q(torch.from_numpy(s).unsqueeze(0)).argmax())
            s2, r, term, trunc, info = env.step(a)
            done = term or trunc
            buf.append((s, a, r, s2, float(term)))
            s = s2
            total_steps += 1
            ep_steps += 1
            hits = info["hits"]

            if len(buf) >= batch:
                bs, ba, br, bs2, bd = zip(*random.sample(buf, batch))
                bs = torch.from_numpy(np.stack(bs))
                bs2 = torch.from_numpy(np.stack(bs2))
                ba = torch.tensor(ba)
                br = torch.tensor(br, dtype=torch.float32)
                bd = torch.tensor(bd, dtype=torch.float32)
                with torch.no_grad():
                    y = br + gamma * (1 - bd) * q_target(bs2).max(1).values
                pred = q(bs).gather(1, ba[:, None]).squeeze(1)
                loss = nn.functional.mse_loss(pred, y)
                opt.zero_grad()
                loss.backward()
                opt.step()
            if total_steps % target_every == 0:
                q_target.load_state_dict(q.state_dict())

        rows.append((seed, ep, hits, ep_steps))
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--seed-start", type=int, default=0)
    p.add_argument("--obs", default="image", choices=["image", "full", "ball"])
    p.add_argument("--episodes", type=int, default=70)
    p.add_argument("--lr", type=float, default=0.002)
    p.add_argument("--buffer", type=int, default=10000)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--gamma", type=float, default=0.95)
    p.add_argument("--target-every", type=int, default=10)
    p.add_argument("--eps-start", type=float, default=1.0)
    p.add_argument("--eps-end", type=float, default=0.05)
    p.add_argument("--eps-decay-steps", type=int, default=2000)
    p.add_argument("--diff-only", action="store_true")
    p.add_argument("--out", default="results/dqn_image.csv")
    a = p.parse_args()

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "episode", "hits", "steps"])
        for i in range(a.seed_start, a.seed_start + a.seeds):
            t = time.time()
            rows = run_seed(i, a.obs, a.episodes, a.lr, a.buffer, a.batch,
                            a.gamma, a.target_every, a.eps_start, a.eps_end,
                            a.eps_decay_steps, absolute=not a.diff_only)
            w.writerows(rows)
            f.flush()
            mean_hits = np.mean([r[2] for r in rows])
            print(f"seed {i}: mean hits/episode {mean_hits:.2f} ({time.time() - t:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
