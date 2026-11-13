"""
agreement.py - AI vs human agreement for the OI rigor review (Validation tab).

Usage (Windows CMD):
    1. In Google Sheets open the Validation tab, then File > Download > Comma-separated values (.csv)
    2. Put the CSV next to this file, then run:
           python agreement.py Validation.csv
       Optional: python agreement.py Validation.csv --boot 5000 --seed 1 --margin 0.15
    3. Fact checks (download the Checks tab as Checks.csv):
           python agreement.py --checks Checks.csv
       Per check: human-human agreement, AI sensitivity/specificity against the
       human consensus, and how often the two AI models agree (routing coverage).
    4. Turn AI check answers into item scores with the same rule as the sheet:
           python agreement.py --score AI_checks.csv > AI_item_scores.csv
       (AI_checks.csv has the Checks tab's columns, one row per paper.)

What it reports (all pre-registered; do not change after seeing data):
    - Linear-weighted Cohen's kappa and Gwet's AC2 for each rater pair
    - 95% CIs from a cluster bootstrap that resamples PAPERS (not items),
      because items within one paper are not independent
    - Primary test: is the AI interchangeable with a human rater?
          delta = mean(kappa(Tani, AI), kappa(Gabe, AI)) - kappa(Tani, Gabe)
      Decision with non-inferiority margin m (default 0.15):
          lower 95% bound of delta >  -m  -> AI non-inferior to a human rater
          upper 95% bound of delta <  -m  -> AI worse than a human rater
          otherwise                       -> inconclusive (report AI as exploratory)
    - Per-item exact agreement of AI vs human consensus and the routing rule
      (AI-assisted only if >= 70% exact agreement and off-by-2 on <= 10% of sources)

Only rows where both raters gave 0, 1 or 2 count; NA and UNCLEAR are counted separately.
Standard library only (no installs needed).
"""
import csv
import random
import sys
import argparse
from collections import defaultdict

CATS = (0, 1, 2)


def num(x):
    x = (x or "").strip()
    if x in ("0", "1", "2", "0.0", "1.0", "2.0"):
        return int(float(x))
    return None


def wkappa(pairs):
    """Linear-weighted Cohen's kappa for 0/1/2 scores."""
    n = len(pairs)
    if n == 0:
        return None
    do = sum(abs(a - b) for a, b in pairs) / n
    pa = [sum(1 for a, _ in pairs if a == k) / n for k in CATS]
    pb = [sum(1 for _, b in pairs if b == k) / n for k in CATS]
    de = sum(pa[i] * pb[j] * abs(i - j) for i in CATS for j in CATS)
    if de == 0:
        return None
    return 1 - do / de


def gwet_ac2(pairs):
    """Gwet's AC2 with linear weights, two raters, categories 0/1/2."""
    n = len(pairs)
    if n == 0:
        return None
    q = len(CATS)
    w = [[1 - abs(k - l) / (q - 1) for l in CATS] for k in CATS]
    tw = sum(sum(r) for r in w)
    pa = sum(w[a][b] for a, b in pairs) / n
    pi = [(sum(1 for a, _ in pairs if a == k) + sum(1 for _, b in pairs if b == k)) / (2 * n) for k in CATS]
    pe = tw / (q * (q - 1)) * sum(p * (1 - p) for p in pi)
    if pe == 1:
        return None
    return (pa - pe) / (1 - pe)


def exact(pairs):
    return sum(1 for a, b in pairs if a == b) / len(pairs) if pairs else None


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    hdr_i = next((i for i, r in enumerate(rows) if r and r[0].strip() == "Source"), None)
    if hdr_i is None:
        raise SystemExit("No header row starting with 'Source' found. Download the Validation tab as CSV.")
    hdr = [h.strip() for h in rows[hdr_i]]

    def col(prefix):
        for i, h in enumerate(hdr):
            if h.lower().startswith(prefix.lower()):
                return i
        raise SystemExit(f"Column starting with '{prefix}' not found in header: {hdr}")

    c = {"track": col("Track"), "item": col("Item"), "t": col("Tani"), "g": col("Gabe"),
         "cons": col("Human consensus"), "ai1": col("AI model 1"), "ai2": col("AI model 2"),
         "pid": col("Paper ID")}
    data = []
    for r in rows[hdr_i + 1:]:
        if len(r) <= c["pid"] or not r[c["pid"]].strip():
            continue
        get = lambda k: r[c[k]] if c[k] < len(r) else ""
        data.append({"pid": get("pid").strip(), "track": get("track").strip(), "item": get("item").strip(),
                     "t": get("t"), "g": get("g"), "cons": get("cons"), "ai1": get("ai1"), "ai2": get("ai2")})
    return data


