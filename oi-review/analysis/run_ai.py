"""
run_ai.py - reproducible AI scoring runs for the OI rigor review.

Every call is logged (model, settings, prompt hash, date, raw reply), so a run can be
reported and repeated. Standard library only.

Windows CMD, from the folder with this file:

  1) Build the prompt from the frozen rubric (download the Check_Items and Rubric_Anchors
     tabs as CSV first). Re-run this whenever the rubric changes; the prompt version and
     its SHA-256 are printed and saved next to it.
         python run_ai.py build-prompt --check-items Check_Items.csv --anchors Rubric_Anchors.csv --version AI-P1.1

  2) List the sources to score in a CSV with columns: Paper ID, Source, Track, Text file
     (Track = Empirical or Review; Text file = a .txt of the full text, e.g. made with
     pdftotext). Then run one model:
         set ANTHROPIC_API_KEY=...            (or OPENAI_API_KEY for --provider openai)
         python run_ai.py score --sources sources.csv --prompt prompt_AI-P1.1.md --provider anthropic --model <exact model id> --rater "AI model 1" --out run1

     Run the second model the same way with --rater "AI model 2" and a different --out.

  Outputs in the --out folder:
     checks.csv      paste into the Checks tab (rows for that rater)
     judgment.csv    paste into Validation column H (model 1) or M (model 2)
     calls.jsonl     one line per API call: time, model, parameters, prompt SHA-256, raw reply
     run.json        run summary (what to report in the Methods)

  Test without an API key:
         python run_ai.py score --sources sources.csv --prompt prompt_AI-P1.1.md --provider mock --model mock --rater "AI model 1" --out test_run
"""
import argparse, csv, datetime, hashlib, json, os, random, re, sys, time, urllib.request

CHECK_CODES = ["SM1", "SM2", "SM3", "UA1", "UA2", "CT1", "CF1", "CF2", "CF3", "CF4", "CF5",
               "EA1", "EA2", "EA3", "RB1", "RB2", "TR1", "TR2", "TR3", "TR4", "SR1", "SR2", "SR3"]
EMPIRICAL_CHECKS = CHECK_CODES[:20]
REVIEW_CHECKS = CHECK_CODES[20:]
JUDGMENT = {"Empirical": ["CC"], "Review": ["PS", "HR", "MP", "CC"]}
CHECK_HEADERS = {  # must match the Checks tab header row
    "SM1": "SM1 system tested", "SM2": "SM2 system claimed", "SM3": "SM3 gap stated",
    "UA1": "UA1 n units reported", "UA2": "UA2 sessions as independent", "CT1": "CT1 controls (count)",
    "CF1": "CF1 comparison claimed", "CF2": "CF2 comparator run", "CF3": "CF3 same task+metric",
    "CF4": "CF4 tuning documented", "CF5": "CF5 limits stated", "EA1": "EA1 energy claim",
    "EA2": "EA2 energy measured", "EA3": "EA3 comparator", "RB1": "RB1 >1 day/batch/line",
    "RB2": "RB2 limitation stated", "TR1": "TR1 protocol", "TR2": "TR2 stim/rec params",
    "TR3": "TR3 data public", "TR4": "TR4 code public", "SR1": "SR1 sources named",
    "SR2": "SR2 terms reported", "SR3": "SR3 criteria reported"}


# ------------------------------------------------------------------ rubric -> prompt
def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))


def allowed_values(text):
    """'Y / N / U' -> ['Y','N','U']; 'Whole number 0-5' -> ['0'..'5']."""
    t = (text or "").strip()
    m = re.search(r"(\d+)\s*-\s*(\d+)", t)
    if "whole number" in t.lower() and m:
        return [str(i) for i in range(int(m.group(1)), int(m.group(2)) + 1)]
    return [v.strip() for v in t.split("/") if v.strip()]


