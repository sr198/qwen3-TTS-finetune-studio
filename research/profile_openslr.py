"""Reproduce the OpenSLR Nepali dataset findings in the handover doc.

Downloads only metadata (no audio): the HF dataset's metadata.csv and OpenSLR 54's
utt_spk_text.tsv, then reports what the dataset contains, recovers SLR54 speaker IDs,
breaks down SLR43 speakers and sizes TTS-grade filters.

Usage:
  python research/profile_openslr.py --cache data/openslr_meta
"""

import argparse
import collections
import csv
import statistics as st
import urllib.request
from pathlib import Path

HF_METADATA = "https://huggingface.co/datasets/Aananda-giri/openSLR-Nepali/resolve/main/metadata.csv"
SLR54_TSV = "https://www.openslr.org/resources/54/utt_spk_text.tsv"


def fetch(url, path):
    if not path.exists():
        print(f"downloading {url}")
        urllib.request.urlretrieve(url, path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="data/openslr_meta")
    args = ap.parse_args()
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    meta = fetch(HF_METADATA, cache / "metadata.csv")
    tsv = fetch(SLR54_TSV, cache / "utt_spk_text.tsv")

    with open(meta, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    spk54 = {}
    with open(tsv, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            spk54[parts[0]] = parts[1]

    hours = lambda rs: sum(float(r["duration"]) for r in rs) / 3600
    print(f"\n== Overall: {len(rows)} clips, {hours(rows):.2f} h, "
          f"median {st.median(float(r['duration']) for r in rows):.2f} s")
    for k in ["quality", "gender", "sample_rate"]:
        print(f"{k}: {dict(collections.Counter(r[k] for r in rows))}")

    low = [r for r in rows if r["quality"] == "low"]
    high = [r for r in rows if r["quality"] == "high"]
    uid = lambda r: r["file_name"].split("/")[-1][:-4]

    print(f"\n== quality=low (SLR54): {len(low)} clips, {hours(low):.2f} h")
    matched = [spk54[uid(r)] for r in low if uid(r) in spk54]
    print(f"speaker IDs recovered: {len(matched)}/{len(low)}, speakers: {len(set(matched))}")
    per_spk = collections.Counter()
    for r in low:
        if uid(r) in spk54:
            per_spk[spk54[uid(r)]] += float(r["duration"])
    print(f"max minutes per speaker: {max(per_spk.values()) / 60:.1f}")

    print("\nTTS-grade filters on SLR54:")
    for dmin, snr in [(2.0, 13), (2.5, 15), (3.0, 15), (2.0, 18)]:
        s = [r for r in low if float(r["duration"]) >= dmin and float(r["snr_db"]) >= snr]
        spk = {spk54.get(uid(r)) for r in s}
        print(f"  dur>={dmin}s snr>={snr}dB: {len(s)} clips, {hours(s):.1f} h, {len(spk)} speakers")

    print(f"\n== quality=high: {len(high)} clips, {hours(high):.2f} h")
    by = collections.defaultdict(list)
    for r in high:
        name = r["file_name"].split("/")[-1]
        by[f"SLR43 #{name.split('_')[1]}" if name.startswith("nep_") else "Voice* (unknown source)"].append(r)
    for k, rs in sorted(by.items(), key=lambda kv: -hours(kv[1])):
        g = dict(collections.Counter(r["gender"] for r in rs))
        print(f"  {k:26s} {len(rs):4d} clips {hours(rs) * 60:5.1f} min  {g}")


if __name__ == "__main__":
    main()