def pairs_for(rows, x, y):
    out = []
    for r in rows:
        a, b = num(r[x]), num(r[y])
        if a is not None and b is not None:
            out.append((a, b))
    return out


def by_paper(data):
    papers = defaultdict(list)
    for r in data:
        papers[r["pid"]].append(r)
    return papers


def boot(papers, stat_fn, B, rng):
    ids = list(papers)
    vals = []
    for _ in range(B):
        sample = [r for pid in (rng.choice(ids) for _ in ids) for r in papers[pid]]
        v = stat_fn(sample)
        if v is not None:
            vals.append(v)
    if len(vals) < B * 0.5:
        return None, None, len(vals)
    vals.sort()
    lo = vals[int(0.025 * (len(vals) - 1))]
    hi = vals[int(0.975 * (len(vals) - 1))]
    return lo, hi, len(vals)


def fmt(v):
    return "  -  " if v is None else f"{v:5.2f}"


# ---------------------------------------------------------------- fact checks
CHECKS = ["SM1", "SM2", "SM3", "UA1", "UA2", "CT1", "CF1", "CF2", "CF3", "CF4", "CF5",
          "EA1", "EA2", "EA3", "RB1", "RB2", "TR1", "TR2", "TR3", "TR4", "SR1", "SR2", "SR3"]
CATEGORICAL = {"SM1", "SM2", "CT1", "EA2"}   # not Y/N: exact agreement only


def norm(x):
    x = (x or "").strip()
    return x.upper() if len(x) <= 1 else x.lower()


def is_y(x):
    return norm(x) == "Y"


def item_scores(c):
    """Same rules as Check_Items / the Checks tab formulas. c: dict check -> answer.
    Returns dict item -> 0/1/2/'NA'/'' ('' = incomplete)."""
    g = lambda k: norm(c.get(k, ""))
    out = {}
    # SM
    if not g("SM1") or not g("SM2"):
        out["SM"] = ""
    elif g("SM1") == g("SM2"):
        out["SM"] = 2
    else:
        out["SM"] = "" if not g("SM3") else (1 if g("SM3") == "Y" else 0)
    # UA
    if not g("UA1"):
        out["UA"] = ""
    elif g("UA1") == "na":
        out["UA"] = "NA"
    elif g("UA1") != "Y":
        out["UA"] = 0
    else:
        out["UA"] = "" if not g("UA2") else {"Y": 0, "N": 2}.get(g("UA2"), 1)
    # CT
    try:
        out["CT"] = min(int(float(g("CT1"))), 2) if g("CT1") else ""
    except ValueError:
        out["CT"] = ""
    # CF
    if not g("CF1"):
        out["CF"] = ""
    elif g("CF1") == "N":
        out["CF"] = "NA"
    elif not g("CF2"):
        out["CF"] = ""
    elif g("CF2") != "Y":
        out["CF"] = 0
    elif not all(g(k) for k in ("CF3", "CF4", "CF5")):
        out["CF"] = ""
    elif g("CF3") == "Y" and g("CF4") == "Y":
        out["CF"] = 2
    elif (g("CF3") == "Y" or g("CF4") == "Y") and g("CF5") == "Y":
        out["CF"] = 1
    else:
        out["CF"] = 0
    # EA
    if not g("EA1"):
        out["EA"] = ""
    elif g("EA1") == "N":
        out["EA"] = "NA"
    elif not g("EA2"):
        out["EA"] = ""
    elif g("EA2") == "none":
        out["EA"] = 0
    elif g("EA2") == "partial":
        out["EA"] = 1
    else:
        out["EA"] = "" if not g("EA3") else (2 if g("EA3") == "Y" else 1)
    # RB
    if not g("RB1"):
        out["RB"] = ""
    elif g("RB1") == "Y":
        out["RB"] = 2
    else:
        out["RB"] = "" if not g("RB2") else (1 if g("RB2") == "Y" else 0)
    # TR
    t = [g(k) for k in ("TR1", "TR2", "TR3", "TR4")]
    if not all(t):
        out["TR"] = ""
    else:
        meth = t[0] == "Y" and t[1] == "Y"
        share = t[2] == "Y" or t[3] == "Y"
        out["TR"] = 2 if (meth and share) else (1 if (meth or share) else 0)
    # SR
    s = [g(k) for k in ("SR1", "SR2", "SR3")]
    if not all(s):
        out["SR"] = ""
    else:
        ny = sum(1 for v in s if v == "Y")
        out["SR"] = 2 if ny == 3 else (1 if ny >= 1 else 0)
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, c - h), min(1.0, c + h)