def load_checks(path):
    rows = read_rows(path)
    hdr = next(i for i, r in enumerate(rows) if r and r[0].strip() == "Item")
    checks, judgment = {}, []
    for r in rows[hdr + 1:]:
        if len(r) < 6 or not r[0].strip():
            continue
        item, track, typ, code, question, answers = [c.strip() for c in r[:6]]
        if typ == "Rule" and code in CHECK_CODES:
            checks[code] = {"item": item, "track": track, "question": question, "allowed": allowed_values(answers)}
        elif typ == "Judgment":
            judgment.append((item, track))
    missing = [c for c in CHECK_CODES if c not in checks]
    if missing:
        sys.exit(f"Check_Items CSV is missing checks: {missing}")
    return checks, judgment


def load_anchors(path):
    """Returns {(track, item): {2:..., 1:..., 0:..., NA:...}} from Rubric_Anchors."""
    rows = read_rows(path)
    out, track = {}, "Empirical"
    for r in rows:
        if not r:
            continue
        if r[0].startswith("Rubric v1.1") and "review-track" in r[0]:
            track = "Review"
        if len(r) >= 7 and r[0].strip() in ("SM", "UA", "CT", "CF", "EA", "RB", "TR", "CC", "PS", "HR", "MP", "SR"):
            out[(track, r[0].strip())] = {"name": r[1].strip(), "question": r[2].strip(), "2": r[3].strip(),
                                          "1": r[4].strip(), "0": r[5].strip(), "NA": r[6].strip()}
    return out


def build_prompt(check_items, anchors, version):
    checks, _ = load_checks(check_items)
    anc = load_anchors(anchors)
    L = [f"# Prompt {version}: OI rigor appraisal (generated from the frozen rubric)", "",
         "You are appraising one source for a metascience review of organoid intelligence and biocomputing research.",
         "Read the full text provided. Answer ONLY from that text. Do not use outside knowledge about the paper or its authors.",
         "", "Rules:",
         "- For each check, give exactly one of the allowed answers.",
         "- U means the text does not report it or you cannot tell. Use U rather than guessing.",
         "- For every answer and score, give the location (section name, figure or table number, or page) and a paraphrase of at most 25 words. Do not quote more than 15 words.",
         "- Judgment items: score 0, 1, 2 or NA using the anchors exactly as written. If the anchors do not settle it, answer UNCLEAR.",
         "- Return ONLY a JSON object in the format at the end. No other text.", ""]
    for track, codes in (("Empirical", EMPIRICAL_CHECKS), ("Review", REVIEW_CHECKS)):
        L += [f"## {track} sources: factual checks", ""]
        for c in codes:
            ch = checks[c]
            L.append(f"- {c} ({ch['item']}): {ch['question']} Allowed: {' / '.join(ch['allowed'])}")
        L.append("")
        L += [f"## {track} sources: judgment items", ""]
        for it in JUDGMENT[track]:
            a = anc.get((track, it)) or anc.get(("Empirical", it))
            if not a:
                sys.exit(f"Rubric_Anchors CSV has no anchors for {track} {it}")
            L.append(f"- {it} ({a['name']}): {a['question']} 2 = {a['2']} | 1 = {a['1']} | 0 = {a['0']} | NA when: {a['NA']}")
        L.append("")
    L += ["## Output format", "",
          'Empirical source: {"checks": {"SM1": {"answer": "...", "where": "...", "evidence": "..."}, ... all of SM1-TR4 ...}, '
          '"judgment": {"CC": {"score": "0|1|2|NA|UNCLEAR", "where": "...", "evidence": "..."}}}',
          'Review source: {"checks": {"SR1": {...}, "SR2": {...}, "SR3": {...}}, "judgment": {"PS": {...}, "HR": {...}, "MP": {...}, "CC": {...}}}',
          "", "The source follows."]
    text = "\n".join(L) + "\n"
    spec = {c: checks[c]["allowed"] for c in CHECK_CODES}
    return text, spec


