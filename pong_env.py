"""Simplified Pong on a 40x40 grid, following the description in
Khajehnejad et al. (2024). The paper does not fully specify the environment,
so every choice below is an assumption and is listed in DEVIATIONS.md.

Episode = one rally attempt: it ends the first time the ball is missed.
Hits in an episode are counted in info["hits"].
"""
import numpy as np
import gymnasium as gym
from gymnasium import spaces

SIZE = 40
PADDLE_H = 8
PADDLE_X = 1          # paddle column; the miss line is x == 0
MAX_STEPS = 1000      # safety cap so a very good agent cannot run forever


class SimplePong(gym.Env):
    """Observation modes:
    image  : difference of the two most recent 40x40 frames, shape (1, 40, 40)
    full   : difference of [ball_x, ball_y, paddle_top, paddle_bottom] vectors
    ball   : difference of [ball_y_segment (1-8), ball_x] vectors
    Actions: 0 stay, 1 up, 2 down.
    Reward : +1 per step survived (the paper reports reward as episode length).
    """

    def __init__(self, obs_mode="image", seed=None, absolute=True):
        super().__init__()
        assert obs_mode in ("image", "full", "ball")
        self.obs_mode = obs_mode
        self.absolute = absolute
        self.action_space = spaces.Discrete(3)
        if obs_mode == "image":
            self.observation_space = spaces.Box(-1.0, 1.0, (2 if absolute else 1, SIZE, SIZE), np.float32)
        else:
            dim = 4 if obs_mode == "full" else 2
            if absolute:
                dim *= 2
            self.observation_space = spaces.Box(-SIZE, SIZE, (dim,), np.float32)
        self.rng = np.random.default_rng(seed)
        self._prev = None

    # ---- helpers -------------------------------------------------------
    def _frame(self):
        f = np.zeros((SIZE, SIZE), dtype=np.float32)
        f[self.py:self.py + PADDLE_H, PADDLE_X] = 0.5
        f[int(self.by), int(self.bx)] = 1.0
        return f

    def _vec(self):
        if self.obs_mode == "full":
            return np.array([self.bx, self.by, self.py, self.py + PADDLE_H], np.float32)
        seg = 1 + int(self.by) * 8 // SIZE
        return np.array([seg, self.bx], np.float32)

    def _state(self):
        cur = self._frame() if self.obs_mode == "image" else self._vec()
        prev = self._prev if self._prev is not None else cur
        self._prev = cur
        diff = cur - prev
        if self.obs_mode == "image":
            return np.stack([cur, diff]) if self.absolute else diff[None, :, :]
        return np.concatenate([cur, diff]) if self.absolute else diff

    # ---- gym API -------------------------------------------------------
    def reset(self, seed=None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.bx = SIZE - 2
        self.by = int(self.rng.integers(2, SIZE - 2))
        self.vx = -1
        self.vy = int(self.rng.choice([-1, 1]))
        self.py = int(self.rng.integers(0, SIZE - PADDLE_H))
        self.hits = 0
        self.steps = 0
        self._prev = None
        self._state()                      # prime the previous frame
        return self._state(), {"hits": 0}

    def step(self, action):
        self.steps += 1
        if action == 1:
            self.py = max(0, self.py - 1)
        elif action == 2:
            self.py = min(SIZE - PADDLE_H, self.py + 1)

        self.bx += self.vx
        self.by += self.vy
        if self.by <= 0:
            self.by, self.vy = 0, 1
        elif self.by >= SIZE - 1:
            self.by, self.vy = SIZE - 1, -1
        if self.bx >= SIZE - 1:
            self.bx, self.vx = SIZE - 1, -1

        terminated = False
        if self.bx <= PADDLE_X:
            if self.py <= self.by < self.py + PADDLE_H:
                self.hits += 1
                self.bx, self.vx = PADDLE_X + 1, 1
                # hitting the paddle edge nudges the angle
                self.vy = int(self.rng.choice([-1, 1]))
            else:
                terminated = True
        truncated = self.steps >= MAX_STEPS
        return self._state(), 1.0, terminated, truncated, {"hits": self.hits}