def cohen_nominal(pairs):
    n = len(pairs)
    if n == 0:
        return None
    cats = sorted({x for p in pairs for x in p})
    po = sum(1 for a, b in pairs if a == b) / n
    pe = sum((sum(1 for a, _ in pairs if a == k) / n) * (sum(1 for _, b in pairs if b == k) / n) for k in cats)
    return None if pe == 1 else (po - pe) / (1 - pe)


def gwet_ac1(pairs):
    n = len(pairs)
    if n == 0:
        return None
    cats = sorted({x for p in pairs for x in p})
    q = len(cats)
    if q < 2:
        return 1.0
    po = sum(1 for a, b in pairs if a == b) / n
    pi = [(sum(1 for a, _ in pairs if a == k) + sum(1 for _, b in pairs if b == k)) / (2 * n) for k in cats]
    pe = sum(p * (1 - p) for p in pi) / (q - 1)
    return (po - pe) / (1 - pe)


def load_checks(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    hdr_i = next((i for i, r in enumerate(rows) if r and r[0].strip() == "Paper ID"), None)
    if hdr_i is None:
        raise SystemExit("No header row starting with 'Paper ID' found. Download the Checks tab (not Validation) as CSV.")
    hdr = [h.strip() for h in rows[hdr_i]]
    col = {}
    for i, h in enumerate(hdr):
        code = h.split(" ")[0]
        if code in CHECKS and code not in col:
            col[code] = i
        if h in ("Track", "Rater"):
            col[h] = i
    missing = [k for k in CHECKS if k not in col]
    if missing:
        raise SystemExit(f"Checks CSV is missing columns for: {missing}")
    data = defaultdict(dict)   # pid -> rater -> {check: answer}
    track = {}
    for r in rows[hdr_i + 1:]:
        if not r or not r[0].strip():
            continue
        pid = r[0].strip()
        rater = r[col["Rater"]].strip() if "Rater" in col and col["Rater"] < len(r) else "AI"
        track[pid] = r[col["Track"]].strip() if "Track" in col and col["Track"] < len(r) else ""
        data[pid][rater] = {k: (r[col[k]] if col[k] < len(r) else "") for k in CHECKS}
    return data, track


def checks_report(path):
    data, track = load_checks(path)
    print(f"Sources: {len(data)}  (each source counts once per check, so CIs are Wilson intervals over sources)\n")
    print("Y/N checks: 'U', 'N' and 'request' all count as not-Y, exactly as in the scoring rule.")
    print("Sensitivity = AI says Y when consensus says Y; specificity = AI says not-Y when consensus says not-Y.\n")
    hdr = (f"{'Check':6s} {'n':>3s} {'H-H exact':>9s} {'H-H AC1':>8s} {'Cons-AI1 exact':>14s} "
           f"{'sens [95% CI]':>18s} {'spec [95% CI]':>18s} {'AI1=AI2':>8s} {'acc|agree':>10s} {'U rate':>7s}")
    print(hdr)
    flags = []
    for k in CHECKS:
        binary = k not in CATEGORICAL
        f = (lambda x: "Y" if is_y(x) else "notY") if binary else norm
        hh, ca, both, agree_ok, us, nus = [], [], 0, 0, 0, 0
        tp = fn = tn = fp = 0
        for pid, rr in data.items():
            t, g_ = rr.get("Tani", {}).get(k, ""), rr.get("Gabe", {}).get(k, "")
            c, a1, a2 = (rr.get(x, {}).get(k, "") for x in ("Consensus", "AI model 1", "AI model 2"))
            for v in (t, g_, a1, a2):
                if v.strip():
                    nus += 1
                    us += norm(v) == "U"
            if t.strip() and g_.strip():
                hh.append((f(t), f(g_)))
            if c.strip() and a1.strip():
                ca.append((f(c), f(a1)))
                if binary:
                    if is_y(c):
                        tp += is_y(a1); fn += not is_y(a1)
                    else:
                        tn += not is_y(a1); fp += is_y(a1)
                if a2.strip():
                    both += 1
                    if f(a1) == f(a2):
                        agree_ok += 1 if f(a1) == f(c) else 0
            if c.strip() and a1.strip() and a2.strip() and f(a1) != f(a2):
                pass
        n_ag = sum(1 for pid, rr in data.items()
                   if all(rr.get(x, {}).get(k, "").strip() for x in ("Consensus", "AI model 1", "AI model 2"))
                   and f(rr["AI model 1"][k]) == f(rr["AI model 2"][k]))
        n = len(ca)
        if not n and not hh:
            print(f"{k:6s} {0:3d}   waiting")
            continue
        hx = f"{exact(hh):9.0%}" if hh else f"{'-':>9s}"
        hac = f"{gwet_ac1(hh):8.2f}" if hh else f"{'-':>8s}"
        cx = f"{exact(ca):14.0%}" if ca else f"{'-':>14s}"
        if binary and (tp + fn):
            lo, hi = wilson(tp, tp + fn); sens = f"{tp/(tp+fn):.2f} [{lo:.2f},{hi:.2f}]"
        else:
            sens = "-" if binary else "n/a"
        if binary and (tn + fp):
            lo, hi = wilson(tn, tn + fp); spec = f"{tn/(tn+fp):.2f} [{lo:.2f},{hi:.2f}]"
        else:
            spec = "-" if binary else "n/a"
        cov = f"{n_ag/both:8.0%}" if both else f"{'-':>8s}"
        acc = f"{agree_ok/n_ag:10.0%}" if n_ag else f"{'-':>10s}"
        ur = f"{us/nus:7.0%}" if nus else f"{'-':>7s}"
        print(f"{k:6s} {max(n, len(hh)):3d} {hx} {hac} {cx} {sens:>18s} {spec:>18s} {cov} {acc} {ur}")
        if binary and (tp + fn) and (tp + fn) < 5:
            flags.append(f"{k}: only {tp+fn} consensus-Y sources, so sensitivity is not estimable in any useful way")
        if nus and us / nus > 0.2:
            flags.append(f"{k}: U on {us/nus:.0%} of answers; reword the question before freezing")
    # derived item scores per rater
    print("\nItem scores computed from checks (same rule as the sheet), consensus vs AI model 1:")
    items = ["SM", "UA", "CT", "CF", "EA", "RB", "TR", "SR"]
    for it in items:
        p = []
        for pid, rr in data.items():
            if "Consensus" in rr and "AI model 1" in rr:
                a, b = item_scores(rr["Consensus"]).get(it, ""), item_scores(rr["AI model 1"]).get(it, "")
                if a != "" and b != "":
                    p.append((a, b))
        if not p:
            print(f"  {it}: waiting")
            continue
        ex = sum(1 for a, b in p if a == b)
        lo, hi = wilson(ex, len(p))
        print(f"  {it}: {ex}/{len(p)} exact ({ex/len(p):.0%}, 95% CI {lo:.0%}-{hi:.0%})")
    if flags:
        print("\nFLAGS")
        for fl in flags:
            print("  - " + fl)
    print("\nReminder: with ~14 empirical sources, a check needs about 13/14 correct before its lower 95% bound passes 0.70."
          " Treat per-check results as screening, not proof; the blind audit on the main corpus is the real check.")


def score_file(path):
    data, track = load_checks(path)
    w = csv.writer(sys.stdout)
    w.writerow(["Paper ID", "Rater", "Track", "SM", "UA", "CT", "CF", "EA", "RB", "TR", "SR"])
    for pid, rr in data.items():
        for rater, c in rr.items():
            s = item_scores(c)
            emp = track.get(pid, "").lower().startswith("emp")
            row = [s[i] if (emp and i != "SR") or (not emp and i == "SR") else "" for i in
                   ("SM", "UA", "CT", "CF", "EA", "RB", "TR", "SR")]
            w.writerow([pid, rater, track.get(pid, "")] + row)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--checks":
        return checks_report(sys.argv[2])
    if len(sys.argv) >= 3 and sys.argv[1] == "--score":
        return score_file(sys.argv[2])
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261108)
    ap.add_argument("--margin", type=float, default=0.15)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    data = load(a.csv)
    papers = by_paper(data)
    print(f"Sources: {len(papers)}   rows: {len(data)}   bootstrap: {a.boot} resamples of papers\n")

    pair_defs = [("Tani vs Gabe (human-human)", "t", "g"), ("Tani vs AI model 1", "t", "ai1"),
                 ("Gabe vs AI model 1", "g", "ai1"), ("Consensus vs AI model 1", "cons", "ai1"),
                 ("AI model 1 vs AI model 2", "ai1", "ai2"), ("Consensus vs AI model 2", "cons", "ai2")]
    print(f"{'Pair':32s} {'n':>4s} {'exact':>6s} {'kappa_w':>8s} {'95% CI':>14s} {'AC2':>6s} {'95% CI':>14s}")
    results = {}
    for name, x, y in pair_defs:
        p = pairs_for(data, x, y)
        if not p:
            print(f"{name:32s} {0:4d}   (no scored pairs yet)")
            continue
        k, g = wkappa(p), gwet_ac2(p)
        klo, khi, _ = boot(papers, lambda s: wkappa(pairs_for(s, x, y)), a.boot, rng)
        glo, ghi, _ = boot(papers, lambda s: gwet_ac2(pairs_for(s, x, y)), a.boot, rng)
        results[(x, y)] = k
        print(f"{name:32s} {len(p):4d} {exact(p):6.0%} {fmt(k):>8s} [{fmt(klo)},{fmt(khi)}] {fmt(g):>6s} [{fmt(glo)},{fmt(ghi)}]")

    # Primary test
    def delta(stat):
        def f(s):
            hh = stat(pairs_for(s, "t", "g"))
            ta = stat(pairs_for(s, "t", "ai1"))
            ga = stat(pairs_for(s, "g", "ai1"))
            if None in (hh, ta, ga):
                return None
            return (ta + ga) / 2 - hh
        return f

    print("\nPRIMARY TEST: AI interchangeable with a human rater?  delta = mean(human vs AI) - (human vs human)")
    for label, stat in (("weighted kappa (primary)", wkappa), ("Gwet AC2 (sensitivity)", gwet_ac2)):
        d = delta(stat)(data)
        if d is None:
            print(f"  {label}: not enough data yet")
            continue
        lo, hi, nb = boot(papers, delta(stat), a.boot, rng)
        if lo is None:
            print(f"  {label}: delta {d:+.2f}, CI not estimable (too few papers with all three raters)")
            continue
        if lo > -a.margin:
            verdict = "NON-INFERIOR: AI acceptable as a rater"
        elif hi < -a.margin:
            verdict = "INFERIOR: AI worse than a human rater"
        else:
            verdict = "INCONCLUSIVE: report AI as exploratory; humans score the corpus"
        print(f"  {label}: delta {d:+.2f}  95% CI [{lo:+.2f}, {hi:+.2f}]  margin -{a.margin:.2f}  ->  {verdict}")

    # Per-item routing
    print("\nPER ITEM (consensus vs AI model 1)  rule: >=70% exact AND off-by-2 on <=10% of sources")
    print(f"{'Item':10s} {'n':>4s} {'exact':>6s} {'off2':>5s} {'NA/UNCL':>8s}  routing")
    items = sorted({(r["track"], r["item"]) for r in data})
    for track, item in items:
        rows = [r for r in data if r["track"] == track and r["item"] == item]
        p = pairs_for(rows, "cons", "ai1")
        mism = sum(1 for r in rows if (r["cons"].strip() and r["ai1"].strip()) and (num(r["cons"]) is None or num(r["ai1"]) is None) and r["cons"].strip() != r["ai1"].strip())
        if not p:
            print(f"{track[:3]+' '+item:10s} {0:4d}   waiting")
            continue
        off2 = sum(1 for x, y in p if abs(x - y) == 2)
        ok = exact(p) >= 0.70 and off2 <= max(1, round(0.10 * len(p)))
        print(f"{track[:3]+' '+item:10s} {len(p):4d} {exact(p):6.0%} {off2:5d} {mism:8d}  {'AI-assisted' if ok else 'HUMAN-SCORE'}")

    unclear = sum(1 for r in data if r["ai1"].strip().upper() == "UNCLEAR")
    filled = sum(1 for r in data if r["ai1"].strip())
    if filled:
        print(f"\nAI model 1 said UNCLEAR on {unclear} of {filled} rows ({unclear/filled:.0%}); above ~10% means it is dodging hard items.")


if __name__ == "__main__":
    main()
