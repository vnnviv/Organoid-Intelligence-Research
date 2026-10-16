import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

SPLIT = 17

df = pd.read_csv(sys.argv[1])
df["ace"] = (df["hits"] == 0).astype(float) * 100
df["long"] = (df["hits"] >= 3).astype(float) * 100
df["phase"] = (df["episode"] > SPLIT).map({False: "early", True: "late"})

per_seed = df.groupby(["seed", "phase"])[["hits", "ace", "long"]].mean().unstack()
print(f"seeds: {df['seed'].nunique()}, episodes per seed: {df['episode'].max()}\n")
for m, label in [("hits", "hits per episode"), ("ace", "% aces"), ("long", "% long rallies (>=3)")]:
    early, late = per_seed[(m, "early")], per_seed[(m, "late")]
    t, p = stats.ttest_rel(late, early)
    print(f"{label:<24} early {early.mean():6.2f}  late {late.mean():6.2f}  "
          f"paired t={t:5.2f} p={p:.3f}")

curve = df.groupby("episode")["hits"].agg(["mean", "sem"])
plt.figure(figsize=(6, 4))
plt.plot(curve.index, curve["mean"])
plt.fill_between(curve.index, curve["mean"] - curve["sem"], curve["mean"] + curve["sem"], alpha=0.3)
plt.xlabel("episode")
plt.ylabel("mean hits per episode")
plt.title("DQN learning curve")
out = sys.argv[1].replace(".csv", ".png")
plt.tight_layout()
plt.savefig(out, dpi=150)
print(f"\nsaved {out}")
