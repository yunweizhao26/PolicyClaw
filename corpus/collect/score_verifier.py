from __future__ import annotations

import argparse, json, math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATION = HERE / "validation"
LABELS = ["complete_policy", "partial_policy", "cookie_only", "other_legal", "not_policy"]
POSITIVE = "complete_policy"
Z95 = 1.959964


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    if n == 0:
        return math.nan, math.nan
    p = k / n
    centre, half = p + z * z / (2 * n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (centre - half) / (1 + z * z / n), (centre + half) / (1 + z * z / n)


def rate(k: int, n: int) -> str:
    if n == 0:
        return "n/a (0 pages)"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * k / n:.1f}% (95% CI {100 * lo:.1f} to {100 * hi:.1f})"


def read_jsonl(paths) -> dict:
    out, dupes = {}, []
    for path in paths:
        for n, line in enumerate(Path(path).read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{n}: {e}")
            if rec.get("id") in out:
                dupes.append(rec["id"])
            out[rec["id"]] = rec
    return out, dupes


def label_of(rec: dict | None) -> str:
    if rec is None:
        return "missing"
    return rec.get("label") if rec.get("label") in LABELS else "error"


def scores(pairs: list[tuple[str, str]]) -> dict:
    tp = sum(1 for h, v in pairs if h == POSITIVE and v == POSITIVE)
    v_pos = sum(1 for _, v in pairs if v == POSITIVE)
    h_pos = sum(1 for h, _ in pairs if h == POSITIVE)
    agree = sum(1 for h, v in pairs if h == v)
    return {"n": len(pairs), "tp": tp, "verifier_pos": v_pos, "labeler_pos": h_pos, "agree": agree}


def table(header: list[str], rows: list[list]) -> list[str]:
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header),
            *["| " + " | ".join(str(c) for c in row) + " |" for row in rows]]


def one_line(s: str) -> str:
    return " ".join(str(s).split()).replace("|", "/")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", type=Path, default=VALIDATION / "verifier.jsonl")
    parser.add_argument("--labels", type=Path, default=VALIDATION / "labels")
    parser.add_argument("--key", type=Path, default=VALIDATION / "key.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    key = json.loads(args.key.read_text())["pages"]
    human, human_dupes = read_jsonl(sorted(args.labels.glob("*.jsonl")))
    verifier, _ = read_jsonl([args.verifier])
    unknown = sorted(set(human) - set(key))
    ids = sorted(i for i in key if i in human)
    pairs = {i: (label_of(human[i]), label_of(verifier.get(i))) for i in ids}
    bad_human = sorted(i for i, (h, _) in pairs.items() if h not in LABELS)

    lines = ["# Verifier against labelers", "",
             f"Pages in the sample: {len(key)}. Labeled by the labelers: {len(ids)}. "
             f"Labeled by the verifier: {sum(1 for i in key if label_of(verifier.get(i)) in LABELS)}. "
             f"Scored (both): {sum(1 for h, v in pairs.values() if h in LABELS)}.", ""]
    if unknown or human_dupes or bad_human:
        lines += [f"Label problems: ids not in the sample {unknown}; ids labeled twice {sorted(set(human_dupes))}; "
                  f"labels outside the rubric {bad_human}.", ""]
    scored = {i: p for i, p in pairs.items() if p[0] in LABELS}
    s = scores(list(scored.values()))
    lines += ["## complete_policy", "",
              f"- Precision: {rate(s['tp'], s['verifier_pos'])}",
              f"- Recall: {rate(s['tp'], s['labeler_pos'])}",
              f"- Agreement on all five labels: {rate(s['agree'], s['n'])}", ""]

    columns = LABELS + sorted({v for _, v in scored.values()} - set(LABELS))
    matrix = Counter(scored.values())
    lines += ["## Confusion matrix", "", "Rows: labelers. Columns: verifier.", ""]
    lines += table(["labelers \\ verifier", *columns, "total"],
                   [[h, *[matrix[(h, v)] for v in columns], sum(matrix[(h, v)] for v in columns)] for h in LABELS]
                   + [["total", *[sum(matrix[(h, v)] for h in LABELS) for v in columns], len(scored)]])
    lines.append("")

    def breakdown(group_of) -> list[list]:
        groups = {}
        for i, p in scored.items():
            groups.setdefault(group_of(i), []).append(p)
        rows = []
        for g in sorted(groups):
            t = scores(groups[g])
            rows.append([g, t["n"], t["labeler_pos"], t["verifier_pos"], t["tp"], rate(t["tp"], t["verifier_pos"]),
                         rate(t["tp"], t["labeler_pos"]), rate(t["agree"], t["n"])])
        return rows

    head = ["group", "pages", "labelers complete", "verifier complete", "both complete", "precision", "recall",
            "agreement (5 labels)"]
    lines += ["## By source", ""] + table(head, breakdown(lambda i: key[i]["source"])) + [""]
    lines += ["## By stratum", ""] + table(head, breakdown(lambda i: key[i]["stratum"])) + [""]

    dist = {}
    for i, (h, v) in scored.items():
        dist.setdefault(key[i]["stratum"], [Counter(), Counter()])
        dist[key[i]["stratum"]][0][h] += 1
        dist[key[i]["stratum"]][1][v] += 1
    lines += ["## Label distribution by stratum", "", "Each cell: labelers / verifier.", ""]
    lines += table(["stratum", *LABELS], [[g, *[f"{d[0][c]} / {d[1][c]}" for c in LABELS]]
                                          for g, d in sorted(dist.items())]) + [""]

    both = [i for i in scored if label_of(verifier.get(i)) in LABELS]
    orgs = sum(1 for i in both if human[i].get("flags", {}).get("multiple_orgs")
               == verifier[i].get("flags", {}).get("multiple_orgs"))
    lang = sum(1 for i in both if str(human[i].get("flags", {}).get("language", "")).lower()
               == str(verifier[i].get("flags", {}).get("language", "")).lower())
    flagged = Counter((bool(human[i].get("flags", {}).get("multiple_orgs")),
                       bool(verifier[i].get("flags", {}).get("multiple_orgs"))) for i in both)
    lines += ["## Flags", "",
              f"- multiple_orgs agreement: {rate(orgs, len(both))}; true for labelers {flagged[(True, True)] + flagged[(True, False)]}, "
              f"for verifier {flagged[(True, True)] + flagged[(False, True)]}, for both {flagged[(True, True)]}",
              f"- language agreement: {rate(lang, len(both))}", ""]

    kinds = [("Verifier complete_policy, labelers not (false positives)", lambda h, v: v == POSITIVE != h),
             ("Labelers complete_policy, verifier not (false negatives)", lambda h, v: h == POSITIVE != v),
             ("Other disagreements", lambda h, v: h != v and POSITIVE not in (h, v))]
    lines += ["## Disagreements", ""]
    for title, test in kinds:
        chosen = sorted((key[i]["stratum"], i) for i, (h, v) in scored.items() if test(h, v))
        lines += [f"### {title}: {len(chosen)}", ""]
        for stratum, i in chosen:
            h, v = human[i], verifier.get(i, {})
            lines += [f"- **{i}** ({stratum}) {key[i]['url'] or 'no URL'}",
                      f"  - labelers: {label_of(h)}. {one_line(h.get('reason', ''))}",
                      f"  - verifier: {label_of(v)}. {one_line(v.get('reason', v.get('error', '')))}"]
        lines.append("")

    report = "\n".join(lines)
    print(report)
    if args.out:
        args.out.write_text(report + "\n")


if __name__ == "__main__":
    main()