# ------------------------------------------------------------------ model calls
def call_anthropic(model, system, user, temperature, max_tokens):
    key = os.environ.get("ANTHROPIC_API_KEY") or sys.exit("Set ANTHROPIC_API_KEY first.")
    body = {"model": model, "max_tokens": max_tokens, "temperature": temperature, "system": system,
            "messages": [{"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    text = "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
    return text, {"response_id": r.get("id"), "model_reported": r.get("model"), "usage": r.get("usage"),
                  "stop_reason": r.get("stop_reason")}


def call_openai(model, system, user, temperature, max_tokens):
    key = os.environ.get("OPENAI_API_KEY") or sys.exit("Set OPENAI_API_KEY first.")
    body = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + key, "content-type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    return r["choices"][0]["message"]["content"], {"response_id": r.get("id"), "model_reported": r.get("model"),
                                                   "usage": r.get("usage"),
                                                   "system_fingerprint": r.get("system_fingerprint")}


def call_mock(model, system, user, temperature, max_tokens, spec=None, track="Empirical", seed=0):
    rng = random.Random(seed)
    codes = EMPIRICAL_CHECKS if track == "Empirical" else REVIEW_CHECKS
    out = {"checks": {c: {"answer": rng.choice(spec[c]), "where": "Methods", "evidence": "mock"} for c in codes},
           "judgment": {j: {"score": rng.choice(["0", "1", "2"]), "where": "Abstract", "evidence": "mock"}
                        for j in JUDGMENT[track]}}
    return json.dumps(out), {"response_id": f"mock-{seed}", "model_reported": "mock"}


# ------------------------------------------------------------------ validation of replies
def parse_reply(text, track, spec):
    t = text.strip()
    t = re.sub(r"^```(json)?|```$", "", t, flags=re.M).strip()
    try:
        d = json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, re.S)
        if not m:
            return None, "no JSON object in reply"
        try:
            d = json.loads(m.group(0))
        except json.JSONDecodeError as e:
            return None, f"invalid JSON: {e}"
    codes = EMPIRICAL_CHECKS if track == "Empirical" else REVIEW_CHECKS
    problems = []
    for c in codes:
        a = str(((d.get("checks") or {}).get(c) or {}).get("answer", "")).strip()
        if a not in spec[c]:
            problems.append(f"{c}={a!r} not in {spec[c]}")
    for j in JUDGMENT[track]:
        s = str(((d.get("judgment") or {}).get(j) or {}).get("score", "")).strip().upper()
        if s not in ("0", "1", "2", "NA", "UNCLEAR"):
            problems.append(f"{j}={s!r}")
    return d, ("; ".join(problems) if problems else None)


# ------------------------------------------------------------------ main
def cmd_build(a):
    text, spec = build_prompt(a.check_items, a.anchors, a.version)
    path = f"prompt_{a.version}.md"
    open(path, "w", encoding="utf-8").write(text)
    json.dump(spec, open(f"prompt_{a.version}.spec.json", "w"), indent=1)
    sha = hashlib.sha256(text.encode()).hexdigest()
    open(f"prompt_{a.version}.sha256", "w").write(sha + "\n")
    print(f"Wrote {path} ({len(text)} chars). SHA-256 {sha}")
    print("Record this hash on the Protocol tab and in the OSF registration. Do not edit the file by hand.")


def cmd_score(a):
    prompt = open(a.prompt, encoding="utf-8").read()
    sha = hashlib.sha256(prompt.encode()).hexdigest()
    spec_path = a.prompt.replace(".md", ".spec.json")
    spec = json.load(open(spec_path)) if os.path.exists(spec_path) else sys.exit(f"Missing {spec_path}; run build-prompt.")
    rows = [r for r in csv.DictReader(open(a.sources, newline="", encoding="utf-8-sig")) if r.get("Paper ID")]
    os.makedirs(a.out, exist_ok=True)
    calls = open(os.path.join(a.out, "calls.jsonl"), "a", encoding="utf-8")
    caller = {"anthropic": call_anthropic, "openai": call_openai, "mock": call_mock}[a.provider]
    checks_out, judg_out, failures = [], [], []
    for i, r in enumerate(rows):
        track = "Review" if r["Track"].strip().lower().startswith("rev") else "Empirical"
        text = open(r["Text file"], encoding="utf-8", errors="replace").read()
        if len(text) < 2000:
            failures.append((r["Paper ID"], f"text file only {len(text)} characters; full text needed"))
            continue
        user = f"Track: {track}\nPaper ID: {r['Paper ID']}\n\n=== FULL TEXT ===\n{text[:a.max_chars]}"
        reply, meta, parsed, err = None, {}, None, "not run"
        for attempt in range(1, a.retries + 2):
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            try:
                if a.provider == "mock":
                    reply, meta = call_mock(a.model, prompt, user, a.temperature, a.max_tokens, spec, track, i)
                else:
                    reply, meta = caller(a.model, prompt, user, a.temperature, a.max_tokens)
                parsed, err = parse_reply(reply, track, spec)
            except Exception as e:
                err = f"API error: {e}"
            calls.write(json.dumps({"time_utc": ts, "paper_id": r["Paper ID"], "attempt": attempt,
                                    "provider": a.provider, "model_requested": a.model,
                                    "temperature": a.temperature, "max_tokens": a.max_tokens,
                                    "prompt_file": os.path.basename(a.prompt), "prompt_sha256": sha,
                                    "text_chars_sent": min(len(text), a.max_chars),
                                    "text_truncated": len(text) > a.max_chars, **meta,
                                    "validation_error": err, "reply": reply}) + "\n")
            calls.flush()
            if parsed is not None and err is None:
                break
            time.sleep(a.pause)
        if parsed is None or err:
            failures.append((r["Paper ID"], err))
            continue
        codes = EMPIRICAL_CHECKS if track == "Empirical" else REVIEW_CHECKS
        row = {"Paper ID": r["Paper ID"], "Source": r.get("Source", ""), "Track": track, "Rater": a.rater}
        for c in CHECK_CODES:
            row[CHECK_HEADERS[c]] = parsed["checks"][c]["answer"] if c in codes else ""
        row["Notes / evidence location"] = " | ".join(f"{c}: {parsed['checks'][c].get('where','')}" for c in codes)
        checks_out.append(row)
        for j in JUDGMENT[track]:
            jd = parsed["judgment"][j]
            judg_out.append({"Paper ID": r["Paper ID"], "Track": track, "Item": j, "Rater": a.rater,
                             "Score": str(jd.get("score", "")).upper(), "Where": jd.get("where", ""),
                             "Evidence": jd.get("evidence", "")})
        time.sleep(a.pause)
    calls.close()
    if checks_out:
        with open(os.path.join(a.out, "checks.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(checks_out[0])); w.writeheader(); w.writerows(checks_out)
    if judg_out:
        with open(os.path.join(a.out, "judgment.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(judg_out[0])); w.writeheader(); w.writerows(judg_out)
    summary = {"run_date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "provider": a.provider,
               "model_requested": a.model, "rater_label": a.rater, "temperature": a.temperature,
               "max_tokens": a.max_tokens, "max_chars": a.max_chars, "prompt_file": os.path.basename(a.prompt),
               "prompt_sha256": sha, "sources": len(rows), "scored": len(checks_out),
               "failed": [{"paper_id": p, "reason": e} for p, e in failures]}
    json.dump(summary, open(os.path.join(a.out, "run.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))
    if failures:
        print("\nSome sources failed. Fix the cause and re-run only those; calls.jsonl keeps every attempt.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build-prompt")
    b.add_argument("--check-items", required=True)
    b.add_argument("--anchors", required=True)
    b.add_argument("--version", required=True)
    s = sub.add_parser("score")
    s.add_argument("--sources", required=True)
    s.add_argument("--prompt", required=True)
    s.add_argument("--provider", choices=["anthropic", "openai", "mock"], required=True)
    s.add_argument("--model", required=True, help="exact, dated model id; record it in the Methods")
    s.add_argument("--rater", required=True, choices=["AI model 1", "AI model 2"])
    s.add_argument("--out", required=True)
    s.add_argument("--temperature", type=float, default=0.0)
    s.add_argument("--max-tokens", type=int, default=4000)
    s.add_argument("--max-chars", type=int, default=180000, help="longer texts are cut and the cut is logged")
    s.add_argument("--retries", type=int, default=2)
    s.add_argument("--pause", type=float, default=1.0)
    a = ap.parse_args()
    {"build-prompt": cmd_build, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
