"""Build recording prompt lists for Nepali TTS.

Outputs (TSV: id, category, source, text):
  all_prompts.tsv          every prompt with a stable ID
  voice_talent.tsv         ~2000 prompts for each voice talent, ordered so any prefix is balanced
  contributor_XX.tsv       per-contributor packs: shared core + domain + unique coverage text

Coverage text is chosen from OpenSLR 43/54 transcripts (CC BY-SA 4.0) by greedy
akshara / akshara-bigram coverage.

Usage:
  python build_prompts.py --metadata metadata.csv --slr54 utt_spk_text.tsv --out prompts/
"""

import argparse
import collections
import csv
import random
import re
from pathlib import Path

from domain_prompts import build as build_domain

# One akshara: independent vowel, or consonant cluster (C + (virama C)*) with optional nukta,
# dependent vowel sign or trailing virama, followed by optional anusvara/chandrabindu/visarga.
AKSHARA = re.compile(
    r"(?:[अ-औॠॡ]"
    r"|[क-हक़-य़]़?(?:्[क-हक़-य़]़?)*"
    r"(?:[ा-ौॢॣ]|्)?)"
    r"[ऀ-ः]?"
)
ALLOWED = re.compile(r"^[ऀ-ॿ ,?!।]+$")
WORD = re.compile(r"[\u0900-\u0963\u0966-\u097f]+")


def units(text):
    words = text.replace("।", " ").replace(",", " ").replace("?", " ").replace("!", " ").split()
    out = set()
    for w in words:
        aks = AKSHARA.findall(w)
        out.update(aks)
        out.update(f"{a}|{b}" for a, b in zip(aks, aks[1:]))
        if aks:
            out.add(f"#|{aks[0]}")
            out.add(f"{aks[-1]}|#")
    return out


def load_candidates(metadata, slr54, min_word_freq=3, min_common=0.9):
    texts = set()
    with open(metadata, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            texts.add(r["transcript"].strip())
    with open(slr54, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3:
                texts.add(parts[2].strip())
    texts = {re.sub(r"\s+", " ", t).replace(" ।", "।") for t in texts}
    # Word frequency across the corpus: rare words are mostly typos, foreign names or obscure terms.
    wfreq = collections.Counter(w for t in texts for w in WORD.findall(t))
    out = []
    for t in texts:
        words = WORD.findall(t)
        if not (5 <= len(words) <= 25 and 25 <= len(t) <= 180):
            continue
        if not ALLOWED.match(t) or re.search(r"[०-९]|[?!।]{2,}", t):
            continue
        if sum(wfreq[w] >= min_word_freq for w in words) / len(words) < min_common:
            continue
        out.append(t)
    return sorted(out)


def greedy_cover(cands, k, exclude_units=(), seed=0):
    """Pick k sentences maximizing rarity-weighted new units per character (lazy greedy)."""
    freq = collections.Counter(u for t in cands for u in units(t))
    weight = {u: 1.0 for u in freq}
    covered = collections.Counter({u: 1 for u in exclude_units})
    cand_units = {t: units(t) for t in cands}

    def gain(t):
        # diminishing returns: a unit counts less each time it is already covered (up to 3x)
        return sum(weight[u] / (1 + covered[u]) for u in cand_units[t] if covered[u] < 3) / len(t) ** 0.5

    rng = random.Random(seed)
    pool = list(cands)
    rng.shuffle(pool)
    scores = {t: gain(t) for t in pool}
    chosen = []
    while len(chosen) < k and scores:
        best = max(scores, key=scores.get)
        fresh = gain(best)
        if fresh + 1e-12 < scores[best]:
            scores[best] = fresh
            continue
        chosen.append(best)
        del scores[best]
        for u in cand_units[best]:
            covered[u] += 1
    return chosen


def write_tsv(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "category", "source", "text"])
        w.writerows(rows)


def interleave(domain, coverage, seed):
    """Mix domain and coverage evenly so any prefix of the list has both."""
    rng = random.Random(seed)
    domain, coverage = domain[:], coverage[:]
    rng.shuffle(domain)
    out = []
    ratio = len(coverage) / max(1, len(domain))
    acc = 0.0
    ci = 0
    for d in domain:
        out.append(d)
        acc += ratio
        while acc >= 1 and ci < len(coverage):
            out.append(coverage[ci])
            ci += 1
            acc -= 1
    out.extend(coverage[ci:])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", required=True, help="HF openSLR-Nepali metadata.csv")
    ap.add_argument("--slr54", required=True, help="OpenSLR 54 utt_spk_text.tsv")
    ap.add_argument("--out", default="prompts")
    ap.add_argument("--talent_coverage", type=int, default=1400)
    ap.add_argument("--n_templated", type=int, default=400)
    ap.add_argument("--contributors", type=int, default=8)
    ap.add_argument("--core", type=int, default=50, help="prompts every contributor reads")
    ap.add_argument("--contrib_domain", type=int, default=100)
    ap.add_argument("--contrib_coverage", type=int, default=150)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    domain = [(f"cc_{i:04d}", cat, "domain", t)
              for i, (cat, t) in enumerate(build_domain(args.n_templated, args.seed), 1)]

    cands = load_candidates(args.metadata, args.slr54)
    n_contrib_cov = args.contributors * args.contrib_coverage
    picked = greedy_cover(cands, args.talent_coverage + n_contrib_cov,
                          exclude_units={u for *_, t in domain for u in units(t)}, seed=args.seed)
    coverage = [(f"cv_{i:05d}", "coverage", "openslr", t) for i, t in enumerate(picked, 1)]
    talent_cov, contrib_cov = coverage[:args.talent_coverage], coverage[args.talent_coverage:]

    write_tsv(out / "all_prompts.tsv", domain + coverage)
    write_tsv(out / "voice_talent.tsv", interleave(domain, talent_cov, args.seed))

    rng = random.Random(args.seed + 1)
    core = rng.sample(domain, args.core)
    rest_domain = [d for d in domain if d not in core]
    for c in range(args.contributors):
        dom = [rest_domain[(c * args.contrib_domain + j) % len(rest_domain)] for j in range(args.contrib_domain)]
        cov = contrib_cov[c * args.contrib_coverage:(c + 1) * args.contrib_coverage]
        write_tsv(out / f"contributor_{c + 1:02d}.tsv", core + interleave(dom, cov, args.seed + c))

    # Report
    all_u = collections.Counter(u for t in cands for u in units(t))
    talent_u = {u for *_, t in domain + talent_cov for u in units(t)}
    ak = [u for u in all_u if "|" not in u]
    print(f"candidates: {len(cands)}  domain: {len(domain)}  coverage picked: {len(picked)}")
    print(f"talent list: {len(domain) + len(talent_cov)} prompts, "
          f"aksharas covered {sum(1 for u in ak if u in talent_u)}/{len(ak)} "
          f"({sum(all_u[u] for u in ak if u in talent_u) / sum(all_u[u] for u in ak):.2%} of corpus akshara tokens)")
    words = sum(len(t.split()) for *_, t in domain + talent_cov)
    print(f"talent words: {words}  est. audio at ~2.2 words/s: {words / 2.2 / 3600:.2f} h")


if __name__ == "__main__":
    main()
